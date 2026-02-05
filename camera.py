class Camera:
    def __init__(self, screen_width, screen_height):
        self.offset_x = 0
        self.offset_y = 0
        self.screen_w = screen_width
        self.screen_h = screen_height

    def update(self, target_rect):
        # Center Camera on Player
        self.offset_x = target_rect.centerx - self.screen_w // 2
        self.offset_y = target_rect.centery - self.screen_h // 2
    
    def apply(self, rect):
        # Welt -> screen Koordinaten
        return rect.move(-self.offset_x, -self.offset_y)
