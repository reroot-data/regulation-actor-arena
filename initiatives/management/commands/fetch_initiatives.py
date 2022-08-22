from subprocess import call

import humps
import requests
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from rest_framework.parsers import JSONParser

from ...models import Initiative
from ...serializers import InitiativeSerializer


class Command(BaseCommand):
    help = "Fetches the initiatives from the Have your say platform"

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

    def fetch_initiative_detail(self, initiative):
        """
        fetches and saves initiatives
        """
        DETAIL_URL = (
            "https://ec.europa.eu/info/law/better-regulation/brpapi/groupInitiatives"
        )
        DETAIL_HEADERS = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,nl;q=0.7,sr;q=0.6",
            "Cache-Control": "No-Cache",
            "Connection": "keep-alive",
            "Referer": "https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/13526-Social-economy-developing-framework-conditions_en",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
        }

        id = initiative.pop("id")
        print("fetch initiative ", id)
        detail_response = requests.get(
            f"{DETAIL_URL}/{id}",
            headers=DETAIL_HEADERS,
            params={"language": "EN"},
        )
        detail_response.raise_for_status()
        data = humps.decamelize(detail_response.json())  # type: ignore
        publications = data.pop("publications")
        serializer = InitiativeSerializer(
            Initiative.objects.filter(id=id).first(), data=data
        )

        if serializer.is_valid():
            serializer.save()
        else:
            for key, error in serializer.errors.items():
                print(key, error)

    def handle(self, *args, **options):
        self.stdout.write("fetch stages")
        call_command("fetch_stages")
        self.stdout.write("fetch types")
        call_command("fetch_types")
        self.stdout.write("fetch topics")
        call_command("fetch_topics")
        LIST_URL = (
            f"https://ec.europa.eu/info/law/better-regulation/brpapi/searchInitiatives"
        )
        FEEDBACK_URL = (
            "https://ec.europa.eu/info/law/better-regulation/brpapi/allFeedback"
        )

        ### PAYLOAD
        PAYLOAD = {}

        ### HEADERS
        LIST_HEADERS = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,nl;q=0.7,sr;q=0.6",
            "Cache-Control": "No-Cache",
            "Connection": "keep-alive",
            "Referer": "https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives_en",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
        }

        ### PARAMS
        LIST_PARAMS = {"size": 100, "language": "EN", "page": 0}

        self.stdout.write("fetch first page")
        first_page = requests.get(
            LIST_URL,
            headers=LIST_HEADERS,
            params=LIST_PARAMS,
            data=PAYLOAD,
        )
        data, total_pages = self.get_data_total_from_response(first_page)
        for initiative in data:
            self.fetch_initiative_detail(initiative)

        for page in range(0, total_pages):
            self.stdout.write(f"fetch page {page + 1} from {total_pages}")
            LIST_PARAMS["page"] = page
            page = requests.get(
                LIST_URL, headers=LIST_HEADERS, params=LIST_PARAMS, data=PAYLOAD
            )
            initiatives, _ = self.get_data_total_from_response(page)

            for initiative in initiatives:
                self.fetch_initiative_detail(initiative)
