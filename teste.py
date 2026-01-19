from integrations.hevy.workouts import get_current_week_workouts

if __name__ == "__main__":
    workouts = get_current_week_workouts()

    for w in workouts:
        print("=" * 50)
        print("Treino:", w["title"])

        for ex in w["exercises"]:
            print(f"\n{ex['name']}")
            print("Reps:", ex["reps_range"])

            for s in ex["sets_detail"]:
                print(
                    f"  - {s['type']} | "
                    f"{s['weight_kg']} kg x {s['reps']} reps"
                )
