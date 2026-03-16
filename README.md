# CLI To-Do List (Python)

Sebuah aplikasi manajemen tugas (*To-Do List*) sederhana dan interaktif berbasis antarmuka baris perintah (CLI). Proyek ini dibangun menggunakan Python murni dengan arsitektur yang modular, *type-hinting*, dan persintensi data menggunakan JSON.

## 🚀 Fitur Utama

- **Dashboard Preview:** Melihat ringkasan cepat semua tugas langsung di layar utama.
- **Manajemen Tugas (CRUD):** - Menambahkan tugas (Judul, Deskripsi, Estimasi Waktu).
  - Melihat detail spesifik setiap tugas.
  - Menandai tugas sebagai selesai `[x]`.
  - Menghapus tugas.
- **Penyimpanan Persisten:** Data otomatis tersimpan ke dalam `task.json` sehingga tidak hilang saat aplikasi ditutup (mirip cara kerja *database* sederhana).
- **Validasi & Error Handling:** Sistem menolak input kosong dan menangani kesalahan *typing* pengguna (seperti memasukkan huruf saat diminta angka) tanpa mengalami *crash*.
- **Unit Tested:** Dilengkapi dengan *test case* menggunakan `pytest` untuk memastikan stabilitas logika bisnis dan simulasi *input user*.

## 🛠️ Prasyarat (Prerequisites)

- **Python 3.10** atau lebih baru (karena menggunakan fitur *Structural Pattern Matching* / `match-case`).
- (Opsional) `pytest` untuk menjalankan *automated testing*.

## ⚙️ Cara Menjalankan Aplikasi

1. *Clone* atau unduh *repository* ini ke komputer lokal Anda.
2. Buka terminal (atau IDE seperti PyCharm/VSCode) dan arahkan ke folder proyek ini.
3. Jalankan perintah berikut:

   ```bash
   python app.py
   
4. Gunakan angka (1-5) pada keyboard lalu tekan Enter untuk bernavigasi di dalam menu.

## 🧪 Cara Menjalankan Unit Test
Aplikasi ini menggunakan pytest dan fitur monkeypatch untuk menyimulasikan input pengguna pada CLI tanpa harus menyentuh file production database (task.json).

1. Pastikan pytest sudah terinstal di environment Anda:

    ```Bash
    pip install pytest

2. Jalankan perintah testing:

    ```Bash
    pytest test_app.py -v
3. Terminal akan menampilkan laporan hijau jika semua skenario logika dan pencegahan error berhasil dilewati secara otomatis.

## 💡 Konsep Pembelajaran (Dari PHP/JS ke Python)
Proyek ini dibangun dengan menerapkan beberapa konsep esensial Python bagi developer yang beralih dari PHP/JavaScript:
- Penggunaan List (mirip Array terindeks) dan Dictionary (mirip Object/Associative Array).
- Pembacaan & penulisan File Handling menggunakan block with open(...) yang otomatis menangani penutupan file.
- Penggunaan modul bawaan json (json.dump / json.load) ekuivalen dengan JSON.stringify dan JSON.parse.
- Dependency Injection sederhana pada parameter fungsi untuk kemudahan mocking saat testing.
- Penggunaan Type Hinting (-> list, : dict) ala TypeScript untuk integrasi IDE yang lebih baik.