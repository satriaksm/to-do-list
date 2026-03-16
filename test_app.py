import pytest
import os
import json
from app import add_task, load_task, complete_task, delete_task

# Kita buat nama file khusus untuk testing (database bohongan)
TEST_FILE = "test_task.json"


# --- FIXTURE (Mirip beforeEach & afterEach di Jest/PHPUnit) ---
@pytest.fixture
def setup_database():
    """Fixture ini berjalan sebelum dan sesudah setiap test."""
    # BEFORE EACH: Pastikan file test bersih sebelum test dimulai
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

    # Kata kunci 'yield' memisahkan logika 'before' dan 'after'
    yield

    # AFTER EACH: Hapus file test setelah test selesai agar tidak nyampah
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


# --- TEST CASE ---
# Parameter 'monkeypatch' adalah bawaan pytest.
# Parameter 'setup_database' memanggil fixture di atas.
def test_add_task_berhasil(monkeypatch, setup_database):
    # 1. ARRANGE (Persiapan Data)
    tasks_awal = []

    # Kita siapkan daftar ketikan yang akan diketik oleh "User Hantu" (Automation)
    # Urutannya: Judul -> Deskripsi -> Estimasi -> Enter (untuk kembali)
    simulasi_ketikan = iter(["Belajar Pytest", "Membuat unit test CLI", "1 Jam", ""])

    # Kita bajak fungsi 'input' bawaan Python.
    # Setiap kali aplikasi meminta input(), otomatis ambil dari simulasi_ketikan
    monkeypatch.setattr('builtins.input', lambda prompt="": next(simulasi_ketikan))

    # Kita bajak juga clear_screen agar terminal tidak berkedip-kedip saat di-test
    monkeypatch.setattr('app.clear_screen', lambda: None)

    # 2. ACT (Jalankan Fungsi)
    # Kita panggil add_task, arahkan ke TEST_FILE
    add_task(tasks_awal, filename=TEST_FILE)

    # 3. ASSERT (Verifikasi Hasil)
    # Cek apakah data masuk ke dalam List di RAM
    assert len(tasks_awal) == 1
    assert tasks_awal[0]["title"] == "Belajar Pytest"
    assert tasks_awal[0]["description"] == "Membuat unit test CLI"
    assert tasks_awal[0]["done"] == False

    # Cek apakah data benar-benar tersimpan ke file JSON (Database bohongan)
    assert os.path.exists(TEST_FILE) == True

    with open(TEST_FILE, 'r') as file:
        saved_data = json.load(file)
        assert len(saved_data) == 1
        assert saved_data[0]["title"] == "Belajar Pytest"


def test_add_task_judul_kosong_lalu_berhasil(monkeypatch, setup_database, capsys):
    # 1. ARRANGE
    tasks_awal = []

    # Skenario User Iseng:
    # 1. Tekan Enter doang ("") -> Harus ditolak
    # 2. Ketik spasi doang ("   ") -> Harus ditolak karena ada .strip()
    # 3. Ketik "Tugas Valid" -> Harus diterima dan lanjut
    # 4. Ketik "-" untuk deskripsi
    # 5. Ketik "-" untuk estimasi
    # 6. Tekan Enter ("") untuk kembali ke menu
    simulasi_ketikan = iter(["", "   ", "Tugas Valid", "-", "-", ""])

    monkeypatch.setattr('builtins.input', lambda prompt="": next(simulasi_ketikan))
    monkeypatch.setattr('app.clear_screen', lambda: None)

    # 2. ACT
    add_task(tasks_awal, filename=TEST_FILE)

    # 3. ASSERT - Validasi Data
    assert len(tasks_awal) == 1
    assert tasks_awal[0]["title"] == "Tugas Valid"  # Pastikan yang tersimpan adalah input yang ke-3

    # 4. ASSERT - Validasi Pesan Error di Terminal
    # capsys.readouterr() akan mengambil semua teks yang di-print() selama fungsi berjalan
    captured = capsys.readouterr()

    # Kita cek apakah pesan peringatan benar-benar dicetak ke layar
    # Karena user gagal 2 kali, pastikan pesannya ada di dalam output terminal
    assert "Judul tidak boleh kosong!" in captured.out


# ==========================================
# TEST CASE: TANDAI SELESAI (COMPLETE TASK)
# ==========================================

def test_complete_task_berhasil(monkeypatch, setup_database):
    # 1. ARRANGE (Siapkan Data Awal)
    # Analogi PHP/JS: Kita membuat "Mock Database" berupa Array of Objects di memori
    tasks_awal = [
        {"title": "Mandi", "description": "-", "estimate": "-", "done": False},
        {"title": "Ngoding", "description": "-", "estimate": "-", "done": False}
    ]

    # Skenario: User mengetik angka "2" (memilih Ngoding), lalu Enter ("") untuk kembali ke menu
    simulasi_ketikan = iter(["2", ""])
    monkeypatch.setattr('builtins.input', lambda prompt="": next(simulasi_ketikan))
    monkeypatch.setattr('app.clear_screen', lambda: None)

    # 2. ACT (Jalankan Fungsi)
    complete_task(tasks_awal, filename=TEST_FILE)

    # 3. ASSERT (Verifikasi)
    assert tasks_awal[0]["done"] == False  # Tugas 1 ("Mandi") harusnya tetap False
    assert tasks_awal[1]["done"] == True  # Tugas 2 ("Ngoding") harusnya berubah True!


def test_complete_task_input_huruf_harus_ditolak(monkeypatch, setup_database, capsys):
    # Skenario Unhappy Path: User iseng memasukkan huruf "A" saat diminta nomor tugas
    tasks_awal = [{"title": "Belajar Pytest", "done": False}]

    simulasi_ketikan = iter(["A", ""])  # "A" lalu Enter
    monkeypatch.setattr('builtins.input', lambda prompt="": next(simulasi_ketikan))
    monkeypatch.setattr('app.clear_screen', lambda: None)

    complete_task(tasks_awal, filename=TEST_FILE)

    captured = capsys.readouterr()

    # Verifikasi bahwa pesan error ValueError ("Tolong masukkan angka yang valid!") muncul
    assert "Tolong masukkan angka yang valid!" in captured.out

    # Verifikasi bahwa data tidak berubah sama sekali (tetap False)
    assert tasks_awal[0]["done"] == False


# ==========================================
# TEST CASE: HAPUS TUGAS (DELETE TASK)
# ==========================================

def test_delete_task_berhasil(monkeypatch, setup_database):
    # 1. ARRANGE
    tasks_awal = [
        {"title": "Tugas 1", "done": False},
        {"title": "Tugas 2", "done": False},
        {"title": "Tugas 3", "done": False}
    ]

    # Skenario: User ingin menghapus tugas nomor "1" (Tugas 1), lalu Enter
    simulasi_ketikan = iter(["1", ""])
    monkeypatch.setattr('builtins.input', lambda prompt="": next(simulasi_ketikan))
    monkeypatch.setattr('app.clear_screen', lambda: None)

    # 2. ACT
    delete_task(tasks_awal, filename=TEST_FILE)

    # 3. ASSERT
    # Karena awalnya ada 3 tugas, setelah dihapus 1 harusnya sisa 2 (len == 2)
    assert len(tasks_awal) == 2

    # Karena 'Tugas 1' dihapus (di-pop dari index 0),
    # maka 'Tugas 2' sekarang otomatis maju menjadi index 0. Ini sifat list.pop() di Python!
    assert tasks_awal[0]["title"] == "Tugas 2"
    assert tasks_awal[1]["title"] == "Tugas 3"