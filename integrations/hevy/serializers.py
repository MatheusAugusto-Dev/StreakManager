def serialize_routine(routine: dict) -> dict:
    exercises_output = []

    for exercise in routine.get("exercises", []):
        name = exercise.get("title", "Unknown Exercise")
        rest_seconds = exercise.get("rest_seconds")

        sets = exercise.get("sets", [])
        sets_count = len(sets)

        reps_values = []

        for s in sets:
            # prioridade: rep_range
            if s.get("rep_range"):
                start = s["rep_range"].get("start")
                end = s["rep_range"].get("end")

                if start and end:
                    reps_values.append((start, end))
                elif start:
                    reps_values.append((start, start))

            # fallback: reps simples
            elif s.get("reps"):
                reps_values.append((s["reps"], s["reps"]))

        # normaliza reps
        if reps_values:
            min_reps = min(r[0] for r in reps_values)
            max_reps = max(r[1] for r in reps_values)

            reps = (
                f"{min_reps}-{max_reps}"
                if min_reps != max_reps
                else str(min_reps)
            )
        else:
            reps = None

        exercises_output.append({
            "name": name,
            "sets": sets_count,
            "reps": reps,
            "rest_seconds": rest_seconds
        })

    return {
        "routine_name": routine.get("title"),
        "exercise_count": len(exercises_output),
        "exercises": exercises_output
    }

def serialize_workout(workout: dict) -> dict:
    exercises_output = []

    for exercise in workout.get("exercises", []):
        sets = exercise.get("sets", [])

        sets_detail = []
        reps_values = []

        for s in sets:
            reps = s.get("reps")
            weight = s.get("weight_kg")
            set_type = s.get("type")

            # considera apenas sets com reps (musculação)
            if reps is not None:
                sets_detail.append({
                    "type": set_type,
                    "weight_kg": weight,
                    "reps": reps
                })
                reps_values.append(reps)

        # faixa de reps
        if reps_values:
            min_reps = min(reps_values)
            max_reps = max(reps_values)
            reps_range = (
                f"{min_reps}-{max_reps}"
                if min_reps != max_reps
                else str(min_reps)
            )
        else:
            reps_range = None

        exercises_output.append({
            "name": exercise.get("title"),
            "sets_total": len(sets_detail),
            "reps_range": reps_range,
            "sets_detail": sets_detail
        })

    return {
        "workout_id": workout.get("id"),
        "title": workout.get("title"),
        "routine_id": workout.get("routine_id"),
        "start_time": workout.get("start_time"),
        "end_time": workout.get("end_time"),
        "exercise_count": len(exercises_output),
        "exercises": exercises_output
    }
