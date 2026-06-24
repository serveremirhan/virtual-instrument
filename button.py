import pygame
import math

class RadialMenu:
    def __init__(self, center, inner_radius, outer_radius, num_segments):
        self.center = center
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.num_segments = num_segments
        self.segment_angle = 360 / num_segments
        self.line_color = (255, 255, 255)

    def get_hovered_segment(self, mx, my):
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

    def _draw_segment(self, surface, color, start_angle, end_angle):
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