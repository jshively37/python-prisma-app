import requests
import typing as t
from urllib.error import HTTPError

ENDPOINTS = {}
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
        print(PRISMA_HEADERS)
        self.session.headers = PRISMA_HEADERS

    def _create_access_token(self):
        url = "https://auth.apps.paloaltonetworks.com/oauth2/access_token"
        auth_data = f"{GRANT_TYPE}:{self.tsg_id}"
        auth_info = (self.client_id, self.client_secret)
        response = requests.post(
            url=url, headers=PRISMA_HEADERS, data=auth_data, auth=auth_info
        ).json()
        PRISMA_HEADERS.update({"Authorization": f"Bearer {response['access_token']}"})

    def make_request(self) -> t.Dict:
        pass
