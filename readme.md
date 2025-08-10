# DrowsinessGuard: Sistem Peringatan Kantuk Berbasis Computer Vision

![Demo Aplikasi](https://i.imgur.com/8aL0x2V.gif) DrowsinessGuard adalah sebuah aplikasi desktop cerdas yang menggunakan webcam untuk memonitor wajah pengemudi atau pengguna komputer secara *real-time* dan mendeteksi tanda-tanda kantuk untuk mencegah kecelakaan.

## ✨ Fitur Utama

- **Deteksi Wajah & Mata Real-Time**: Menggunakan MediaPipe Face Mesh untuk pelacakan 468 titik landmark wajah dengan akurasi tinggi.
- **Analisis Tingkat Keterbukaan Mata**: Menghitung metrik **Eye Aspect Ratio (EAR)** untuk mengukur seberapa terbuka mata pengguna.
- **Sistem Peringatan Cerdas**: Memicu alarm suara jika mata pengguna terdeteksi tertutup lebih lama dari durasi yang ditentukan (misalnya, > 1.5 detik).
- **Visualisasi**: Menampilkan *feedback* visual langsung di layar, termasuk landmark mata dan nilai EAR saat ini.

## 🛠️ Tumpukan Teknologi (Tech Stack)

- **Bahasa**: Python 3.x
- **Library Inti**:
  - **OpenCV**: Untuk menangkap dan memproses frame video dari webcam.
  - **MediaPipe**: Untuk deteksi wajah dan *facial landmarks* yang efisien.
  - **NumPy & SciPy**: Untuk kalkulasi numerik pada metrik EAR.
  - **Playsound**: Untuk memutar file audio sebagai alarm.

## 🚀 Cara Menjalankan Aplikasi

### 1. Prasyarat

- Python 3.7+
- Webcam yang berfungsi

### 2. Setup Lingkungan

1.  **Clone repositori ini atau unduh file proyek.**

2.  **Buat dan aktifkan *virtual environment* (sangat direkomendasikan):**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS / Linux
    source venv/bin/activate
    ```

3.  **Instal semua dependensi yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Siapkan file alarm:**
    Pastikan Anda memiliki file suara bernama `alarm.wav` di dalam direktori proyek.

### 3. Eksekusi Program

Jalankan skrip utama dari terminal Anda:
```bash
python drowsiness_guard.py
```
Aplikasi akan membuka jendela yang menampilkan feed dari webcam Anda. Arahkan wajah Anda ke kamera. Tekan tombol **'q'** kapan saja untuk keluar.

### 4. Kalibrasi (Penting!)

Setiap orang memiliki bentuk mata yang unik, dan kondisi pencahayaan dapat bervariasi. Anda mungkin perlu menyesuaikan nilai `EAR_THRESHOLD`.

- **Cara Kalibrasi**: Jalankan program dan perhatikan nilai `EAR` yang ditampilkan di pojok kanan atas saat mata Anda terbuka normal dan saat Anda sengaja menutupnya.
- **Ubah Nilai**: Buka file `drowsiness_guard.py` dan sesuaikan nilai konstanta `EAR_THRESHOLD` (baris 9).
  - Jika alarm terlalu sensitif (sering berbunyi padahal tidak mengantuk), **naikkan** nilainya sedikit (misal: dari `0.22` ke `0.24`).
  - Jika alarm tidak berbunyi saat Anda benar-benar menutup mata, **turunkan** nilainya (misal: dari `0.22` ke `0.20`).
- Anda juga bisa mengubah `DROWSY_FRAMES_THRESHOLD` untuk mengatur durasi mata harus tertutup sebelum alarm berbunyi.

## 📈 Pengembangan Lebih Lanjut

- Deteksi Menguap (*Yawn Detection*)
- Analisis Pose Kepala (*Head Pose Analysis*)
- GUI dengan Tkinter atau PyQt
- *Logging* data kantuk