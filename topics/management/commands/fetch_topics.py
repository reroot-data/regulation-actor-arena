import humps
import requests
from django.core.management.base import BaseCommand, CommandError
from rest_framework.parsers import JSONParser
from topics.models import Topic


class Command(BaseCommand):
    help = "Fetches all stages an initiative can have"

    def handle(self, *args, **options):
        import requests

        url = "https://ec.europa.eu/info/law/better-regulation/brpapi/topics/"

        payload = {}
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,nl;q=0.7,sr;q=0.6",
            "Cache-Control": "No-Cache",
            "Connection": "keep-alive",
            "Cookie": "_pk_ses.7bcd6c43-58a3-489c-aa36-10b24f1fd5b9.465b=*; _pk_id.7bcd6c43-58a3-489c-aa36-10b24f1fd5b9.465b=9c466a6f747faa1f.1655062394.9.1661010890.1661010686.; _pk_id.59.b924=d60f55cbe2fa3bbe.1648386270.3.1649755842.1649755809.; cck1=%7B%22cm%22%3Atrue%2C%22all1st%22%3Atrue%2C%22closed%22%3Afalse%7D",
            "Referer": "https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives_en?text=green%20deal",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()
        topics = response.json()

        for topic in topics:
            Topic.objects.get_or_create(**topic)
