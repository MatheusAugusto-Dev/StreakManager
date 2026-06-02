# from integrations.hevy.workouts import get_current_week_workouts

from integrations.hevy.routines import (
    get_routines,
    get_serialized_routines
)

def test_raw_routines():
    print("\n=== TESTE: ROTINAS (JSON BRUTO) ===")

    data = get_routines(page=1, page_size=5)

    print(f"Chaves retornadas: {list(data.keys())}")
    print(f"Total de rotinas: {len(data.get('routines', []))}")

    if data.get("routines"):
        r = data["routines"][0]
        print("\nExemplo de rotina bruta:")
        print("ID:", r.get("id"))
        print("Título:", r.get("title"))
        print("Qtd exercícios:", len(r.get("exercises", [])))


def test_serialized_routines():
    print("\n=== TESTE: ROTINAS SERIALIZADAS ===")

    routines = get_serialized_routines(page=2, page_size=10)

    print(f"Rotinas serializadas: {len(routines)}")

    for r in routines:
        print("\n" + "=" * 40)
        print("Rotina:", r.get("routine_name"))
        print("Qtd exercícios:", r.get("total_exercises"))

        for ex in r.get("exercises", []):
            print(
                f"- {ex.get('name')} | "
                f"{ex.get('sets')} sets | "
                f"{ex.get('reps', '—')} reps | "
                f"Descanso: {ex.get('rest_seconds')}s"
            )


if __name__ == "__main__":
    test_raw_routines()
    test_serialized_routines()

# if __name__ == "__main__":
#     workouts = get_current_week_workouts()

#     for w in workouts:
#         print("=" * 50)
#         print("Treino:", w["title"])

#         for ex in w["exercises"]:
#             print(f"\n{ex['name']}")
#             print("Reps:", ex["reps_range"])

#             for s in ex["sets_detail"]:
#                 print(
#                     f"  - {s['type']} | "
#                     f"{s['weight_kg']} kg x {s['reps']} reps"
#                 )
