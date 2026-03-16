import json
import os

file_name = "task.json"

def load_task() :
    if not os.path.exists(file_name) : #Cek apakah json ada
        return [] #return kosong

    with open(file_name, 'r') as file :
        return json.load(file) #ubah string json ke list

def save_task(tasks) :
    with open(file_name, 'w') as file : #tulis file_name dengan variabel tasks (ditimpa)
        json.dump(tasks, file, indent=4)


def detail_task(task):
    # Parameter 'task' di sini hanya menerima 1 Object (Dictionary), bukan seluruh list.
    print("\n" + "=" * 30)
    print("        DETAIL TUGAS")
    print("=" * 30)
    print(f"Judul     : {task['title']}")

    # Ternary operator untuk status
    print(f"Status    : {'Selesai [x]' if task['done'] else 'Belum Selesai [ ]'}")

    # Kita gunakan .get() agar aman. Jika versi data json lama tidak punya key 'description',
    # Python tidak akan error, tapi mereturn default value "-" (seperti fitur nullish coalescing '??' di PHP)
    print(f"Deskripsi : {task.get('description', '-')}")
    print(f"Estimasi  : {task.get('estimate', '-')}")
    print("=" * 30)

    input("Tekan Enter untuk kembali...")  # Menahan layar agar user sempat membaca


def display_tasks(tasks):
    while True:
        print("\n--- Daftar To-Do List ---")
        if not tasks:
            print("Belum ada tugas!")
            return  # Kembali ke menu utama (keluar dari display_tasks)

        for index, task in enumerate(tasks, start=1):
            status = "[x]" if task["done"] else "[ ]"
            print(f"{index}. {status} {task['title']}")

        print("-------------------------")
        print("[0] Kembali ke Menu Utama")

        pilihan = input("Pilih nomor tugas untuk lihat detail: ")

        if pilihan == "0":
            break  # Hentikan sub-menu, kembali ke menu utama

        try:
            # Konversi input ke integer untuk mencari index array
            task_index = int(pilihan) - 1

            # Validasi apakah index ada di dalam array
            if 0 <= task_index < len(tasks):
                # Kirim SATU object task ke fungsi detail_task
                detail_task(tasks[task_index])
            else:
                print("Nomor tugas tidak valid!")
        except ValueError:
            print("Harap masukkan angka yang valid!")

def add_task(tasks) :
    title = input("Masukkan tugas baru: ") #input untuk user memasukkan task
    description = input("Deskripsikan tugas baru: ")
    estimate = input("Masukkan estimasi waktu selesai tugas baru: ")
    new_task = {
        "title": title,
        "description": description,
        "estimate": estimate,
        "done": False,
    }
    tasks.append(new_task) # array push, untuk memasukkan data ke array
    save_task(tasks)
    print("Tugas berhasil ditambahkan!")

def complete_task(tasks) :
    for index, task in enumerate(tasks, start=1):
        status = "[x]" if task["done"] else "[ ]"
        print(f"{index}. {status} {task['title']}")
    try :
        task_num = int(input("Nomor tugas yang sudah selesai: ")) #input yang dibuat wajib integer
        index = task_num - 1 # karena array dimulai dari 0 jadi kurangi 1

        if 0 <= index < len(tasks) :
            tasks[index]["done"] = True
            save_task(tasks)
            print("Tugas ditandai selesai.!")
        else :
            print("Nomor tugas tidak valid!")
    except ValueError :
        print("Tolong masukkan angka yang valid!")

def delete_task(tasks) :
    for index, task in enumerate(tasks, start=1):
        status = "[x]" if task["done"] else "[ ]"
        print(f"{index}. {status} {task['title']}")
    try :
        task_num = int(input("Nomor tugas yang selesai: "))
        index = task_num - 1

        if 0 <= index < len(tasks) :
            removed = tasks.pop(index) #pop() menghapus dari list
            save_task(tasks)
            print(f"Tugas '{removed['title']}' berhasil dihapus!")
        else :
            print("Nomor tugas tidak valid!")
    except ValueError :
        print("Tolong masukkan angka yang valid!")

def main() :
    tasks = load_task() #muat data

    while True : # infinite loop untuk run aplikasi
        # --- PREVIEW DASHBOARD ---
        print("\n=== PREVIEW TUGAS ===")
        if not tasks:
            print("Belum ada tugas! Silakan tambah tugas baru.")
            # HAPUS 'return' dari sini agar aplikasi tidak tertutup
        else:
            for task in tasks:
                status = "[x]" if task["done"] else "[ ]"
                print(f"{status} {task['title']}")
        print("-------------------------\n")

        print("\n=== Menu To-do List ===\n")
        print("[1] Lihat Tugas")
        print("[2] Tambah Tugas")
        print("[3] Tandai Selesai")
        print("[4] Hapus Tugas")
        print("[5] Keluar")

        pilihan = int(input("Pilih menu (1-5): "))

        # if pilihan == 1 :
        #     display_tasks(tasks)
        # elif pilihan == 2 :
        #     add_task(tasks)
        # elif pilihan == 3 :
        #     complete_task(tasks)
        # elif pilihan == 4 :
        #     delete_task(tasks)
        # elif pilihan == 5 :
        #     print("Sampai Jumpa!")
        #     break
        # else :
        #     print("Pilihan tidak valid!")

        match pilihan :
            case 1 :
                display_tasks(tasks)
            case 2 :
                add_task(tasks)
            case 3 :
                complete_task(tasks)
            case 4 :
                delete_task(tasks)
            case 5 :
                print("Sampai Jumpa!")
                break
            case _ :
                print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
