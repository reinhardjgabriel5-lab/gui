import csv
import os
from models import ArtToy

def muat_data():
    daftar_koleksi = []
    if not os.path.exists("koleksi.csv"):
        print("File koleksi.csv tidak ditemukan.")
        return daftar_koleksi
        
    with open("koleksi.csv", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # Lewati header
        for row in reader:
            koleksi = ArtToy(
                nama_seri=row[0],
                karakter=row[1],
                kelangkaan=row[2],
                kondisi=row[3]
            )
            daftar_koleksi.append(koleksi)
    return daftar_koleksi

def tampilkan_koleksi():
    daftar_koleksi = muat_data()
    if not daftar_koleksi:
        print("Tidak ada data koleksi.")
        return
        
    print("\n=== DAFTAR KOLEKSI ART TOY ===\n")
    print(f"{'Nama Seri':25}{'Karakter':20}{'Kelangkaan':15}{'Kondisi'}")
    print("-" * 75)
    for koleksi in daftar_koleksi:
        print(
            f"{koleksi.nama_seri:25}"
            f"{koleksi.karakter:20}"
            f"{koleksi.kelangkaan:15}"
            f"{koleksi.kondisi}"
        )
    print("-" * 75)
    print(f"Total Koleksi: {len(daftar_koleksi)}")

def main():
    while True:
        print("\n=== MENU ===")
        print("1. Tampilkan Koleksi")
        print("2. Refresh Data")
        print("0. Keluar")
        
        pilihan = input("Pilih: ")
        
        if pilihan == "1":
            tampilkan_koleksi()
        elif pilihan == "2":
            print("Data dimuat ulang...")
            tampilkan_koleksi()
        elif pilihan == "0":
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()