import pygame
import math

class RadialMenu:
    # labels=None ekledik, böylece yazı göndermezsek hata vermez
    def __init__(self, center, inner_radius, outer_radius, num_segments, labels=None):
        self.center = center
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.num_segments = num_segments
        self.segment_angle = 360 / num_segments
        self.line_color = (255, 255, 255)
        
        self.labels = labels
        # Pygame'in varsayılan fontunu kullanıyoruz (Arial benzeri), boyutu 24
        self.font = pygame.font.SysFont(None, 24)

    def get_hovered_segment(self, mx, my):
        # Burası eskisiyle tamamen aynı kalacak
        dx = mx - self.center[0]
        dy = my - self.center[1]
        distance = math.hypot(dx, dy)
        
        if self.inner_radius <= distance <= self.outer_radius:
            mouse_angle = math.degrees(math.atan2(dy, dx))
            if mouse_angle < 0:
                mouse_angle += 360
            return int(mouse_angle // self.segment_angle)
        return -1 

    def draw(self, surface, hovered_segment):
        for i in range(self.num_segments):
            start_angle = i * self.segment_angle
            end_angle = (i + 1) * self.segment_angle
            
            if i == hovered_segment:
                color = (0, 0, 0, 200)
            else:
                color = (0, 0, 0, 100)
                
            self._draw_segment(surface, color, start_angle, end_angle)
            
            # --- YAZI ÇİZİM KISMI ---
            if self.labels and i < len(self.labels):
                # 1. Dilimin tam orta açısını bul (Derece)
                mid_angle = (start_angle + end_angle) / 2
                rad = math.radians(mid_angle)
                
                # 2. Yazının merkeze olan uzaklığı (İç ve dış çemberin tam ortası)
                text_radius = (self.inner_radius + self.outer_radius) / 2
                
                # 3. Yazının X ve Y koordinatlarını Trigonometri ile hesapla
                text_x = self.center[0] + text_radius * math.cos(rad)
                text_y = self.center[1] + text_radius * math.sin(rad)
                
                # 4. Yazıyı oluştur (Beyaz renk) ve tam o koordinata ortala
                text_surface = self.font.render(self.labels[i], True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(text_x, text_y))
                surface.blit(text_surface, text_rect)

    def _draw_segment(self, surface, color, start_angle, end_angle):
        # Burası eskisiyle tamamen aynı kalacak
        points = []
        for angle in range(int(start_angle), int(end_angle) + 1):
            rad = math.radians(angle)
            x = self.center[0] + self.outer_radius * math.cos(rad)
            y = self.center[1] + self.outer_radius * math.sin(rad)
            points.append((x, y))
            
        for angle in range(int(end_angle), int(start_angle) - 1, -1):
            rad = math.radians(angle)
            x = self.center[0] + self.inner_radius * math.cos(rad)
            y = self.center[1] + self.inner_radius * math.sin(rad)
            points.append((x, y))
            
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, self.line_color, points, 2)