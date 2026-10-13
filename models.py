class ArtToy:
    def __init__(self, nama_seri, karakter, kelangkaan, kondisi="Open Box"):
        self.nama_seri = nama_seri
        self.karakter = karakter
        self.kelangkaan = kelangkaan
        self.kondisi = kondisi

    def to_list(self):
        return [self.nama_seri, self.karakter, self.kelangkaan, self.kondisi]

    def __str__(self):
        return f"{self.karakter} - Seri {self.nama_seri} ({self.kelangkaan}) - {self.kondisi}"