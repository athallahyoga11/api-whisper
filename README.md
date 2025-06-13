# Jasper Whisper Backend & Android App

Repositori ini berisi panduan singkat untuk menjalankan backend (FastAPI Whisper) dan menghubungkannya dengan aplikasi Android Jasper menggunakan jaringan ITS.

---

## 📦 Backend (FastAPI Whisper)

### 🔧 Install Dependencies

```bash
cd api-whisper

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

## Run Server

sudo apt install uvicorn

nohup uvicorn main:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &

## Android App
