import os
import requests
from dotenv import load_dotenv

load_dotenv()


class HevyClient:
    def __init__(self):
        self.base_url = os.getenv("HEVY_BASE_URL")
        self.api_key = os.getenv("HEVY_API_KEY")

        if not self.api_key:
            raise RuntimeError("HEVY_API_KEY não definida no .env")

        self.headers = {
            "accept": "application/json",
            "api-key": self.api_key
        }

    def get(self, endpoint: str, params: dict | None = None):
        url = f"{self.base_url}{endpoint}"

        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=30
        )

        response.raise_for_status()
        return response.json()
