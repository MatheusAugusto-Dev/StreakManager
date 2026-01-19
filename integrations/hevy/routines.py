from integrations.hevy.client import HevyClient
from integrations.hevy.serializers import serialize_routine


def get_routines(page: int = 1, page_size: int = 10) -> dict:
    """
    Obtém rotinas de treino do Hevy.
    Retorna o JSON bruto da API.
    """

    client = HevyClient()

    params = {
        "page": page,
        "pageSize": page_size
    }

    data = client.get("/routines", params=params)
    return data

def get_serialized_routines(page=1, page_size=10):
    client = HevyClient()

    data = client.get(
        "/routines",
        params={
            "page": page,
            "pageSize": page_size
        }
    )

    return [serialize_routine(r) for r in data.get("routines", [])]