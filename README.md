# 🎙️ Jasper Whisper - Voice Transcription System

Sistem transkripsi suara lengkap yang terdiri dari backend FastAPI dengan Whisper AI dan aplikasi Android native. Dirancang khusus untuk deployment di jaringan ITS dengan akses melalui VPN.

## 📋 Daftar Isi
- [Fitur Utama](#-fitur-utama)
- [Arsitektur Sistem](#-arsitektur-sistem)
- [Backend Setup](#-backend-setup)
- [Android App Setup](#-android-app-setup)
- [Konfigurasi VPN ITS](#-konfigurasi-vpn-its)
- [Testing & Debugging](#-testing--debugging)
- [Troubleshooting](#-troubleshooting)
- [Developer](#-developer)

## ✨ Fitur Utama

- **Backend FastAPI**: Server transkripsi dengan Whisper Small model
- **Android App**: Aplikasi native untuk recording dan upload audio
- **VPN Support**: Terintegrasi dengan VPN ITS untuk akses secure
- **RESTful API**: Dokumentasi lengkap dengan Swagger UI

## 🏗️ Arsitektur Sistem

```
[Android App] ←→ [VPN ITS] ←→ [FastAPI Backend + Whisper]
```

## 🔧 Backend Setup

### Prerequisites
- Python 3.8+
- Ubuntu/Debian server
- Port 8000 available

### Installation

1. **Clone dan Setup Environment**
   ```bash
   cd api-whisper
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Uvicorn (jika belum ada)**
   ```bash
   sudo apt update
   sudo apt install python3-pip
   pip install uvicorn
   ```

### Running the Server

**Development Mode:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Production Mode (Background):**
```bash
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &
```

**Monitor Logs:**
```bash
tail -f uvicorn.log
```

**Stop Server:**
```bash
# Cari process ID
ps aux | grep uvicorn
# Kill process
kill <PID>
```

## 📱 Android App Setup

### Installation Steps

1. **Transfer APK**
   - Via USB: Copy `app-debug.apk` ke folder Download
   - Via Bluetooth: Share file ke perangkat target
   - Via Cloud: Upload ke Google Drive/OneDrive

2. **Install APK**
   ```
   1. Buka File Manager di Android
   2. Navigate ke lokasi app-debug.apk
   3. Tap file APK
   4. Izinkan "Install from Unknown Sources" jika diminta
   5. Tap "Install"
   6. Tap "Open" setelah instalasi selesai
   ```

3. **Permissions Required**
   - Microphone access (untuk recording)
   - Internet access (untuk API calls)
   - Storage access (untuk temporary files)

## 🌐 Konfigurasi VPN ITS

### Setup OpenVPN

1. **Download OpenVPN Connect**
   - [Google Play Store](https://play.google.com/store/apps/details?id=net.openvpn.openvpn)
   - Atau search "OpenVPN Connect" di Play Store

2. **Download Konfigurasi VPN ITS**
   ```
   1. Buka browser, akses: https://vpn.its.ac.id
   2. Login dengan akun SSO ITS
   3. Download file konfigurasi (.ovpn)
   4. Save ke folder Download
   ```

3. **Import Konfigurasi**
   ```
   1. Buka aplikasi OpenVPN Connect
   2. Tap "+" atau "Import Profile"
   3. Pilih "File" tab
   4. Browse dan pilih file .ovpn yang sudah didownload
   5. Tap "Import"
   ```

4. **Connect ke VPN**
   ```
   1. Tap profile VPN ITS yang sudah diimport
   2. Masukkan username dan password ITS
   3. Tap "Connect"
   4. Tunggu hingga status "Connected"
   ```

### Verifikasi Koneksi VPN

**Test 1: Web Browser**
```
1. Buka browser di Android
2. Akses: http://[SERVER_IP]:8000/docs
3. Jika muncul Swagger UI, koneksi berhasil
```

**Test 2: Ping Test**
```bash
# Di terminal server
ping [ANDROID_VPN_IP]
```

## ⚙️ Konfigurasi Aplikasi Android

### 1. AndroidManifest.xml
Pastikan permissions sudah ditambahkan:
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
```

### 2. Network Configuration
Tambahkan network security config untuk HTTP:
```xml
<!-- AndroidManifest.xml -->
<application
    android:networkSecurityConfig="@xml/network_security_config"
    ... >
```

**res/xml/network_security_config.xml:**
```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">[SERVER_IP]</domain>
    </domain-config>
</network-security-config>
```

### 3. API Configuration
Update BASE_URL di konfigurasi Retrofit:
```kotlin
object ApiConfig {
    const val BASE_URL = "http://[SERVER_IP]:8000/"
    
    fun getApiService(): ApiService {
        val retrofit = Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
        return retrofit.create(ApiService::class.java)
    }
}
```

## 🧪 Testing & Debugging

### Backend Testing

**1. API Documentation**
```
URL: http://[SERVER_IP]:8000/docs
```

**2. Health Check**
```bash
curl -X GET "http://[SERVER_IP]:8000/health"
```

**3. Test Upload Audio**
```bash
curl -X POST "http://[SERVER_IP]:8000/transcribe" \
  -H "Content-Type: multipart/form-data" \
  -F "audio=@test_audio.wav"
```

### Android Testing

1. **Check VPN Connection**
   - Status bar harus menunjukkan icon VPN
   - Test akses ke server via browser

2. **Check App Permissions**
   - Settings > Apps > Jasper > Permissions
   - Pastikan Microphone dan Storage enabled

3. **Debug Logs**
   ```bash
   # Via ADB
   adb logcat | grep Jasper
   ```

## 🔍 Troubleshooting

### Backend Issues

**Server tidak bisa diakses:**
```bash
# Check if server is running
ps aux | grep uvicorn

# Check port availability
sudo netstat -tlnp | grep :8000

# Check firewall
sudo ufw status
sudo ufw allow 8000
```

**Memory/Performance Issues:**
```bash
# Monitor resource usage
htop
free -h
df -h
```

### Android Issues

**Aplikasi tidak bisa connect:**
1. Pastikan VPN aktif dan connected
2. Check BASE_URL di kode aplikasi
3. Verify network permissions
4. Test manual via browser

**Recording tidak berfungsi:**
1. Check microphone permissions
2. Test dengan aplikasi voice recorder lain
3. Restart aplikasi

**Installation gagal:**
1. Enable "Install from Unknown Sources"
2. Check storage space
3. Clear download cache

### VPN Issues

**Tidak bisa connect ke VPN:**
1. Verify credentials ITS
2. Check internet connection
3. Try download ulang file .ovpn
4. Contact IT support ITS

## 📚 API Documentation

Setelah server berjalan, akses dokumentasi lengkap di:
```
http://[SERVER_IP]:8000/docs
```

### Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/transcribe` | Upload audio untuk transkripsi |
| GET | `/docs` | Swagger UI documentation |

## 🚀 Deployment Tips

### Production Considerations

1. **Use HTTPS**: Setup reverse proxy dengan Nginx
2. **Environment Variables**: Jangan hardcode credentials
3. **Logging**: Setup proper logging dan log rotation
4. **Monitoring**: Implement health checks
5. **Backup**: Regular backup konfigurasi

### Security Best Practices

1. **Firewall**: Hanya buka port yang diperlukan
2. **Authentication**: Implement API authentication
3. **Rate Limiting**: Prevent abuse
4. **Input Validation**: Validate semua input

## 📞 Support

Jika mengalami masalah:

1. **Check Logs**: Backend logs di `uvicorn.log`
2. **Verify Network**: Test koneksi VPN dan server
3. **Update Dependencies**: Pastikan semua package up-to-date
4. **Documentation**: Baca dokumentasi API di `/docs`

## 👤 Developer

**Athallah Yoga**

**Tech Stack:**
- **Backend**: FastAPI + Whisper Small Model
- **Android**: Kotlin + Retrofit + ConstraintLayout  
- **Infrastructure**: Ubuntu Server + OpenVPN
- **API**: RESTful with Swagger documentation

**Contact:**
- Email: [athallahyoga99@gmail.com]
- GitHub: [github.com/username]

---

*Last updated: June 2025*
