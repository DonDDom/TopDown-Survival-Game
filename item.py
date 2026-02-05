import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, tile_size=32):
        super().__init__()
        self.x = x
        self.y = y
        self.item_type = item_type
        self.tile_size = tile_size
        self.rect = pygame.Rect(x, y, tile_size, tile_size)
        self.collected = False

        # Bilder für Items
        if item_type == "health_potion":
            self.image = pygame.image.load("assets/images/items/potion_health.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (tile_size, tile_size))

    def collect(self):
        self.collected = True
        self.kill()  # Entferne vom Screen