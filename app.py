import json
import os

# CONSTANT: Biasanya ditulis dengan huruf kapital semua di Python (PEP 8)
FILE_NAME = "task.json"


def clear_screen():
    # Fungsi tambahan untuk membersihkan layar terminal
    # 'cls' untuk Windows, 'clear' untuk Mac/Linux
    os.system('cls' if os.name == 'nt' else 'clear')


def load_task() -> list:  # '-> list' adalah Type Hint bahwa fungsi ini mengembalikan Array/List
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        # Jika file ada tapi isinya corrupt/bukan JSON valid, kembalikan list kosong
        print("Peringatan: File data rusak. Memulai dengan daftar kosong.")
        return []


def save_task(tasks: list):  # ': list' adalah Type Hint untuk parameter
    with open(FILE_NAME, 'w') as file:
        json.dump(tasks, file, indent=4)


# --- FUNGSI HELPER BARU (Penerapan DRY) ---
def print_task_list(tasks: list) -> bool:
    """Mencetak daftar tugas. Mengembalikan True jika ada tugas, False jika kosong."""
    if not tasks:
        print("Belum ada tugas!")
        return False

    for index, task in enumerate(tasks, start=1):
        status = "[x]" if task["done"] else "[ ]"
        print(f"{index}. {status} {task['title']}")
    return True


# ------------------------------------------

def detail_task(task: dict):
    clear_screen()
    print("\n" + "=" * 30)
    print("        DETAIL TUGAS")
    print("=" * 30)
    print(f"Judul     : {task['title']}")
    print(f"Status    : {'Selesai [x]' if task['done'] else 'Belum Selesai [ ]'}")
    print(f"Deskripsi : {task.get('description', '-')}")
    print(f"Estimasi  : {task.get('estimate', '-')}")
    print("=" * 30)
    input("Tekan Enter untuk kembali...")


def display_tasks(tasks: list):
    while True:
        clear_screen()
        print("\n--- Daftar To-Do List ---")

        # Panggil helper. Jika kosong (False), langsung hentikan loop
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


def add_task(tasks: list):
    clear_screen()
    print("\n--- Tambah Tugas Baru ---")

    # Validasi input agar judul tidak boleh kosong
    while True:
        title = input("Masukkan judul tugas: ").strip()  # .strip() mirip trim() di PHP/JS
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
    save_task(tasks)
    input("\nTugas berhasil ditambahkan! Tekan Enter untuk kembali...")


def complete_task(tasks: list):
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
                save_task(tasks)
                print("Tugas berhasil ditandai selesai!")
        else:
            print("Nomor tugas tidak valid!")
    except ValueError:
        print("Tolong masukkan angka yang valid!")

    input("Tekan Enter untuk kembali...")


def delete_task(tasks: list):
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
            save_task(tasks)
            print(f"Tugas '{removed['title']}' berhasil dihapus!")
        else:
            print("Nomor tugas tidak valid!")
    except ValueError:
        print("Tolong masukkan angka yang valid!")

    input("Tekan Enter untuk kembali...")


def main():
    tasks = load_task()

    while True:
        clear_screen()
        print("\n=== PREVIEW TUGAS ===")
        # Panggil helper tanpa index nomor (karena ini cuma preview)
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

        # MENGGUNAKAN STRING untuk mencegah ValueError jika menekan Enter
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


if __name__ == "__main__":
    main()