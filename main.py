from ortools.sat.python import cp_model

def main():
    # University scheduling parameters
    num_professors = 5  # Total professors
    num_subjects = 5     # Total subjects
    num_days = 5         # Number of days in the week
    num_slots = 4        # Number of time slots per day
    num_halls = 3        # Number of available halls

    all_professors = range(num_professors)
    all_subjects = range(num_subjects)
    all_days = range(num_days)
    all_slots = range(num_slots)
    all_halls = range(num_halls)

    # Professors' preferences (1 = preferred time slot, 0 = not preferred)
    # zawdo yb2o 6 slots 3lchan yakhod el youm kol sa3tn sa3tn
    preferences = [
        [[1, 0, 0, 1 ], [0, 1, 0, 0], [1, 0, 0, 0], [0, 1, 0, 1], [0, 0, 1, 0]],
        [[0, 1, 0, 0], [0, 0, 1, 1], [1, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 1]],
        [[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0]],
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1], [0, 1, 0, 0], [1, 0, 0, 0]],
        [[0, 1, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1]],
    ]

    # Create the model
    model = cp_model.CpModel()

    # Variables: schedule[(prof, subj, day, slot, hall)] = 1 if scheduled
    schedule = {}
    for p in all_professors:
        for s in all_subjects:
            for d in all_days:
                for t in all_slots:
                    for h in all_halls:
                        schedule[(p, s, d, t, h)] = model.new_bool_var(f"schedule_p{p}_s{s}_d{d}_t{t}_h{h}")

    # Constraint: Each subject must be assigned exactly once
    for s in all_subjects:
        model.add_exactly_one(schedule[(p, s, d, t, h)] for p in all_professors for d in all_days for t in all_slots for h in all_halls)

    # Constraint: Each professor can teach only one subject per time slot
    for p in all_professors:
        for d in all_days:
            for t in all_slots:
                model.add_at_most_one(schedule[(p, s, d, t, h)] for s in all_subjects for h in all_halls)

    # Constraint: Each hall can hold only one subject per time slot
    for h in all_halls:
        for d in all_days:
            for t in all_slots:
                model.add_at_most_one(schedule[(p, s, d, t, h)] for p in all_professors for s in all_subjects)

    # Objective: Maximize professors' preferred time slots
    model.maximize(
        sum(preferences[p][d][t] * schedule[(p, s, d, t, h)]
            for p in all_professors for s in all_subjects for d in all_days for t in all_slots for h in all_halls)
    )

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status == cp_model.OPTIMAL:
        print("Optimal Schedule:")
        for d in all_days:
            print(f"Day {d}:")
            for t in all_slots:
                for h in all_halls:
                    for p in all_professors:
                        for s in all_subjects:
                            if solver.value(schedule[(p, s, d, t, h)]) == 1:
                                print(f"  - Prof {p} teaches Subject {s} in Hall {h} at Slot {t}.")
            print()
    else:
        print("No optimal solution found!")

    # Statistics
    print("\nSolver Statistics:")
    print(f"  - Conflicts: {solver.num_conflicts}")
    print(f"  - Branches: {solver.num_branches}")
    print(f"  - Wall time: {solver.wall_time}s")

if __name__ == "__main__":
    main()
