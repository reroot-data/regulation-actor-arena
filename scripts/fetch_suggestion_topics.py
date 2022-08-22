import requests

url = "https://ec.europa.eu/info/law/better-regulation/brpapi/suggestionTopics/"

payload = {}
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,nl;q=0.7,sr;q=0.6",
    "Cache-Control": "No-Cache",
    "Connection": "keep-alive",
    "Referer": "https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/12970-Review-of-the-EU-school-fruit-vegetables-and-milk-scheme/feedback_en?p_id=25977074",
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

print(response.text)
# {
#     "code": "TOPIC1_2022",
#     "label": "How to favour interconnectivity between the digital and the green transition, including through simplification?",
#     "jsonLinks": null
# },
