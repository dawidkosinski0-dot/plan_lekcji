from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ortools.sat.python import cp_model

app = FastAPI()

# -----------------------------
# CORS (ważne na Render + frontend)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# DANE TESTOWE
# (na start — później zrobimy z formularza)
# -----------------------------
classes = ["1A", "1B"]

subjects = {
    "1A": ["Math", "English", "Physics"],
    "1B": ["Math", "English"]
}

teachers = {
    "Math": "Kowalski",
    "English": "Nowak",
    "Physics": "Wiśniewski"
}

DAYS = range(5)
HOURS = range(4)

# -----------------------------
# API START
# -----------------------------
@app.get("/")
def home():
    return {"status": "API działa"}

# -----------------------------
# GENERATOR PLANU LEKCJI
# -----------------------------
@app.get("/generate")
def generate():

    model = cp_model.CpModel()

    # x[class, subject, day, hour]
    x = {}

    for c in classes:
        for s in subjects[c]:
            for d in DAYS:
                for h in HOURS:
                    x[(c, s, d, h)] = model.NewBoolVar(f"{c}_{s}_{d}_{h}")

    # -----------------------------
    # 1. KAŻDY PRZEDMIOT 1 RAZ W TYGODNIU
    # -----------------------------
    for c in classes:
        for s in subjects[c]:
            model.Add(
                sum(x[(c, s, d, h)] for d in DAYS for h in HOURS) == 1
            )

    # -----------------------------
    # 2. MAX 1 LEKCJA W KLASIE W DANEJ GODZINIE
    # -----------------------------
    for c in classes:
        for d in DAYS:
            for h in HOURS:
                model.Add(
                    sum(x[(c, s, d, h)] for s in subjects[c]) <= 1
                )

    # -----------------------------
    # SOLVER
    # -----------------------------
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        return {"error": "Brak rozwiązania"}

    # -----------------------------
    # WYNIK
    # -----------------------------
    result = {}

    for c in classes:
        result[c] = []

        for d in DAYS:
            for h in HOURS:
                for s in subjects[c]:
                    if solver.Value(x[(c, s, d, h)]) == 1:
                        result[c].append({
                            "day": int(d),
                            "hour": int(h),
                            "subject": s,
                            "teacher": teachers[s]
                        })

    return result
