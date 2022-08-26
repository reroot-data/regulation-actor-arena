import http
from email import policy
from pprint import pprint
from re import A
from subprocess import call

import humps
import requests
from backend.requests import TimeoutHTTPAdapter, logging_hook
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from feedbacks.models import Feedback, FeedbackAttachment
from feedbacks.serializers import FeedbackAttachmentSerializer, FeedbackSerializer
from policy_areas.models import PolicyArea
from policy_areas.serializers import PolicyAreaSerializer
from publication_documents.models import Attachment, Link, Publication
from publication_documents.serializers import (
    AttachmentSerializer,
    LinkSerializer,
    PublicationSerializer,
)
from requests.adapters import HTTPAdapter, Retry
from topics.models import Topic
from topics.serializer import TopicSerializer

from ...models import Initiative, LegalBasis
from ...serializers import InitiativeSerializer, LegalBasisSerializer


class Command(BaseCommand):
    help = "Fetches the initiatives from the Have your say platform"

    def get_data_total_from_response(self, response):
        """
        returns a tupe of (data, total_pages) from a response
        """
        response_json = response.json()
        response_data = response_json.get("_embedded", {}).get(
            "initiativeResultDtoes", []
        )
        response_total_pages = response_json.get("page", {}).get("totalPages", 0)

        return response_data, response_total_pages

    def get_request(
        self,
    ):
        retry_strategy = Retry(total=3, backoff_factor=30)
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
            }
        )
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        return http

    def fetch_initiative_detail(self, initiative):
        """
        fetches and saves initiatives
        """

        id = initiative.pop("id")
        if Initiative.objects.filter(id=id).exists():
            # Do not fetch detail if already in the database
            return

        print("fetch initiative ", id)
        DETAIL_URL = (
            "https://ec.europa.eu/info/law/better-regulation/brpapi/groupInitiatives"
        )

        detail_response = self.get_request().get(
            f"{DETAIL_URL}/{id}",
            params={"language": "EN"},
        )
        detail_response.raise_for_status()
        data = humps.decamelize(detail_response.json())  # type: ignore
        publications = data.pop("publications")
        legal_basis = data.pop("legal_basis")
        policy_areas = data.pop("policy_areas")
        topics = data.pop("topics")
        serializer = InitiativeSerializer(
            Initiative.objects.filter(id=id).first(), data=data
        )

        # Save Initiative
        if serializer.is_valid():
            instance = serializer.save()
            # Save publications
            for publication in publications:
                attachments = publication.pop("attachments")
                links = publication.pop("useful_links")
                publication_serializer = PublicationSerializer(
                    Publication.objects.filter(id=publication["id"]).first(),
                    data=publication,
                )
                if publication_serializer.is_valid():
                    publication_obj = publication_serializer.save()
                    # Save links
                    for link in links:
                        link_serializer = LinkSerializer(
                            Link.objects.filter(**link).first(), data=link
                        )
                        if link_serializer.is_valid():
                            obj = link_serializer.save()
                            publication_obj.useful_links.add(obj)
                        else:
                            for key, error in link_serializer.errors.items():
                                print("link", key, error)
                    # Save attachments
                    for attachment in attachments:
                        attachment_serializer = AttachmentSerializer(
                            Attachment.objects.filter(id=attachment["id"]).first(),
                            data=attachment,
                        )
                        if attachment_serializer.is_valid():
                            obj = attachment_serializer.save()
                            publication_obj.attachments.add(obj)
                        else:
                            for key, error in attachment_serializer.errors.items():
                                print("attachment", key, error)
                    if publication["total_feedback"] > 0:
                        # Fetch feedbacks
                        call_command("fetch_feedback", publication_obj.id)
                        instance.publications.add(publication_obj)
                else:
                    for key, error in publication_serializer.errors.items():
                        print("publication", key, error)
            # Save legal_basis
            for legal_base in legal_basis:
                legal_base_serializer = LegalBasisSerializer(
                    LegalBasis.objects.filter(**legal_base).first(), data=legal_base
                )
                if legal_base_serializer.is_valid():
                    obj = legal_base_serializer.save()
                    instance.legal_basis.add(obj)
                else:
                    for key, error in legal_base_serializer.errors.items():
                        print("legal_base", key, error)
            # Save policy area
            for policy_area in policy_areas:
                policy_area_serializer = PolicyAreaSerializer(
                    PolicyArea.objects.filter(**policy_area).first(), data=policy_area
                )
                if policy_area_serializer.is_valid():
                    obj = policy_area_serializer.save()
                    instance.policy_areas.add(obj)
                else:
                    for key, error in serializer.errors.items():
                        print("policy_area", key, error)
            # Save topics
            for topic in topics:
                topic_serializer = TopicSerializer(
                    Topic.objects.filter(**topic).first(), data=topic
                )
                if topic_serializer.is_valid():
                    obj = topic_serializer.save()
                    instance.topics.add(obj)
                else:
                    for key, error in topic_serializer.errors.items():
                        print("topic", key, error)
        else:
            for key, error in serializer.errors.items():
                print("initiative", key, error)

    def handle(self, *args, **options):
        # self.stdout.write("fetch stages")
        call_command("fetch_stages")
        # self.stdout.write("fetch types")
        call_command("fetch_types")
        # self.stdout.write("fetch topics")
        call_command("fetch_topics")
        # self.stdout.write("fetch user types")
        call_command("fetch_user_types")
        # self.stdout.write("fetch countries")
        call_command("fetch_countries")

        URL = (
            f"https://ec.europa.eu/info/law/better-regulation/brpapi/searchInitiatives"
        )
        PARAMS = {"size": 10, "language": "EN", "page": 0}

        self.stdout.write("fetch initiatives")

        first_page = self.get_request().get(
            URL,
            params=PARAMS,
        )
        first_page.raise_for_status()
        data, total_pages = self.get_data_total_from_response(first_page)
        for initiative in data:
            self.fetch_initiative_detail(initiative)

        for page in range(0, total_pages):
            # self.stdout.write(f"initiatives:  page {page + 1} from {total_pages}")
            PARAMS["page"] = page
            page = self.get_request().get(
                URL,
                params=PARAMS,
            )
            initiatives, _ = self.get_data_total_from_response(page)

            for initiative in initiatives:
                self.fetch_initiative_detail(initiative)
