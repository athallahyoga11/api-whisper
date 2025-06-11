# QUICK STARTUP GUIDE

## Backend

### Install dependencies

⁠ bash
cd api-whisper

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

### How to Run

apt install uvicorn

nohup uvicorn main:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &
