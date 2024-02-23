import json
import typing as t
import requests
import sys

BASE_URL = "https://api.sase.paloaltonetworks.com/sse/config/v1/"

ENDPOINTS = {
    'push_config': 'config-versions/candidate:push',
    'get_decrpyt': 'decryption-exclusions?folder=Mobile Users',
    'decrypt_exclusions': 'decryption-exclusions?folder=Mobile Users'
}
GRANT_TYPE = "grant_type=client_credentials&scope=tsg_id"
PRISMA_HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}


class PrismaClient:
    def __init__(
        self,
        tsg_id: str,
        client_id: str,
        client_secret: str,
    ):
        self.tsg_id = tsg_id
        self.client_id = client_id
        self.client_secret = client_secret

    def create_session(self) -> None:
        self._create_access_token()
        self.session = requests.Session()
        self.session.headers = PRISMA_HEADERS

    def _create_access_token(self) -> None:
        url = "https://auth.apps.paloaltonetworks.com/oauth2/access_token"
        auth_data = f"{GRANT_TYPE}:{self.tsg_id}"
        auth_info = (self.client_id, self.client_secret)
        try:
            response = requests.post(
                url=url, headers=PRISMA_HEADERS, data=auth_data, auth=auth_info
            ).json()
            PRISMA_HEADERS.update(
                {"Authorization": f"Bearer {response['access_token']}"}
            )
        except KeyError:
            sys.exit(
                "Please validate your TSG, client id, or client secret and try again"
            )
        except Exception as e:
            sys.exit(f"General error has occured: {e}")

    def make_request(self) -> t.Dict:
        pass

    def get_ssl_decrypt_bypass(self) -> None:
        url = BASE_URL + ENDPOINTS['get_decrpyt']
        print(url)
        response = requests.get(url=url, headers=PRISMA_HEADERS)
        print(response.text)

    def add_ssl_decrypt_bypass(self) -> None:
        payload = {
            "description": "test bypass",
            "name": "https://go.boardbooks.com"
        }
        print(payload)
        url = BASE_URL + ENDPOINTS['decrypt_exclusions']
        print(url)
        response = requests.post(url=url, headers=PRISMA_HEADERS, data=payload)
        print(response.text)

    def commit_config(self) -> None:
        url = BASE_URL + ENDPOINTS['push_config']
        payload = {
            'description': 'automated push',
            'folders': ['Mobile Users']
        }
        response = requests.post(url=url, headers=PRISMA_HEADERS, json=payload)
        print(response.text)
