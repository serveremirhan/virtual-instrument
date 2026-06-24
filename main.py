import pygame
import sys

# Kendi oluşturduğumuz alt menü sınıflarını içeri aktarıyoruz
from notes import NotesMenu
from chords import ChordsMenu

pygame.init()
WIDTH, HEIGHT = 1920, 1024
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tamamen Ayrılmış Modüler Menüler")
clock = pygame.time.Clock()

BG_COLOR = (40, 40, 40)

def main():
    # Menü nesnelerini oluşturuyoruz (Ekran boyutlarını parametre olarak göndererek)
    menu_sol = ChordsMenu(WIDTH, HEIGHT)
    menu_sag = NotesMenu(WIDTH, HEIGHT)

    running = True
    while running:
        screen.fill(BG_COLOR)
        mx, my = pygame.mouse.get_pos()
        
        # Farenin menülerdeki durumunu al
        hovered_sol = menu_sol.get_hovered_segment(mx, my)
        hovered_sag = menu_sag.get_hovered_segment(mx, my)

        # Olay (Event) Kontrolü
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Sol tık
                    
                    # Eğer farenin altında sol menüden bir buton varsa, sol menünün işlemini yap
                    if hovered_sol != -1:
                        menu_sol.islem_yap(hovered_sol)
                        
                    # Eğer farenin altında sağ menüden bir buton varsa, sağ menünün işlemini yap
                    elif hovered_sag != -1:
                        menu_sag.islem_yap(hovered_sag)

        # Çizim işlemleri
        transparent_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        menu_sol.draw(transparent_surface, hovered_sol)
        menu_sag.draw(transparent_surface, hovered_sag)
        
        screen.blit(transparent_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()