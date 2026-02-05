import pygame


class Enemy:
    def __init__(self, data, pos):
        self.data = data

        self.size = data.get("size", 32)
        self.x, self.y = float(pos[0]), float(pos[1])
        self.rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)

        self.hp = data["hp"]
        self.max_hp = data["hp"]
        self.speed = data["speed"]
        self.damage = data["damage"]
        #kontact-hit-cooldown
        self.hit_cooldown = data.get("hit_cooldown", 1.4) # sekunden
        self.hit_timer = 0.0
        #Stun/ hit stun
        self.stun_timer = 0.0
        self.stun_duration = 0.35

        # Knockback / Hitstun
        self.vx, self.vy = 0.0, 0.0
        self.knockback_friction = 0.85

        # Sprite optional
        self.sprite = None
        sprite_path = data.get("sprite")
        if sprite_path:
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))

        # Rush ability (für Boss)
        self.rush_cooldown = data.get("rush_cooldown", 0)
        self.rush_timer = 0
        self.rush_state = "idle"
        self.rush_windup = data.get("rush_windup", 0.5)
        self.rush_speed = data.get("rush_speed", 10.0)
        self.rush_duration = data.get("rush_duration", 0.3)
        self.rush_dir = (0, 0)  # Richtung für Dash

        self.alive = True

    def take_damage(self, amount, knock_dir=(0, 0), knock_strength=6.0):
        if not self.alive:
            return
        self.hp -= int(amount)

        # Knockback
        dx, dy = knock_dir
        self.vx += dx * knock_strength
        self.vy += dy * knock_strength

        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def update(self, dt, player_rect, map_manager=None):
        if not self.alive:
            return
        # Hit cooldown timer
        if self.hit_timer > 0:
            self.hit_timer -= dt
            if self.hit_timer < 0:
                self.hit_timer = 0
        # Stun timer
        if self.stun_timer > 0:
            self.stun_timer -= dt
            if self.stun_timer < 0:
                self.stun_timer = 0
            return  # Skip movement while stunned

        # Rush ability
        if self.rush_cooldown > 0:
            self.rush_timer -= dt
            if self.rush_state == "idle":
                if self.rush_timer <= 0:
                    # Starte Windup: Richtung weg vom Player
                    px, py = player_rect.centerx, player_rect.centery
                    ex, ey = self.rect.centerx, self.rect.centery
                    dx = ex - px
                    dy = ey - py
                    mag = (dx * dx + dy * dy) ** 0.5
                    if mag != 0:
                        dx /= mag
                        dy /= mag
                    self.rush_dir = (dx, dy)
                    self.rush_state = "windup"
                    self.rush_timer = self.rush_windup
            elif self.rush_state == "windup":
                if self.rush_timer <= 0:
                    # Starte Dash: Richtung zum Player
                    px, py = player_rect.centerx, player_rect.centery
                    ex, ey = self.rect.centerx, self.rect.centery
                    dx = px - ex
                    dy = py - ey
                    mag = (dx * dx + dy * dy) ** 0.5
                    if mag != 0:
                        dx /= mag
                        dy /= mag
                    self.rush_dir = (dx, dy)
                    self.rush_state = "dashing"
                    self.rush_timer = self.rush_duration
                else:
                    # Während Windup: leicht zurück bewegen
                    dx, dy = self.rush_dir
                    self.x += dx * self.speed * 0.5 * dt * 60  # Langsamer zurück
                    self.y += dy * self.speed * 0.5 * dt * 60
                    self.rect.topleft = (int(self.x), int(self.y))
                    return
            elif self.rush_state == "dashing":
                if self.rush_timer <= 0:
                    self.rush_state = "idle"
                    self.rush_timer = self.rush_cooldown
                else:
                    # Dash-Bewegung
                    dx, dy = self.rush_dir
                    new_x = self.x + dx * self.rush_speed * dt * 60
                    new_y = self.y + dy * self.rush_speed * dt * 60
                    # Einfacher Kollisionscheck für Wände
                    temp_rect = pygame.Rect(int(new_x), int(new_y), self.size, self.size)
                    if map_manager and map_manager.check_collision(temp_rect):
                        # Stoppe Dash bei Kollision
                        self.rush_state = "idle"
                        self.rush_timer = self.rush_cooldown
                    else:
                        self.x = new_x
                        self.y = new_y
                        self.rect.topleft = (int(self.x), int(self.y))
                    return

        # follow player
        px, py = player_rect.centerx, player_rect.centery
        ex, ey = self.rect.centerx, self.rect.centery
        dx = px - ex
        dy = py - ey

        # Normalize (ohne math import)
        mag = (dx * dx + dy * dy) ** 0.5
        if mag != 0:
            dx /= mag
            dy /= mag

        # --- Kollisionssichere Bewegung (wie beim Player) ---
        # X-Achse
        new_x = self.x + dx * self.speed * dt * 60 + self.vx * dt * 60
        old_y = self.y
        temp_rect = pygame.Rect(int(new_x), int(old_y), self.size, self.size)
        if map_manager and map_manager.check_collision(temp_rect):
            # Versuche Alternativrichtungen, falls blockiert (einfaches Ausweichen)
            tried = False
            # Erst nur Y bewegen
            alt_rect = pygame.Rect(int(self.x), int(self.y + dy * self.speed * dt * 60), self.size, self.size)
            if not map_manager.check_collision(alt_rect):
                new_x = self.x
                new_y = self.y + dy * self.speed * dt * 60 + self.vy * dt * 60
                tried = True
            else:
                # Dann nur X bewegen
                alt_rect = pygame.Rect(int(self.x + dx * self.speed * dt * 60), int(self.y), self.size, self.size)
                if not map_manager.check_collision(alt_rect):
                    new_x = self.x + dx * self.speed * dt * 60 + self.vx * dt * 60
                    new_y = self.y
                    tried = True
            if not tried:
                new_x = self.x
                new_y = self.y
        else:
            # Y-Achse
            new_y = self.y + dy * self.speed * dt * 60 + self.vy * dt * 60
            temp_rect = pygame.Rect(int(new_x), int(new_y), self.size, self.size)
            if map_manager and map_manager.check_collision(temp_rect):
                new_y = self.y  # Rücksetzen bei Kollision

        self.x = new_x
        self.y = new_y

        # Knockback-Friction
        self.vx *= self.knockback_friction
        self.vy *= self.knockback_friction

        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, screen, camera=None):
        if not self.alive:
            return

        # Apply camera offset if provided
        if camera:
            screen_rect = camera.apply(self.rect)
        else:
            screen_rect = self.rect

        if self.sprite:
            screen.blit(self.sprite, screen_rect)
        else:
            pygame.draw.rect(screen, (200, 60, 60), screen_rect)

        # HP bar (tiny)
        bar_w = screen_rect.width
        bar_h = 5
        hp_ratio = self.hp / self.max_hp if self.max_hp else 0
        bg = pygame.Rect(screen_rect.left, screen_rect.top - 8, bar_w, bar_h)
        fg = pygame.Rect(screen_rect.left, screen_rect.top - 8, int(bar_w * hp_ratio), bar_h)
        pygame.draw.rect(screen, (40, 40, 40), bg)
        pygame.draw.rect(screen, (80, 220, 80), fg)
