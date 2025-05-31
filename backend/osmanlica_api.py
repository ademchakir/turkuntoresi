from fastapi import FastAPI, File, UploadFile, Body, Request as FastAPIRequest
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import io
from pdf2image import convert_from_bytes
from typing import List
import os
import json
import base64
import requests
from fastapi.responses import PlainTextResponse, FileResponse
from bs4 import BeautifulSoup
import subprocess
from fastapi import APIRouter, HTTPException
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def limit_upload_size(request: FastAPIRequest, call_next):
    max_body_size = 100 * 1024 * 1024  # 100 MB
    if request.headers.get("content-length"):
        if int(request.headers["content-length"]) > max_body_size:
            return PlainTextResponse("Dosya çok büyük! (100MB limiti aşıldı)", status_code=413)
    return await call_next(request)

# Basit Osmanlıca-Latin harf çevirici (örnek)
def osmanlica_to_latin(text):
    harf_cevir = {
        "ا": "a", "ب": "b", "ج": "c", "د": "d", "ه": "e", "ف": "f", "گ": "g", "ح": "h", "ی": "i",
        "ژ": "j", "ک": "k", "ل": "l", "م": "m", "ن": "n", "و": "o", "پ": "p", "ق": "q", "ر": "r",
        "س": "s", "ت": "t", "ع": "u", "و": "v", "ش": "ş", "چ": "ç", "ط": "t", "ظ": "z", "ز": "z",
        "ص": "s", "ض": "z", "ث": "s", "خ": "h", "غ": "ğ", "ء": "'", "ذ": "z", "ؤ": "u", "ئ": "i",
        "ى": "a", "ة": "e", "آ": "a", "أ": "a", "إ": "i", "ء": "'"
    }
    return ''.join([harf_cevir.get(c, c) for c in text])

class OsmanlicaMetin(BaseModel):
    metin: str

@app.post("/cevir")
def cevir(metin: OsmanlicaMetin):
    latin = osmanlica_to_latin(metin.metin)
    return {"latin": latin}

def preprocess_image(image):
    # Gri tonlama
    image = image.convert('L')
    # Kontrastı artır
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    # Gürültü azaltma (opsiyonel)
    image = image.filter(ImageFilter.MedianFilter(size=3))
    # Basit threshold (siyah-beyaz)
    image = image.point(lambda x: 0 if x < 140 else 255, '1')
    return image

@app.post("/ocr")
def ocr(file: UploadFile = File(...)):
    try:
        image_bytes = file.file.read()
        image = Image.open(io.BytesIO(image_bytes))
        image = preprocess_image(image)
        osmanlica_text = pytesseract.image_to_string(image, lang='osd')
        latin = osmanlica_to_latin(osmanlica_text)
        return {"osmanlica": osmanlica_text, "latin": latin}
    except Exception as e:
        return {"error": str(e)}

PDF_POPPLER_PATH = r"C:\\poppler\\bin"  # Poppler'ın kurulu olduğu dizin (gerekirse değiştirin)

@app.post("/pdf-ocr")
def pdf_ocr(file: UploadFile = File(...)):
    print(f"[PDF-OCR] Yükleme başladı: {file.filename}")
    try:
        pdf_bytes = file.file.read()
        print(f"[PDF-OCR] Dosya boyutu: {len(pdf_bytes)} byte")
        images = convert_from_bytes(pdf_bytes, poppler_path=PDF_POPPLER_PATH)
        print(f"[PDF-OCR] {len(images)} sayfa bulundu.")
        all_osmanlica = []
        all_latin = []
        for idx, img in enumerate(images):
            print(f"[PDF-OCR] Sayfa {idx+1} OCR başlıyor...")
            img = preprocess_image(img)
            osmanlica_text = pytesseract.image_to_string(img, lang='osd')
            latin = osmanlica_to_latin(osmanlica_text)
            all_osmanlica.append(osmanlica_text)
            all_latin.append(latin)
            print(f"[PDF-OCR] Sayfa {idx+1} tamamlandı.")
        print(f"[PDF-OCR] Tüm sayfalar tamamlandı.")
        return {
            "osmanlica": all_osmanlica,
            "latin": all_latin
        }
    except Exception as e:
        print(f"[PDF-OCR] Hata: {e}")
        return {"error": str(e)}

# Basit sözlük örneği
osmanlica_sozluk = {
    "علم": "bilim",
    "كتاب": "kitap"
}

@app.get("/anlam/{kelime}")
def anlam(kelime: str):
    return {"anlam": osmanlica_sozluk.get(kelime, "Bulunamadı")}

