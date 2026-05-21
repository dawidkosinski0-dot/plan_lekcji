from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI()

# CORS (żeby działał frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MODEL danych z formularza
class Lesson(BaseModel):
    class_name: str
    subject: str
    teacher: str


# test czy działa
@app.get("/")
def home():
    return {"status": "API działa"}


# zapis danych
@app.post("/save")
def save(lesson: Lesson):

    # jeśli plik nie istnieje → tworzymy
    if not os.path.exists("data.json"):
        with open("data.json", "w") as f:
            json.dump([], f)

    # wczytaj dane
    with open("data.json", "r") as f:
        data = json.load(f)

    # dodaj nowy wpis
    data.append(lesson.dict())

    # zapisz
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

    return {"status": "saved"}


# odczyt danych
@app.get("/lessons")
def get_lessons():

    if not os.path.exists("data.json"):
        return []

    with open("data.json", "r") as f:
        return json.load(f)
