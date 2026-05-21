from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# CORS (ważne dla HTML)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# MODEL DANYCH
# -------------------------
class FormData(BaseModel):
    name: str
    class_name: str
    subject: str

# -------------------------
# ENDPOINT ZAPISU
# -------------------------
@app.post("/save")
def save(data: FormData):

    text = f"Name: {data.name}, Class: {data.class_name}, Subject: {data.subject}\n"

    with open("data.txt", "a", encoding="utf-8") as f:
        f.write(text)

    return {"status": "saved"}
