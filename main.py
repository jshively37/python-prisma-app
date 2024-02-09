import os
from prisma.client import PrismaClient
from dotenv import load_dotenv

load_dotenv()
TSG_ID = os.environ.get("TSG_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")


if __name__ == "__main__":
    client = PrismaClient(
        tsg_id=TSG_ID,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    client.create_session()
