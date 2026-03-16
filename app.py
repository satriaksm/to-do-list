"""
CLI To-Do List Application
--------------------------
Aplikasi manajemen tugas berbasis Command Line Interface (CLI).
Modul ini menangani operasi CRUD (Create, Read, Update, Delete) untuk daftar tugas
dan menyimpannya secara persisten ke dalam file JSON.

Ditulis dengan gaya Pythonic, menggunakan Type Hinting, dan kompatibel dengan Python 3.10+.
"""

import json
import os

# Nama file default untuk penyimpanan database JSON
FILE_NAME = "task.json"


def clear_screen() -> None:
    """
    Membersihkan layar terminal untuk meningkatkan kenyamanan UI/UX.
    Menggunakan perintah OS yang sesuai (cls untuk Windows, clear untuk Unix/Linux).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def load_task() -> list:
    """
    Memuat daftar tugas dari file JSON.

    Returns:
        list: Daftar tugas berupa list of dictionaries. Mengembalikan list kosong []
              jika file tidak ditemukan atau isinya korup.
    """
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Peringatan: File data rusak. Memulai dengan daftar kosong.")
        return []


def save_task(tasks: list, filename: str = FILE_NAME) -> None:
    """
    Menyimpan daftar tugas ke dalam file JSON secara persisten.

    Args:
        tasks (list): Daftar tugas yang akan disimpan.
        filename (str): Nama file tujuan. Default menggunakan FILE_NAME.
    """
    with open(filename, 'w') as file:
        json.dump(tasks, file, indent=4)


def print_task_list(tasks: list) -> bool:
    """
    Fungsi helper untuk mencetak daftar tugas singkat beserta index-nya.

    Args:
        tasks (list): Daftar tugas yang akan dicetak.

    Returns:
        bool: True jika list tidak kosong, False jika list kosong.
    """
    if not tasks:
        print("Belum ada tugas!")
        return False

    for index, task in enumerate(tasks, start=1):
        status = "[x]" if task["done"] else "[ ]"
        print(f"{index}. {status} {task['title']}")
    return True


def detail_task(task: dict) -> None:
    """
    Menampilkan detail lengkap dari satu tugas spesifik.

    Args:
        task (dict): Object dictionary dari satu tugas.
    """
    clear_screen()
    print("\n" + "=" * 30)
    print("        DETAIL TUGAS")
    print("=" * 30)
    print(f"Judul     : {task['title']}")
    print(f"Status    : {'Selesai [x]' if task['done'] else 'Belum Selesai [ ]'}")

    # Menggunakan .get() untuk fallback data legacy yang mungkin tidak punya key ini
    print(f"Deskripsi : {task.get('description', '-')}")
    print(f"Estimasi  : {task.get('estimate', '-')}")
    print("=" * 30)
    input("Tekan Enter untuk kembali...")


def display_tasks(tasks: list) -> None:
    """
    Menampilkan sub-menu interaktif untuk melihat daftar tugas dan mengakses detailnya.
    Fungsi akan mengunci layar (loop) sampai user memilih untuk kembali (0).

    Args:
        tasks (list): Daftar tugas saat ini.
    """
    while True:
        clear_screen()
        print("\n--- Daftar To-Do List ---")

        if not print_task_list(tasks):
            input("\nTekan Enter untuk kembali...")
            return

        print("-------------------------")
        print("[0] Kembali ke Menu Utama")

        pilihan = input("\nPilih nomor tugas untuk lihat detail (atau 0): ")

        if pilihan == "0":
            break

        try:
            task_index = int(pilihan) - 1
            if 0 <= task_index < len(tasks):
                detail_task(tasks[task_index])
            else:
                input("Nomor tugas tidak valid! Tekan Enter untuk mengulang...")
        except ValueError:
            input("Harap masukkan angka yang valid! Tekan Enter untuk mengulang...")


def add_task(tasks: list, filename: str = FILE_NAME) -> None:
    """
    Meminta input user untuk membuat tugas baru dan menyimpannya ke database.

    Args:
        tasks (list): Referensi daftar tugas saat ini (mutated in place).
        filename (str): Target file JSON untuk penyimpanan.
    """
    clear_screen()
    print("\n--- Tambah Tugas Baru ---")

    # Loop validasi untuk mencegah judul kosong
    while True:
        title = input("Masukkan judul tugas: ").strip()
        if title:
            break
        print("Judul tidak boleh kosong!\n")

    description = input("Deskripsikan tugas: ").strip()
    estimate = input("Estimasi waktu selesai: ").strip()

    new_task = {
        "title": title,
        "description": description if description else "-",
        "estimate": estimate if estimate else "-",
        "done": False,
    }

    tasks.append(new_task)
    save_task(tasks, filename)
    input("\nTugas berhasil ditambahkan! Tekan Enter untuk kembali...")


def complete_task(tasks: list, filename: str = FILE_NAME) -> None:
    """
    Menandai tugas spesifik sebagai selesai (done = True) berdasarkan input index user.

    Args:
        tasks (list): Referensi daftar tugas saat ini.
        filename (str): Target file JSON untuk penyimpanan.
    """
    clear_screen()
    print("\n--- Tandai Tugas Selesai ---")

    if not print_task_list(tasks):
        input("\nTekan Enter untuk kembali...")
        return

    try:
        task_num = int(input("\nNomor tugas yang sudah selesai: "))
        index = task_num - 1

        if 0 <= index < len(tasks):
            if tasks[index]["done"]:
                print("Tugas ini memang sudah selesai.")
            else:
                tasks[index]["done"] = True
                save_task(tasks, filename)
                print("Tugas berhasil ditandai selesai!")
        else:
            print("Nomor tugas tidak valid!")
    except ValueError:
        print("Tolong masukkan angka yang valid!")

    input("Tekan Enter untuk kembali...")


def delete_task(tasks: list, filename: str = FILE_NAME) -> None:
    """
    Menghapus satu tugas dari daftar berdasarkan input index user.

    Args:
        tasks (list): Referensi daftar tugas saat ini.
        filename (str): Target file JSON untuk penyimpanan.
    """
    clear_screen()
    print("\n--- Hapus Tugas ---")

    if not print_task_list(tasks):
        input("\nTekan Enter untuk kembali...")
        return

    try:
        task_num = int(input("\nNomor tugas yang ingin dihapus: "))
        index = task_num - 1

        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            save_task(tasks, filename)
            print(f"Tugas '{removed['title']}' berhasil dihapus!")
        else:
            print("Nomor tugas tidak valid!")
    except ValueError:
        print("Tolong masukkan angka yang valid!")

    input("Tekan Enter untuk kembali...")


def main() -> None:
    """
    Entry point utama dari aplikasi.
    Menjalankan main loop untuk merender antarmuka Menu dan menangani routing menu.
    """
    tasks = load_task()

    while True:
        clear_screen()
        print("\n=== PREVIEW TUGAS ===")
        if not tasks:
            print("Belum ada tugas! Silakan tambah tugas baru.")
        else:
            for task in tasks:
                status = "[x]" if task["done"] else "[ ]"
                print(f"{status} {task['title']}")
        print("-------------------------\n")

        print("=== Menu To-do List ===")
        print("[1] Lihat Daftar & Detail")
        print("[2] Tambah Tugas")
        print("[3] Tandai Selesai")
        print("[4] Hapus Tugas")
        print("[5] Keluar")

        pilihan = input("\nPilih menu (1-5): ").strip()

        match pilihan:
            case "1":
                display_tasks(tasks)
            case "2":
                add_task(tasks)
            case "3":
                complete_task(tasks)
            case "4":
                delete_task(tasks)
            case "5":
                clear_screen()
                print("Terima kasih! Sampai Jumpa!")
                break
            case _:
                input("Pilihan tidak valid! Tekan Enter untuk mengulang...")


# Block ini memastikan main() hanya berjalan jika script dieksekusi langsung
if __name__ == "__main__":
    main()