@app.get("/osmanlica-anlam/{kelime}")
def osmanlica_anlam(kelime: str):
    try:
        url = f"https://www.osmanlicasozlukler.com/arama?q={kelime}"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return {"error": f"Siteye erişilemedi: {resp.status_code}"}
        soup = BeautifulSoup(resp.text, "html.parser")
        sonuc = soup.find("div", class_="sonuc")
        if not sonuc:
            return {"anlam": "Bulunamadı"}
        # Anlamı ilk <li> içinde bul
        li = sonuc.find("li")
        if li:
            return {"anlam": li.get_text(strip=True)}
        return {"anlam": sonuc.get_text(strip=True)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/latin-anlamlar")
def latin_anlamlar(metin: str):
    # Metni kelimelere ayır
    kelimeler = [k.strip().lower() for k in metin.split() if k.strip()]
    anlamlar = {}
    for kelime in kelimeler:
        try:
            url = f"https://www.osmanlicasozlukler.com/arama?q={kelime}"
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200:
                anlamlar[kelime] = f"Siteye erişilemedi: {resp.status_code}"
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            sonuc = soup.find("div", class_="sonuc")
            if not sonuc:
                anlamlar[kelime] = "Bulunamadı"
                continue
            li = sonuc.find("li")
            if li:
                anlamlar[kelime] = li.get_text(strip=True)
            else:
                anlamlar[kelime] = sonuc.get_text(strip=True)
        except Exception as e:
            anlamlar[kelime] = f"Hata: {e}"
    return {"anlamlar": anlamlar}

# Düzeltme veritabanı dosyası
DUZELTME_DB = os.path.join(os.path.dirname(__file__), 'duzeltmeler.json')

def load_duzeltmeler():
    if not os.path.exists(DUZELTME_DB):
        return []
    with open(DUZELTME_DB, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_duzeltmeler(duzeltmeler):
    with open(DUZELTME_DB, 'w', encoding='utf-8') as f:
        json.dump(duzeltmeler, f, ensure_ascii=False, indent=2)

# Düzeltme ekleme endpoint'i (görsel veya metin ile)
class Duzeltme(BaseModel):
    yanlis: str  # Yanlış okunan kelime veya base64 görsel
    dogru: str   # Doğru hali
    tip: str = "metin"  # "metin" veya "gorsel"

@app.post("/duzeltme-ekle")
def duzeltme_ekle(duzeltme: Duzeltme):
    duzeltmeler = load_duzeltmeler()
    duzeltmeler.append(duzeltme.dict())
    save_duzeltmeler(duzeltmeler)
    return {"status": "ok"}

# OCR sonrası düzeltme uygulayan fonksiyon (hem metin hem görsel için)
def apply_duzeltmeler(text: str) -> str:
    duzeltmeler = load_duzeltmeler()
    for d in duzeltmeler:
        if d.get("tip") == "metin" and d.get("yanlis") in text:
            text = text.replace(d["yanlis"], d["dogru"])
        # Görsel tabanlı düzeltme için ek geliştirme gerekebilir
    return text

@app.post("/ocr-duzeltmeli")
def ocr_duzeltmeli(file: UploadFile = File(...)):
    try:
        image_bytes = file.file.read()
        image = Image.open(io.BytesIO(image_bytes))
        image = preprocess_image(image)
        osmanlica_text = pytesseract.image_to_string(image, lang='osd')
        osmanlica_text = apply_duzeltmeler(osmanlica_text)
        latin = osmanlica_to_latin(osmanlica_text)
        return {"osmanlica": osmanlica_text, "latin": latin}
    except Exception as e:
        return {"error": str(e)}

@app.post("/pdf-ocr-duzeltmeli")
def pdf_ocr_duzeltmeli(file: UploadFile = File(...)):
    try:
        pdf_bytes = file.file.read()
        images = convert_from_bytes(pdf_bytes)
        all_osmanlica = []
        all_latin = []
        for img in images:
            img = preprocess_image(img)
            osmanlica_text = pytesseract.image_to_string(img, lang='osd')
            osmanlica_text = apply_duzeltmeler(osmanlica_text)
            latin = osmanlica_to_latin(osmanlica_text)
            all_osmanlica.append(osmanlica_text)
            all_latin.append(latin)
        return {
            "osmanlica": all_osmanlica,
            "latin": all_latin
        }
    except Exception as e:
        return {"error": str(e)}

def extract_miladi_year(date_str):
    """
    Verilen tarih bilgisinden miladi yılı (M ile başlayan satırdan) ayıklar.
    Örnek giriş: 'M 04 KASIM 1839' veya 'M 1839' veya 'M 04 1839'
    """
    if not date_str:
        return None
    for part in date_str.split("\n"):
        part = part.strip()
        if part.startswith("M "):
            # M ile başlayan satırı al
            tokens = part.split()
            for token in reversed(tokens):
                if token.isdigit() and len(token) == 4:
                    return int(token)
    return None

@app.get("/kanunlar-yil-araligi")
def kanunlar_yil_araligi(baslangic: int, bitis: int):
    """
    kanun.xlsx dosyasındaki kanunları, miladi yıl aralığına göre filtreler.
    Parametreler:
        baslangic: Başlangıç yılı (dahil)
        bitis: Bitiş yılı (dahil)
    """
    dosya_yolu = os.path.join(os.path.dirname(__file__), 'kanun.xlsx')
    df = pd.read_excel(dosya_yolu)
    # İlk sütunda tarih bilgisi olduğunu varsayıyoruz
    kanunlar = []
    for idx, row in df.iterrows():
        tarih_bilgi = str(row[0])
        yil = extract_miladi_year(tarih_bilgi)
        if yil and baslangic <= yil <= bitis:
            # Tüm satırı dict olarak ekle
            kanunlar.append(row.to_dict())
    return {"kanunlar": kanunlar}

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Sadece PDF dosyaları yüklenebilir."}
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    # Link oluştur (örnek: /pdfs/filename.pdf)
    link = f"/pdfs/{file.filename}"
    return {"link": link}

@app.get("/pdfs/{filename}")
async def get_pdf(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Dosya bulunamadı.")
    return FileResponse(file_path, media_type="application/pdf")

