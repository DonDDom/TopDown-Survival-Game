import pygame

# Toggle runtime debug prints from this module
DEBUG = False


class Player:
    def __init__(self, data, pos):
        self.x, self.y = pos
        self.speed = data["speed"]

        # Größe (passt zu 16x16 Sprite → hochskaliert)
        self.size = 32
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

        # Stats
        self.hp = data["hp"]
        self.max_hp = self.hp
        self.resource_type = data["resource"]
        self.max_resource = data["resource_max"]
        self.resource = self.max_resource
        self.resource_regen = data["resource_regen"]
        self.attack = data["attack"]

        #Attack cooldown
        self.attack_timer = 0.0
        self.attack_cooldown = 0.30

        #Richtungsbasiertes Gehen
        self.facing = "down" #Start richtung
        # remember which horizontal hand the player used last (left/right)
        self.last_hand = "right"

        #I-Frames
        self.invuln_timer = 0.0
        self.invuln_duration = 0.6   # Sekunden

        #knockback velocity
        self.vx, self.vy = 0.0, 0.0
        self.knock_friction = 0.85

                #Dash
        self.dash_cost = 25 #dash kosten pro dash
        self.dash_cooldown = 0.6 #sekund
        # reduce dash distance so player can't dash through walls easily
        # previous: dash_speed=14.0, dash_duration=0.12 -> ~100px
        # new values aim for ~48px total dash distance
        self.dash_duration = 0.10 #sekunden (wie lang der dash zieht)
        self.dash_speed = 8.0 # wie stark der dash ist

        self.dash_cd_timer = 0.0
        self.dash_timer = 0.0
        self.is_dashing = False

        #player tod
        self.dead = False

        #letzte Bewegungsrichtung für Dash merken
        self.last_move_dir = (1, 0) #default rechts

        # Sprite laden
        self.sprite = None
        sprite_path = data.get("sprite")
        if sprite_path:
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            self.sprite = pygame.transform.scale(
                self.sprite, (self.size, self.size)
            )
        # Sword sprite laden
        self.sword_img = pygame.image.load("assets/images/weapon/sword.png").convert_alpha()
        self.sword_img = pygame.transform.scale(self.sword_img, (self.size, self.size))
        
        # Speichere die Daten für Reset
        self.data = data

    def reset(self, pos):
        """Reset player to spawn position with full stats"""
        self.x, self.y = pos
        self.hp = self.data["hp"]
        self.max_hp = self.hp
        self.resource = self.max_resource
        self.attack_timer = 0.0
        self.facing = "down"
        self.last_hand = "right"
        self.invuln_timer = 0.0
        self.vx, self.vy = 0.0, 0.0
        self.dash_cd_timer = 0.0
        self.dash_timer = 0.0
        self.is_dashing = False
        self.last_move_dir = (1, 0)
        self.rect.topleft = (int(self.x), int(self.y))
        
    def update(self, dt, keys):
        #cooldown timer runterzählen
        if self.dash_cd_timer > 0:
            self.dash_cd_timer -= dt
            if self.dash_cd_timer < 0:
                self.dash_cd_timer = 0
        
        #attack cooldown tick
        if self.attack_timer > 0:
            self.attack_timer -= dt
            if self.attack_timer < 0:
                self.attack_timer = 0
        #dash timer runterzählen
        if self.is_dashing:
            self.dash_timer -= dt
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.dash_timer = 0

        if self.invuln_timer > 0:
            self.invuln_timer -= dt
            if self.invuln_timer < 0:
                self.invuln_timer = 0
        #stamina regenerieren
        if self.resource < self.max_resource:
            self.resource += self.resource_regen * dt
            if self.resource > self.max_resource:
                self.resource = self.max_resource

        dx, dy = 0, 0

        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed
        #Faccing setzen (Richtung merken)
        if dx != 0 or dy != 0:
            if abs(dx) > abs(dy):
                self.facing = "right" if dx > 0 else "left"
                # update last horizontal hand when moving left/right
                self.last_hand = "right" if dx > 0 else "left"
            else:
                self.facing = "down" if dy > 0 else "up"

        # FPS-unabhängige Bewegung
        self.x += dx * dt * 60
        self.y += dy * dt * 60
        # Knockback anwenden
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        if not self.is_dashing:
            self.vx *= self.knock_friction
            self.vy *= self.knock_friction

        self.rect.topleft = (int(self.x), int(self.y)) 
    
    def try_dash(self, dir_vec):
        if self.is_dashing:
            return False
        if self.dash_cd_timer > 0:
            return False
        if self.resource < self.dash_cost:
            return False
        dx, dy = dir_vec
        mag = (dx*dx + dy*dy) ** 0.5
        if mag == 0:
            #wenn keine richtung -> nimm letzte bewegungsrichtung
            dx, dy = self.last_move_dir
            mag = (dx*dx + dy*dy) ** 0.5
            if mag == 0:
                dx, dy = (1, 0)
                mag = 1
        dx /= mag
        dy /= mag

        #stamina zahlen
        self.resource -= self.dash_cost
        if self.resource < 0:
            self.resource = 0
        #dash state
        self.is_dashing = True
        self.dash_timer = self.dash_duration
        self.dash_cd_timer = self.dash_cooldown

        # i-frames während dash
        self.invuln_timer = max(self.invuln_timer, self.dash_duration)
        #dash velocity (einmaliger boost)
        self.vx = dx * self.dash_speed
        self.vy = dy * self.dash_speed

        return True

    def try_attack(self):
        """Versucht einen Attack auszuführen, wenn die Cooldown abgelaufen ist"""
        if self.attack_timer > 0:
            return False  # Cooldown ist noch aktiv
        
        # Attack ausführen
        self.attack_timer = self.attack_cooldown  # Cooldown setzen
        return True

    def draw(self, screen, camera=None):
        # blink during i-frames
        blink = self.invuln_timer > 0 and (pygame.time.get_ticks() // 80) % 2 == 0
        # debug info (only when DEBUG=True)
        if DEBUG:
            print(f"draw called: invuln={self.invuln_timer:.2f}, blink={blink}, sprite_set={self.sprite is not None}, facing={self.facing}, rect={self.rect}, x={self.x:.2f}, y={self.y:.2f}, vx={self.vx:.2f}, vy={self.vy:.2f}")
        if blink:
            return
        #Player sprite
        spr = self.sprite
        if self.facing == "left":
            spr = pygame.transform.flip(self.sprite, True, False)
        # Sword orientation: keep the sword vertical (pointing upwards) at all times
        # and flip horizontally when the player uses the left hand so it sits on
        # the left side of the sprite.
        sword = self.sword_img
        if (self.facing == "left") or (self.last_hand == "left" and self.facing in ("up", "down", "right")):
            sword = pygame.transform.flip(sword, True, False)

        # Compute hand position per facing so sword sits in the player's hand
        w, h = self.rect.width, self.rect.height
        if self.facing == "right":
            hand_x = self.rect.right - w // 6
            hand_y = self.rect.centery
        elif self.facing == "left":
            hand_x = self.rect.left + w // 6
            hand_y = self.rect.centery
        elif self.facing == "up":
            # place sword in the same hand position as left/right
            if self.last_hand == "right":
                hand_x = self.rect.right - w // 6
            else:
                hand_x = self.rect.left + w // 6
            # match the vertical position used for left/right so sword stays in same hand
            hand_y = self.rect.centery
        else:  # down
            if self.last_hand == "right":
                hand_x = self.rect.right - w // 6
            else:
                hand_x = self.rect.left + w // 6
            hand_y = self.rect.centery

        sword_pos = (hand_x, hand_y)

        # Apply camera offset if provided
        if camera:
            screen_rect = camera.apply(self.rect)
            screen_sword_pos = (sword_pos[0] - camera.offset_x, sword_pos[1] - camera.offset_y)
        else:
            screen_rect = self.rect
            screen_sword_pos = sword_pos

        # Draw player sprite then sword on top so it's visible in the hand
        screen.blit(spr, screen_rect)
        screen.blit(sword, sword.get_rect(center=screen_sword_pos))

    def take_damage(self,amount,knock_dir=(0,0),knock_strength=10.0):
        #i-frames aktiv -> kein schaden
        if self.invuln_timer > 0:
            return
        # schaden nehmen
        self.hp -= int(amount)
        if self.hp < 0:
            self.hp = 0
        #Tod Check
        if self.hp <= 0:
            self.hp = 0
            self.dead = True
            return
        # i-frames starten
        self.invuln_timer = self.invuln_duration
        # knockback geben (cap total knockback speed)
        dx, dy = knock_dir
        self.vx += dx * knock_strength
        self.vy += dy * knock_strength
        # limit resulting knockback magnitude
        max_knock_speed = 20.0
        mag = (self.vx * self.vx + self.vy * self.vy) ** 0.5
        if mag > max_knock_speed and mag != 0:
            scale = max_knock_speed / mag
            self.vx *= scale
            self.vy *= scale
        if DEBUG:
            print(f"Player HP:{self.hp}")

    def reset(self, pos):
        #Position
        self.x, self.y = float(pos[0]), float(pos[1])
        self.rect.topleft = (int(self.x), int(self.y))
        #Leben/ressources
        self.hp = self.max_hp
        self.resource = self.max_resource
        #Zustände / Timer
        self.dead = False
        self.invuln_timer = 0.0
        self.attack_timer = 0.0
        self.dash_timer = 0.0 if hasattr(self, 'dash_timer') else 0.0
        #Knockback/Velocity
        if hasattr(self, 'vx'): self.vx = 0.0
        if hasattr(self, 'vy'): self.vy = 0.0

