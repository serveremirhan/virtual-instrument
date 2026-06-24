from button import RadialMenu

class ChordsMenu(RadialMenu):
    def __init__(self, width, height):
        # 7 dilimli, ekranın sol tarafında
        super().__init__(center=(width // 3, height // 2), inner_radius=60, outer_radius=250, num_segments=7)

    def islem_yap(self, secilen_buton):
        """Sol menünün butonlarına tıklandığında çalışacak kodlar"""
        if secilen_buton == 0:
            print("SOL MENÜ - 1. Buton: Kılıç Saldırısı!")
        elif secilen_buton == 1:
            print("SOL MENÜ - 2. Buton: Kalkan Savunması!")
        elif secilen_buton == 2:
            print("SOL MENÜ - 3. Buton: Büyü At!")
        else:
            print(f"SOL MENÜ - {secilen_buton + 1}. Buton İşlevi Henüz Eklenmedi.")