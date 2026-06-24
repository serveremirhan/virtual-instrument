from button import RadialMenu

class NotesMenu(RadialMenu):
    def __init__(self, width, height):
        # 9 dilimli, ekranın sağ tarafında
        super().__init__(center=(2 * width // 3, height // 2), inner_radius=60, outer_radius=250, num_segments=9)

    def islem_yap(self, secilen_buton):
        """Sağ menünün butonlarına tıklandığında çalışacak kodlar"""
        if secilen_buton == 0:
            print("SAĞ MENÜ - 1. Buton: Can İksiri İçildi! (+50 HP)")
        elif secilen_buton == 1:
            print("SAĞ MENÜ - 2. Buton: Mana İksiri İçildi! (+30 Mana)")
        elif secilen_buton == 2:
            print("SAĞ MENÜ - 3. Buton: Harita Açıldı!")
        else:
            print(f"SAĞ MENÜ - {secilen_buton + 1}. Buton İşlevi Henüz Eklenmedi.")