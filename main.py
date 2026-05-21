from fastapi.responses import PlainTextResponse
from ortools.sat.python import cp_model

@app.get("/generate", response_class=PlainTextResponse)
def generate():

    model = cp_model.CpModel()

    x = {}

    for c in classes:
        for s in subjects[c]:
            for d in DAYS:
                for h in HOURS:
                    x[(c, s, d, h)] = model.NewBoolVar(f"{c}_{s}_{d}_{h}")

    # 1 lekcja na przedmiot
    for c in classes:
        for s in subjects[c]:
            model.Add(
                sum(x[(c, s, d, h)] for d in DAYS for h in HOURS) == 1
            )

    # brak konfliktów w klasie
    for c in classes:
        for d in DAYS:
            for h in HOURS:
                model.Add(
                    sum(x[(c, s, d, h)] for s in subjects[c]) <= 1
                )

    solver = cp_model.CpSolver()
    solver.Solve(model)

    # -------------------------
    # TWORZENIE TEKSTU
    # -------------------------
    output = ""

    for c in classes:
        output += f"\n===== KLASA {c} =====\n"

        for d in DAYS:
            output += f"\nDzień {d}:\n"

            for h in HOURS:
                for s in subjects[c]:
                    if solver.Value(x[(c, s, d, h)]) == 1:
                        output += f"  Lekcja {h}: {s} ({teachers[s]})\n"

    return output
