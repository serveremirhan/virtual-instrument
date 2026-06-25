import pygame
import sys
import numpy as np
import math
from button import RadialMenu 

# Pygame ve Ses Motoru Başlatma
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2) # Stereo mikser

WIDTH, HEIGHT = 1920, 1024
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dinamik Akor Sentezleyici")
clock = pygame.time.Clock()
BG_COLOR = (40, 40, 40)

# --- MÜZİK VERİLERİ ---
ROOT_FREQS = [261.63,277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88]
NOTA_ISIMLERI = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

AKOR_ISIMLERI = ["min", "dim", "aug", "maj7", "7", "m7", "sus2", "sus4"]
# Formül: Kök notadan kaç yarım ses uzaklaşılacağı
AKOR_ARALIKLARI = {
    "maj": [0, 4, 7],
    "min": [0, 3, 7],
    "dim": [0, 3, 6],
    "aug": [0, 4, 8],
    "maj7": [0, 4, 7, 11],
    "7": [0, 4, 7, 10],
    "m7": [0, 3, 7, 10],
    "sus2": [0, 2, 7],
    "sus4": [0, 5, 7]
}

class SesMotoru:
    def __init__(self):
        self.kanal_A = pygame.mixer.Channel(0)
        self.kanal_B = pygame.mixer.Channel(1)

        self.aktif_kanal = "A"

    def dinamik_akor_uret(self, kok_frekans, araliklar, ses_seviyesi=10000):
        ornekleme_hizi = 44100
        sure = 1.0
        nokta_sayisi = int(ornekleme_hizi * sure)
        zaman = np.arange(nokta_sayisi) / ornekleme_hizi
        toplam_dalga = np.zeros(nokta_sayisi)

        for n in araliklar:
            # Formül: fn = f0 * 2^(n/12)
            f = kok_frekans * (2 ** (n / 12.0))
            kusursuz_frekans = int(round(f * sure)) / sure
            dalga = np.sin(2 * np.pi * kusursuz_frekans * zaman)
            toplam_dalga += dalga

        toplam_dalga = toplam_dalga / len(araliklar)
        sonuc_dalgasi = (ses_seviyesi * toplam_dalga).astype(np.int16)
        stereo_dalga = np.column_stack((sonuc_dalgasi, sonuc_dalgasi))
        
        return pygame.sndarray.make_sound(stereo_dalga)
    

    def cal(self, kok_frekans, akor_tipi):
        araliklar = AKOR_ARALIKLARI[akor_tipi]
        ses = self.dinamik_akor_uret(kok_frekans, araliklar)

        gecis_suresi = 250

        # --- A/B GEÇİŞ MANTIĞI ---
        if self.aktif_kanal == "A":
            # A kanalını yavaşça sustur
            self.kanal_A.fadeout(gecis_suresi)
            # Yeni sesi B kanalında yavaşça başlat
            self.kanal_B.play(ses, loops=-1, fade_ms=gecis_suresi)
            # Artık aktif kanalımız B oldu
            self.aktif_kanal = "B"
            
        else: # Eğer aktif kanal B ise
            # B kanalını yavaşça sustur
            self.kanal_B.fadeout(gecis_suresi)
            # Yeni sesi A kanalında yavaşça başlat
            self.kanal_A.play(ses, loops=-1, fade_ms=gecis_suresi)
            # Artık aktif kanalımız A oldu
            self.aktif_kanal = "A"

def main():
    # Menüleri doğrudan ana şablondan üretiyoruz!
    menu_sol = RadialMenu((WIDTH // 3, HEIGHT // 2), 60, 250, 12, labels=NOTA_ISIMLERI)
    menu_sag = RadialMenu((2 * WIDTH // 3, HEIGHT // 2), 60, 250, 8, labels=AKOR_ISIMLERI)
    
    ses_motoru = SesMotoru()
    
    # Sistemin hafızası (Başlangıçta hiçbir nota seçili değil, varsayılan akor Majör)
    secili_nota_idx = -1
    secili_akor_tipi = "maj"

    running = True
    while running:
        screen.fill(BG_COLOR)
        mx, my = pygame.mouse.get_pos()
        
        hovered_sol = menu_sol.get_hovered_segment(mx, my)
        hovered_sag = menu_sag.get_hovered_segment(mx, my)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                
                # SOL MENÜYE TIKLANIRSA (Notayı değiştir ve çal)
                if hovered_sol != -1:
                    secili_nota_idx = hovered_sol
                    secili_akor_tipi = "maj" # İsteğine göre: Sol menüye tıklayınca varsayılan olarak maj çalar
                    ses_motoru.cal(ROOT_FREQS[secili_nota_idx], secili_akor_tipi)
                    print(f"Çalıyor: {NOTA_ISIMLERI[secili_nota_idx]} {secili_akor_tipi}")

                # SAĞ MENÜYE TIKLANIRSA (Akor tipini değiştir ve eğer seçili nota varsa çal)
                elif hovered_sag != -1:
                    secili_akor_tipi = AKOR_ISIMLERI[hovered_sag]
                    if secili_nota_idx != -1: # Eğer önceden bir nota seçildiyse
                        ses_motoru.cal(ROOT_FREQS[secili_nota_idx], secili_akor_tipi)
                        print(f"Çalıyor: {NOTA_ISIMLERI[secili_nota_idx]} {secili_akor_tipi}")

        # Çizim İşlemleri
        transparent_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        menu_sol.draw(transparent_surface, hovered_sol)
        menu_sag.draw(transparent_surface, hovered_sag)
        
        screen.blit(transparent_surface, (0, 0))
        
        # Kullanıcının ne seçtiğini ekranda görebilmesi için basit bir UI metni
        if secili_nota_idx != -1:
            font = pygame.font.SysFont(None, 48)
            text = font.render(f"Aktif Akor: {NOTA_ISIMLERI[secili_nota_idx]} {secili_akor_tipi}", True, (255, 200, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()