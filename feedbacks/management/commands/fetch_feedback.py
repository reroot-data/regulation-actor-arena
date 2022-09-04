import time

import humps
import requests
from backend.requests import TimeoutHTTPAdapter
from django.core.management.base import BaseCommand, CommandParser
from feedbacks.models import Feedback, FeedbackAttachment
from feedbacks.serializers import FeedbackAttachmentSerializer, FeedbackSerializer
from requests.adapters import HTTPAdapter, Retry


class Command(BaseCommand):
    help = "Fetches the initiatives from the Have Your Say platform"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("publication_id", type=int)

    def get_request(
        self,
    ):
        retry_strategy = Retry(
            total=5,
            backoff_factor=30,
        )
        adapter = TimeoutHTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
            }
        )
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        return http

    def get_data_total_from_response(self, response):
        """
        returns a tupe of (data, total_pages) from a response
        """
        response.raise_for_status()
        response_json = response.json()
        response_data = response_json.get("_embedded", {}).get(
            "initiativeResultDtoes", []
        )
        response_total_pages = response_json.get("page", {}).get("totalPages", 0)

        return response_data, response_total_pages

    def fetch_feedback_detail(self, feedback, publication_id: int):
        _ = feedback.pop("_links")
        attachments = feedback.pop("attachments")
        feedback["country"] = feedback.get("country", "")
        feedback["user_type"] = feedback.get("user_type", "")
        feedback_data = humps.decamelize(  # type: ignore
            {"publication_object": publication_id, **feedback}
        )

        feedback_serializer = FeedbackSerializer(
            Feedback.objects.filter(id=feedback_data["id"]).first(), data=feedback_data  # type: ignore
        )
        if feedback_serializer.is_valid():
            obj = feedback_serializer.save()
            for attachment in attachments:
                attachment_serializer = FeedbackAttachmentSerializer(
                    FeedbackAttachment.objects.filter(id=attachment["id"]).first(),
                    data=attachment,
                )
                if attachment_serializer.is_valid():
                    attachment_obj = attachment_serializer.save()
                    obj.attachments.add(attachment_obj)
        else:
            for key, error in feedback_serializer.errors.items():
                print("feedback", key, error)

    def handle(self, *args, **options):
        publication_id = options["publication_id"]
        URL = "https://ec.europa.eu/info/law/better-regulation/brpapi/allFeedback"
        PARAMS = {"publicationId": publication_id, "size": 10, "page": 0}

        first_page = self.get_request().get(
            URL,
            params=PARAMS,
        )
        if not first_page:
            return
        first_page.raise_for_status()
        response_json = first_page.json()
        feedbacks = response_json.get("_embedded", {}).get("feedback", [])
        total_pages = response_json.get("page", {}).get("totalPages", 0)
        for feedback in feedbacks:
            self.fetch_feedback_detail(feedback, publication_id)

        for page in range(0, total_pages):
            # self.stdout.write(f"feedback fetch page {page + 1} from {total_pages}")
            PARAMS["page"] = page
            page = self.get_request().get(URL, params=PARAMS, timeout=5)
            feedbacks, _ = self.get_data_total_from_response(page)
            for feedback in feedbacks:
                self.fetch_feedback_detail(feedback, publication_id)
