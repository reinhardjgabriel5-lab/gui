import csv
import os
from models import ArtToy

def simpan_koleksi():
    print("\n=== TAMBAH DATA KOLEKSI ART TOY ===")
    nama_seri = input("Nama Seri   : ").strip()
    karakter = input("Karakter    : ").strip()
    kelangkaan = input("Kelangkaan  : ").strip()
    kondisi = input("Kondisi (Default 'Open Box'): ").strip()
    
    if not kondisi:
        kondisi = "Open Box"
    
    if not nama_seri or not karakter or not kelangkaan:
        print("\n[PERINGATAN] Nama Seri, Karakter, dan Kelangkaan wajib diisi!\n")
        return
    
    koleksi = ArtToy(nama_seri, karakter, kelangkaan, kondisi)
    file_exists = os.path.exists("koleksi.csv")
    
    with open("koleksi.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Nama Seri", "Karakter", "Kelangkaan", "Kondisi"])
        writer.writerow(koleksi.to_list())
        
    print("\n[BERHASIL] Koleksi art toy berhasil ditambahkan.\n")

def main():
    while True:
        print("\n=== MENU TAMBAH KOLEKSI ===")
        print("1. Tambah Koleksi")
        print("0. Kembali / Keluar")
        
        pilihan = input("Pilih menu: ")
        
        if pilihan == "1":
            simpan_koleksi()
        elif pilihan == "0":
            print("Keluar dari menu tambah.")
            break
        else:
            print("Pilihan tidak valid.\n")

if __name__ == "__main__":
    main()