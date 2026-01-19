from integrations.hevy.client import HevyClient
from integrations.hevy.serializers import serialize_workout
from integrations.hevy.utils import is_date_in_current_week


def get_current_week_workouts(page=1, page_size=10):
    page_size = min(page_size, 10) 
    client = HevyClient()

    data = client.get(
        "/workouts",
        params={
            "page": page,
            "pageSize": page_size
        }
    )

    workouts = data.get("workouts", [])

    # filtra só os da semana atual
    weekly_workouts = [
        w for w in workouts
        if is_date_in_current_week(w.get("start_time"))
    ]

    return [serialize_workout(w) for w in weekly_workouts]
