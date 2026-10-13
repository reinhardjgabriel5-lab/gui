import subprocess

def buka_tambah_koleksi():
    subprocess.run(["python", "tambah_koleksi.py"])

def buka_tampil_koleksi():
    subprocess.run(["python", "tampil_koleksi.py"])

def menu_utama():
    while True:
        print("\n" + "=" * 4)
        print(" KOLEKSI ART TOY & BLIND BOX ".center(40, "="))
        print("=" * 40)
        print("1. Tambah Koleksi")
        print("2. Tampilkan Koleksi")
        print("0. Keluar")
        print("=" * 40)
        
        pilihan = input("Pilih menu: ")
        
        if pilihan == "1":
            buka_tambah_koleksi()
        elif pilihan == "2":
            buka_tampil_koleksi()
        elif pilihan == "0":
            print("Terima kasih.")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    menu_utama()