# Jasper Whisper Backend & Android App

Repositori ini berisi panduan lengkap untuk:

- Menjalankan **backend** transkripsi suara menggunakan FastAPI + Whisper
- Membangun dan menginstal **aplikasi Android Jasper**
- Menghubungkan aplikasi Android ke backend melalui **VPN ITS**

---

## 📦 Backend (FastAPI Whisper)

### 🔧 Install Dependencies

```bash
cd api-whisper

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
