# FastAPI backend ana dosyası
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import pandas as pd

app = FastAPI()

# CORS middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

class UserCreate(BaseModel):
    name: str

@app.get("/")
def read_root():
    return {"message": "Merhaba, FastAPI çalışıyor!"}

@app.post("/users/")
def create_user(user: UserCreate):
    users = load_users()
    new_id = max([u['id'] for u in users], default=0) + 1
    user_dict = {"id": new_id, "name": user.name}
    users.append(user_dict)
    save_users(users)
    return user_dict

@app.get("/users/")
def read_users():
    return load_users()

@app.get("/kitaplar")
def get_kitaplar():
    xlsx_path = os.path.join(os.path.dirname(__file__), 'Kitap1.xlsx')
    if not os.path.exists(xlsx_path):
        return {"error": "Kitap1.xlsx bulunamadı."}
    df = pd.read_excel(xlsx_path)
    return df.to_dict(orient="records")

@app.get("/kanunlar")
def get_kanunlar():
    xlsx_path = os.path.join(os.path.dirname(__file__), 'kanun.xlsx')
    if not os.path.exists(xlsx_path):
        return {"error": "kanun.xlsx bulunamadı."}
    df = pd.read_excel(xlsx_path)
    return df.to_dict(orient="records")

@app.get("/analyze-excel")
def analyze_excel():
    excel_path = os.path.join(os.path.dirname(__file__), 'yeni.xlsx')
    if not os.path.exists(excel_path):
        return {"error": "Excel dosyası bulunamadı."}
    try:
        df = pd.read_excel(excel_path)
        info = {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "column_names": df.columns.tolist(),
            "sample_data": df.head(5).to_dict(orient="records")
        }
        return info
    except Exception as e:
        return {"error": str(e)}

