import os
import pygame

# Absoluter Projekt-Root: .../pygame.rougelike.surv
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class UIBar:
    def __init__(self, x, y, width, height, fill_path, bg_path=None):
        self.x, self.y = x, y
        self.width, self.height = width, height

        fill_abs = os.path.join(BASE_DIR, fill_path)
        self.fill_img = pygame.image.load(fill_abs).convert_alpha()
        self.fill_img = pygame.transform.scale(self.fill_img, (width, height))

        self.bg_img = None
        if bg_path:
            bg_abs = os.path.join(BASE_DIR, bg_path)
            self.bg_img = pygame.image.load(bg_abs).convert_alpha()
            self.bg_img = pygame.transform.scale(self.bg_img, (width, height))

    def draw(self, screen, ratio):
        ratio = max(0.0, min(1.0, ratio))

        if self.bg_img:
            screen.blit(self.bg_img, (self.x, self.y))

        fill_w = int(self.width * ratio)
        if fill_w > 0:
            screen.blit(
                self.fill_img,
                (self.x, self.y),
                area=pygame.Rect(0, 0, fill_w, self.height)
            )
