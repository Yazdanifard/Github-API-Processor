import requests
import hashlib
import json
from datetime import datetime
from dotenv import load_dotenv
from os import getenv

load_dotenv()

GITHUB_PAT = getenv("GITHUB_PAT", "")


class Reader:
    def __init__(self, specific_list_events: list) -> None:
        self.new_hashed = False
        self.specific_list_events = specific_list_events
        self.specific_events_count = {}
        self.start = False
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {GITHUB_PAT}",
        }
        # print(self.headers)
        self.request = Reader.__get_response(self)

    def __get_response(self) -> requests.models.Response:
        return requests.get(
            "https://api.github.com/events", stream=True, headers=self.headers
        )

    def __hashing_response(self) -> str:
        return hashlib.sha1(
            json.dumps(self.request.json(), sort_keys=True).encode()
        ).hexdigest()

    def get_new_event(self)->list:
        if self.new_hashed != self.__hashing_response():
            self.new_hashed = hash
            events = [
                x for x in self.request.json() if x["type"] in self.specific_list_events
            ]
            if events != []:
                row = [
                    (
                        x["repo"]["id"],
                        x["type"],
                        datetime.strptime(
                            x["created_at"], "%Y-%m-%dT%H:%M:%SZ"
                        ).strftime("%Y-%m-%d %H:%M:%S"),
                        x["repo"]["name"],
                    )
                    for x in events
                ]
                return row
            else:
                return None
