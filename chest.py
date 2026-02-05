import pygame

class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size=32):
        super().__init__()
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.rect = pygame.Rect(x, y, tile_size, tile_size)
        self.opened = False
        self.image = pygame.image.load("assets/images/chest/chest.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))

    def open(self):
        if not self.opened:
            self.opened = True
            # Chest wird entfernt, also kein Image-Change nötig
            return True  # Gib True zurück, wenn erfolgreich geöffnet
        return False