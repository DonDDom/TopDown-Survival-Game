first_room_blocked = False
first_room_triggered = False
def set_first_room_blocked(blocked):
    from tile import Tile
    first_room_block_positions = [(7,7), (7,8), (7,9)]  # Spalte 8, Zeile 8-10
    for (x, y) in first_room_block_positions:
        world_x = x * map_manager.tile_size
        world_y = y * map_manager.tile_size
        for tile in list(map_manager.tiles):
            if tile.rect.topleft == (world_x, world_y):
                map_manager.tiles.remove(tile)
        tile_id = 41 if blocked else 49
        map_manager.tiles.add(Tile(world_x, world_y, tile_id, map_manager.tile_size))

        # --- Erster Raum Blockier-Logik (ganz vorne, allererste Wand) ---
        # Trigger: Spieler durchquert Spalte 8 (x=7) oder 9 (x=8), Zeile 8-10 (y=7-9), bleibt aktiv bis Wand gesetzt

    # --- Erster Raum Blockier-Logik (ganz vorne, allererste Wand) ---
    py = int(player.y // 32)
    px = int(player.x // 32)
    if not first_room_blocked and (7 <= py <= 9) and (px == 7 or px == 8):
        set_first_room_blocked(True)
        first_room_blocked = True
        first_room_triggered = True
    # Entferne Wände wieder, wenn keine Gegner mehr da (optional, falls gewünscht)
    if first_room_blocked and not enemies:
        set_first_room_blocked(False)
        first_room_blocked = False
extra_room_spawn_pending = False
extra_room_spawn_time = 0
extra_room_spawn_delay_ms = 500

extra_room_blocked = False
extra_room_triggered = False
extra_room_entry_pos = None
extra_room_spawn_timer_started = False
extra_room_spawn_start_time = 0
extra_room_spawn_delay = 1000  # ms
extra_room_wave = 0
extra_room_max_waves = 3
extra_room_cleared = False

third_room_triggered = False
third_room_wave = 0
third_room_max_waves = 3
third_room_cleared = False
third_room_spawn_timer_started = False
third_room_spawn_start_time = 0
third_room_spawn_delay = 1000  # ms

fourth_room_triggered = False
fourth_room_wave = 0
fourth_room_max_waves = 2
fourth_room_cleared = False
fourth_room_spawn_timer_started = False
fourth_room_spawn_start_time = 0
fourth_room_spawn_delay = 500  # ms

fifth_room_triggered = False
fifth_room_wave = 0
fifth_room_max_waves = 4
fifth_room_cleared = False
fifth_room_spawn_timer_started = False
fifth_room_spawn_start_time = 0
fifth_room_spawn_delay = 500  # ms

sixth_room_triggered = False
sixth_room_cleared = False
sixth_room_spawned = False
extra_room_block_positions = [
    # Wand bei Reihe 17,18,19, Spalte 14
    (13,16), (13,17), (13,18),
    # Wand bei Reihe 28,29,30, Spalte 14
    (13,27), (13,28), (13,29),
    # Wand bei Reihe 31, Spalte 6,7,8
    (5,30), (6,30), (7,30)
]

def set_extra_room_blocked(blocked):
    from tile import Tile
    for (x, y) in extra_room_block_positions:
        world_x = x * map_manager.tile_size
        world_y = y * map_manager.tile_size
        for tile in list(map_manager.tiles):
            if tile.rect.topleft == (world_x, world_y):
                map_manager.tiles.remove(tile)
        tile_id = 41 if blocked else 49
        map_manager.tiles.add(Tile(world_x, world_y, tile_id, map_manager.tile_size))
import pygame
from Player import Player
from Player_Stats import CHARACTERS
from Enemy import Enemy
from Enemy_Stats import ENEMIES
from chest import Chest
from item import Item
from ui.bars import UIBar
from camera import Camera
from map_manager import MapManager

# --- Raum-Blockier-Logik ---
room_blocked = False
room_block_positions = [
    (7,7), (7,8), (7,9),           # Spalte 8, Zeile 8-10
    (13,16), (13,17), (13,18),    # Spalte 14, Zeile 17-19
    (25,3), (25,4),               # Spalte 26, Zeile 4-5
    (25,5)                        # Spalte 26, Zeile 6 (korrigiert)
]
def set_room_blocked(blocked):
    from tile import Tile
    for (x, y) in room_block_positions:
        world_x = x * map_manager.tile_size
        world_y = y * map_manager.tile_size
        # Entferne evtl. vorhandene Tiles an dieser Stelle
        for tile in list(map_manager.tiles):
            if tile.rect.topleft == (world_x, world_y):
                map_manager.tiles.remove(tile)
        # Setze Wand oder Boden
        tile_id = 41 if blocked else 49
        map_manager.tiles.add(Tile(world_x, world_y, tile_id, map_manager.tile_size))

pygame.init()

game_over = False
game_won = False
SPAWN_POS = (80, 80)

#Reset Funktion
def reset_run(player, enemies, chests, items, spawn_pos):
    enemies.clear()
    chests.clear()
    items.clear()
    player.reset(spawn_pos)
    player.x, player.y = spawn_pos

    # Map zurückladen
    map_manager.load_map_from_csv("assets/tiles/maps/room1.csv")

    # Chests neu laden
    import csv
    with open("assets/tiles/maps/room1.csv", 'r') as file:
        reader = csv.reader(file)
        y = 0
        for row in reader:
            x = 0
            for tile_id_str in row:
                tile_id = int(tile_id_str) if tile_id_str.strip() else -1
                if tile_id == 45:
                    world_x = x * 32
                    world_y = y * 32
                    chests.append(Chest(world_x, world_y))
                x += 1
            y += 1

    # Raum-Status zurücksetzen
    global room_blocked, current_wave, spawn_timer_started, spawn_start_time, first_room_blocked
    room_blocked = False
    current_wave = 0
    spawn_timer_started = False
    spawn_start_time = 0
    first_room_blocked = False

    # Extra-Raum-Status zurücksetzen
    global extra_room_blocked, extra_room_triggered, extra_room_entry_pos, extra_room_spawn_pending, extra_room_spawn_time, extra_room_cleared, extra_room_wave, extra_room_spawn_timer_started, extra_room_spawn_start_time, third_room_triggered, third_room_wave, third_room_cleared, third_room_spawn_timer_started, third_room_spawn_start_time, fourth_room_triggered, fourth_room_wave, fourth_room_cleared, fourth_room_spawn_timer_started, fourth_room_spawn_start_time, fifth_room_triggered, fifth_room_wave, fifth_room_cleared, fifth_room_spawn_timer_started, fifth_room_spawn_start_time, sixth_room_triggered, sixth_room_cleared
    extra_room_blocked = False
    extra_room_triggered = False
    extra_room_entry_pos = None
    extra_room_spawn_pending = False
    extra_room_spawn_time = 0
    extra_room_cleared = False
    extra_room_wave = 0
    extra_room_spawn_timer_started = False
    extra_room_spawn_start_time = 0
    third_room_triggered = False
    third_room_wave = 0
    third_room_cleared = False
    third_room_spawn_timer_started = False
    third_room_spawn_start_time = 0
    fourth_room_triggered = False
    fourth_room_wave = 0
    fourth_room_cleared = False
    fourth_room_spawn_timer_started = False
    fourth_room_spawn_start_time = 0
    fifth_room_triggered = False
    fifth_room_wave = 0
    fifth_room_cleared = False
    fifth_room_spawn_timer_started = False
    fifth_room_spawn_start_time = 0
    sixth_room_triggered = False
    sixth_room_cleared = False
    sixth_room_spawned = False
    elite_defeated = False
    elite_defeated = False  # Wird gesetzt, wenn Elite besiegt

# Bildschirmgröße
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
# Bildschirm erstellen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT,))
hp_bar = UIBar(x=20, y=20, width=200, height=20,
               fill_path="assets/images/ui/hp_fill.png",
               bg_path="assets/images/ui/hp_bg.png")
stamina_bar = UIBar(x=20, y=45, width=200, height=16,
                    fill_path="assets/images/ui/stamina_fill.png",
                   bg_path="assets/images/ui/stamina_bg.png")
pygame.display.set_caption("My Roguelike Game")

clock = pygame.time.Clock()

player = Player(CHARACTERS["knight"], SPAWN_POS)
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
map_manager = MapManager(tile_size=32)
map_manager.load_map_from_csv("assets/tiles/maps/room1.csv")

# Lade Chests aus der Map
import csv
chests = []
with open("assets/tiles/maps/room1.csv", 'r') as file:
    reader = csv.reader(file)
    y = 0
    for row in reader:
        x = 0
        for tile_id_str in row:
            tile_id = int(tile_id_str) if tile_id_str.strip() else -1
            if tile_id == 45:
                world_x = x * 32
                world_y = y * 32
                chests.append(Chest(world_x, world_y))
            x += 1
        y += 1

enemies = []  # Gegner werden erst beim Betreten des Raums gespawnt
items = []  # Items wie Potions

# Timer und Wellen-Logik für Gegner-Spawns
spawn_timer_started = False
spawn_start_time = 0
spawn_delay = 400  # Millisekunden (0.4 Sekunden Verzögerung)
current_wave = 0
max_waves = 3
def get_safe_spawn(x, y, map_manager, size=32):
    """Sucht eine freie Position in der Nähe, falls die Zielposition blockiert ist."""
    rect = pygame.Rect(int(x), int(y), size, size)
    if not map_manager.check_collision(rect):
        return (x, y)
    # Suche in der Umgebung (Kreis)
    for r in range(1, 6):
        for dx in range(-r, r+1):
            for dy in range(-r, r+1):
                tx, ty = x + dx*size, y + dy*size
                rect = pygame.Rect(int(tx), int(ty), size, size)
                if not map_manager.check_collision(rect):
                    return (tx, ty)
    return (x, y)  # Fallback

def get_room_spawn(x, y, map_manager, size=32, room_rect=None):
    """Sucht eine freie Position in einem Raum (optionaler Bereich)."""
    rect = pygame.Rect(int(x), int(y), size, size)
    if not map_manager.check_collision(rect) and (room_rect is None or room_rect.contains(rect)):
        return (x, y)
    # Suche in der Umgebung (Kreis)
    for r in range(1, 8):
        for dx in range(-r, r+1):
            for dy in range(-r, r+1):
                tx, ty = x + dx*size, y + dy*size
                rect = pygame.Rect(int(tx), int(ty), size, size)
                if not map_manager.check_collision(rect) and (room_rect is None or room_rect.contains(rect)):
                    return (tx, ty)
    return (x, y)  # Fallback

# Definiere den Raum als pygame.Rect (z.B. Raum 1: x=250, y=200, w=350, h=200)

# Raum-Rect initialisieren, bevor Spawns generiert werden
room1_rect = pygame.Rect(250, 200, 350, 200)
extra_room_rect = pygame.Rect(128, 544, 288, 384)
third_room_rect = pygame.Rect(928, 96, 416, 416)
fourth_room_rect = pygame.Rect(544, 736, 288, 544)
fifth_room_rect = pygame.Rect(992, 896, 960, 384)
sixth_room_rect = pygame.Rect(1536, 64, 416, 736)

# Gleichmäßig verteilte Spawn-Positionen für jede Welle
import random
def get_spread_spawns(n, room_rect, map_manager, y_margin=40, min_dist=48):
    """Erzeuge n gleichmäßig verteilte, freie Spawn-Positionen im Raum."""
    positions = []
    player_pos = (player.x, player.y) if 'player' in globals() else (room_rect.centerx, room_rect.centery)
    # Definiere die vier Ecken des Raums
    corners = [
        (room_rect.left + 8, room_rect.top + 8),
        (room_rect.right - 40, room_rect.top + 8),
        (room_rect.left + 8, room_rect.bottom - 40),
        (room_rect.right - 40, room_rect.bottom - 40)
    ]
    # Sortiere Ecken nach Entfernung zum Spieler (absteigend)
    corners.sort(key=lambda c: ((c[0]-player_pos[0])**2 + (c[1]-player_pos[1])**2), reverse=True)
    import random
    # Speziallogik für 2. und 3. Welle
    if 'current_wave' in globals() and room_rect == room1_rect:
        if current_wave == 1:
            # 2. Welle: Bat in Zeile 2-4, Spalte 14-19; Ghost in Zeile 16-19, Spalte 15-18
            tile_size = 32
            bat_row = random.randint(2, 4)
            bat_col = random.randint(14, 19)
            bat_x = bat_col * tile_size
            bat_y = bat_row * tile_size
            bat_pos = get_room_spawn(bat_x, bat_y, map_manager, room_rect=None)
            ghost_row = random.randint(16, 19)
            ghost_col = random.randint(15, 18)
            ghost_x = ghost_col * tile_size
            ghost_y = ghost_row * tile_size
            ghost_pos = get_room_spawn(ghost_x, ghost_y, map_manager, room_rect=None)
            return [bat_pos, ghost_pos]
        if current_wave == 2:
            # 3. Welle: beide Gegner in Zeile 8–18, Spalte 22–24
            tile_size = 32
            row1 = random.randint(8, 18)
            col1 = random.randint(22, 24)
            row2 = random.randint(8, 18)
            col2 = random.randint(22, 24)
            pos1 = get_room_spawn(col1 * tile_size, row1 * tile_size, map_manager, room_rect=None)
            pos2 = get_room_spawn(col2 * tile_size, row2 * tile_size, map_manager, room_rect=None)
            return [pos1, pos2]
    # Standard: entfernte Ecken (wiederhole oder wähle zufällig wenn mehr Positionen als Ecken)
    for i in range(n):
        corner_index = i % len(corners)  # Zyklisch durch corners gehen
        pos = get_room_spawn(*corners[corner_index], map_manager, room_rect=room_rect)
        positions.append(pos)
    return positions


running = True
in_menu = True

# Menu loop
start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 300, 200, 100)
while in_menu:
    dt = clock.tick(60) / 1000
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_menu = False
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if start_button.collidepoint(mouse_pos):
                    in_menu = False
    screen.fill((20, 20, 40))  # Dunkler blauer Hintergrund
    # Draw menu
    font = pygame.font.SysFont(None, 72)
    title = font.render("Roguelike Spiel", True, (255, 255, 255))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
    
    # Button Farbe basierend auf Hover
    if start_button.collidepoint(mouse_pos):
        button_color = (150, 150, 200)  # Heller bei Hover
    else:
        button_color = (100, 100, 150)  # Dunkleres Blau
    
    pygame.draw.rect(screen, button_color, start_button, border_radius=10)  # Abgerundete Ecken
    pygame.draw.rect(screen, (255, 255, 255), start_button, 2, border_radius=10)  # Weißer Rahmen
    
    start_text = pygame.font.SysFont(None, 48).render("Start", True, (255, 255, 255))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 325))
    
    # Untertitel
    subtitle_font = pygame.font.SysFont(None, 36)
    subtitle = subtitle_font.render("Klicke auf Start, um zu spielen", True, (200, 200, 200))
    screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 450))
    
    pygame.display.flip()

while running:
    dt = clock.tick(60) / 1000
    dash_pressed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                reset_run(player, enemies, chests, items, SPAWN_POS)
                game_over = False
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_won and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                restart_button = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 20, 120, 50)
                menu_button = pygame.Rect(SCREEN_WIDTH//2 + 30, SCREEN_HEIGHT//2 - 20, 120, 50)
                if restart_button.collidepoint(mouse_x, mouse_y):
                    reset_run(player, enemies, chests, items, SPAWN_POS)
                    game_won = False
                elif menu_button.collidepoint(mouse_x, mouse_y):
                    in_menu = True
                    game_won = False
                    running = False
            if event.button == 3: # right click for dash
                dash_pressed = True
            if event.button == 1: # left click for attack
                if not game_over and not game_won:
                    # larger attack hitbox so player doesn't miss enemies while attacking
                    hitbox = player.rect.inflate(80, 80)
                    for enemy in enemies:
                        if enemy.alive and hitbox.colliderect(enemy.rect):
                            dx = enemy.rect.centerx - player.rect.centerx
                            dy = enemy.rect.centery - player.rect.centery
                            mag = (dx * dx + dy * dy) ** 0.5
                            if mag != 0:
                                dx /= mag
                                dy /= mag
                            enemy.take_damage(player.attack, (dx, dy), knock_strength=6.0)

    keys = pygame.key.get_pressed()
    if not game_over:
        dx = (1 if keys[pygame.K_d] else 0) - (1 if keys[pygame.K_a] else 0)
        dy = (1 if keys[pygame.K_s] else 0) - (1 if keys[pygame.K_w] else 0)
        if dx != 0 or dy != 0:
            mag = (dx*dx + dy*dy) ** 0.5
            player.last_move_dir = (dx / mag, dy / mag)
        if dash_pressed:
            player.try_dash((dx, dy))


        # --- Raum-Blockier-Logik ---
        # Trigger: Spieler betritt Bereich (hier: x > 300 und y zwischen 224 und 320)
        if not room_blocked and 224 <= player.y < 320 and player.x > 300:
            if not spawn_timer_started and current_wave == 0:
                spawn_timer_started = True
                spawn_start_time = pygame.time.get_ticks()
            room_blocked = True

        # --- Extra Raum-Blockier-Logik (dein Bereich) ---
        # Trigger: Spieler durchquert Bereich (Reihe 17-20, Col 13)
        # Zeile 17-20 = y: 16*32 bis 19*32, Spalte 13 = x: 12*32 bis 13*32
        if not extra_room_triggered and (16*32 <= player.y < 20*32) and (12*32 <= player.x < 13*32):
            extra_room_triggered = True
            extra_room_entry_pos = (player.x, player.y)

        # --- Third Raum-Trigger ---
        # Trigger: Spieler betritt Bereich (Reihe 3-16, Col 29-42)
        if not third_room_triggered and (3*32 <= player.y < 16*32) and (29*32 <= player.x < 42*32):
            third_room_triggered = True
            if not third_room_spawn_timer_started and third_room_wave == 0:
                third_room_spawn_timer_started = True
                third_room_spawn_start_time = pygame.time.get_ticks()

        # --- Fourth Raum-Trigger ---
        # Trigger: Spieler betritt Bereich (Reihe 23-39, Col 17-26)
        if not fourth_room_triggered and (23*32 <= player.y < 39*32) and (17*32 <= player.x < 26*32):
            fourth_room_triggered = True
            if not fourth_room_spawn_timer_started and fourth_room_wave == 0:
                fourth_room_spawn_timer_started = True
                fourth_room_spawn_start_time = pygame.time.get_ticks()

        # --- Fifth Raum-Trigger ---
        # Trigger: Spieler betritt Bereich (Reihe 28-39, Col 31-60)
        if not fifth_room_triggered and (28*32 <= player.y < 39*32) and (31*32 <= player.x < 60*32):
            fifth_room_triggered = True
            if not fifth_room_spawn_timer_started and fifth_room_wave == 0:
                fifth_room_spawn_timer_started = True
                fifth_room_spawn_start_time = pygame.time.get_ticks()

        # --- Sixth Raum-Trigger ---
        # Trigger: Spieler betritt Bereich (Reihe 2-24, Col 48-60)
        if not sixth_room_triggered and (2*32 <= player.y < 24*32) and (48*32 <= player.x < 60*32):
            sixth_room_triggered = True

        # Interaktion mit E
        if keys[pygame.K_e]:
            # Check for chests
            chests_to_remove = []
            for chest in chests:
                if not chest.opened and player.rect.colliderect(chest.rect):
                    if chest.open():
                        # Drop health potion
                        items.append(Item(chest.x, chest.y, "health_potion"))
                        chests_to_remove.append(chest)
            for chest in chests_to_remove:
                # Ändere das Tile zu Boden
                for tile in map_manager.tiles:
                    if tile.rect.topleft == (chest.x, chest.y):
                        from tile import get_tile_image
                        tile.tile_id = 49
                        tile.image = get_tile_image(49, 32)
                        break
                chests.remove(chest)
            # Check for items
            for item in items[:]:  # Copy to avoid modification during iteration
                if not item.collected and player.rect.colliderect(item.rect):
                    if item.item_type == "health_potion":
                        player.hp = player.max_hp  # Fill health
                        item.collect()
            # Check for door to boss room
            door_rect = pygame.Rect(54 * 32, 1 * 32, 32, 32)
            if player.rect.colliderect(door_rect) and elite_defeated:
                # Raum wechseln zu Boss-Raum
                map_manager.load_map_from_csv("assets/tiles/maps/boss_room.csv")
                player.x, player.y = 1 * 32, 20 * 32  # Unten links im Boss-Raum
                enemies.clear()
                chests.clear()
                items.clear()
                # Boss spawnen
                enemies.append(Enemy(ENEMIES["boss"], (20 * 32, 10 * 32)))

        # Wand setzen und Wellen starten, wenn Spieler 2 Blöcke (64px) weitergelaufen ist
        if extra_room_triggered and not extra_room_blocked and not extra_room_cleared and extra_room_entry_pos is not None:
            dx = abs(player.x - extra_room_entry_pos[0])
            dy = abs(player.y - extra_room_entry_pos[1])
            if dx >= 64 or dy >= 64:
                enemies.append(Enemy(ENEMIES["ghost"], (2*32, 17*32)))   # links an der Wand oben
                enemies.append(Enemy(ENEMIES["bat"], (2*32, 28*32)))     # unten links 
                enemies.append(Enemy(ENEMIES["bat"], (11*32, 28*32)))    # unten rechts 
                extra_room_blocked = True
                extra_room_wave = 0
                extra_room_spawn_timer_started = True
                extra_room_spawn_start_time = pygame.time.get_ticks()


        # Wellen-Spawn-Logik
        if spawn_timer_started and not enemies and current_wave < max_waves:
            if pygame.time.get_ticks() - spawn_start_time >= spawn_delay:
                # Spawn-Positionen erst jetzt berechnen, damit Abstand zum Spieler stimmt
                types = ["ghost", "bat"]
                positions = get_spread_spawns(2, room1_rect, map_manager)
                for i, pos in enumerate(positions):
                    enemy_type = types[i]
                    enemies.append(Enemy(ENEMIES[enemy_type], pos))
                spawn_timer_started = False
                current_wave += 1

        # Starte nächste Welle, wenn alle Gegner besiegt wurden
        if not enemies and room_blocked and current_wave < max_waves and not spawn_timer_started:
            spawn_timer_started = True
            spawn_start_time = pygame.time.get_ticks()

        # Wellen-Spawn-Logik für Extra-Raum
        if extra_room_triggered and extra_room_spawn_timer_started and not enemies and extra_room_wave < extra_room_max_waves and not extra_room_cleared:
            if pygame.time.get_ticks() - extra_room_spawn_start_time >= extra_room_spawn_delay:
                if extra_room_wave == 0:
                    # Welle 1: 3 Gegner zufällig im Raum
                    positions = get_spread_spawns(3, extra_room_rect, map_manager)
                    enemies.append(Enemy(ENEMIES["ghost"], positions[0]))
                    enemies.append(Enemy(ENEMIES["rat"], positions[1]))
                    enemies.append(Enemy(ENEMIES["bat"], positions[2]))
                elif extra_room_wave == 1:
                    # Welle 2: 3 Gegner zufällig im Raum
                    positions = get_spread_spawns(3, extra_room_rect, map_manager)
                    enemies.append(Enemy(ENEMIES["ghost"], positions[0]))
                    enemies.append(Enemy(ENEMIES["bat"], positions[1]))
                    enemies.append(Enemy(ENEMIES["crab"], positions[2]))
                elif extra_room_wave == 2:
                    # Welle 3: 2 Bats zufällig im Raum
                    positions = get_spread_spawns(2, extra_room_rect, map_manager)
                    enemies.append(Enemy(ENEMIES["bat"], positions[0]))
                    enemies.append(Enemy(ENEMIES["bat"], positions[1]))
                extra_room_spawn_timer_started = False
                extra_room_wave += 1

        # Starte nächste Welle im Extra-Raum, wenn alle Gegner besiegt wurden
        if extra_room_triggered and not enemies and extra_room_wave < extra_room_max_waves and not extra_room_spawn_timer_started and not extra_room_cleared:
            extra_room_spawn_timer_started = True
            extra_room_spawn_start_time = pygame.time.get_ticks()

        # Wellen-Spawn-Logik für Third-Raum
        if third_room_triggered and third_room_spawn_timer_started and not enemies and third_room_wave < third_room_max_waves and not third_room_cleared:
            if pygame.time.get_ticks() - third_room_spawn_start_time >= third_room_spawn_delay:
                if third_room_wave == 0:
                    # Welle 1: 2 Ghosts
                    positions = get_spread_spawns(2, third_room_rect, map_manager)
                    enemies.append(Enemy(ENEMIES["ghost"], positions[0]))
                    enemies.append(Enemy(ENEMIES["cyclop"], positions[1]))
                elif third_room_wave == 1:
                    # Welle 2: 2 Bats
                    positions = get_spread_spawns(2, third_room_rect, map_manager)
                    enemies.append(Enemy(ENEMIES["rat"], positions[0]))
                    enemies.append(Enemy(ENEMIES["spider"], positions[1]))
                elif third_room_wave == 2:
                    # Welle 3: 1 Ghost + 1 Bat
                    positions = get_spread_spawns(2, third_room_rect, map_manager)
                    enemies.append(Enemy(ENEMIES["ghost"], positions[0]))
                    enemies.append(Enemy(ENEMIES["bat"], positions[1]))
                third_room_spawn_timer_started = False
                third_room_wave += 1

        # Starte nächste Welle im Third-Raum, wenn alle Gegner besiegt wurden
        if third_room_triggered and not enemies and third_room_wave < third_room_max_waves and not third_room_spawn_timer_started and not third_room_cleared:
            third_room_spawn_timer_started = True
            third_room_spawn_start_time = pygame.time.get_ticks()

        # Wellen-Spawn-Logik für Fourth-Raum
        if fourth_room_triggered and fourth_room_spawn_timer_started and not enemies and fourth_room_wave < fourth_room_max_waves and not fourth_room_cleared:
            if pygame.time.get_ticks() - fourth_room_spawn_start_time >= fourth_room_spawn_delay:
                if fourth_room_wave == 0:
                    # Welle 1: 2 Ghosts - einer oben, einer unten
                    enemies.append(Enemy(ENEMIES["ghost"], (21*32, 24*32)))  # oben (etwas höher)
                    enemies.append(Enemy(ENEMIES["cyclop"], (21*32, 37*32)))  # unten
                elif fourth_room_wave == 1:
                    # Welle 2: 2 Bats - einer oben, einer unten
                    enemies.append(Enemy(ENEMIES["bat"], (21*32, 24*32)))   # oben (etwas höher)
                    enemies.append(Enemy(ENEMIES["spider"], (21*32, 37*32)))   # unten
                fourth_room_spawn_timer_started = False
                fourth_room_wave += 1

        # Starte nächste Welle im Fourth-Raum, wenn alle Gegner besiegt wurden
        if fourth_room_triggered and not enemies and fourth_room_wave < fourth_room_max_waves and not fourth_room_spawn_timer_started and not fourth_room_cleared:
            fourth_room_spawn_timer_started = True
            fourth_room_spawn_start_time = pygame.time.get_ticks()

        # Wellen-Spawn-Logik für Fifth-Raum
        if fifth_room_triggered and fifth_room_spawn_timer_started and not enemies and fifth_room_wave < fifth_room_max_waves and not fifth_room_cleared:
            if pygame.time.get_ticks() - fifth_room_spawn_start_time >= fifth_room_spawn_delay:
                if fifth_room_wave == 0:
                    # Welle 1: 
                    positions = get_spread_spawns(5, fifth_room_rect, map_manager)
                    for pos in positions:
                        enemies.append(Enemy(ENEMIES["ghost"], pos))
                elif fifth_room_wave == 1:
                    # Welle 2: 
                    positions = get_spread_spawns(5, fifth_room_rect, map_manager)
                    for pos in positions:
                        enemies.append(Enemy(ENEMIES["spider"], pos))
                elif fifth_room_wave == 2:
                    # Welle 3: 
                    positions = get_spread_spawns(5, fifth_room_rect, map_manager)
                    enemies.append(Enemy(ENEMIES["ghost"], positions[0]))
                    enemies.append(Enemy(ENEMIES["cyclop"], positions[1]))
                    enemies.append(Enemy(ENEMIES["cyclop"], positions[2]))
                    enemies.append(Enemy(ENEMIES["spider"], positions[3]))
                    enemies.append(Enemy(ENEMIES["crab"], positions[4]))
                elif fifth_room_wave == 3:
                    # Welle 4: 
                    positions = get_spread_spawns(5, fifth_room_rect, map_manager)
                    enemies.append(Enemy(ENEMIES["ghost"], positions[0]))
                    enemies.append(Enemy(ENEMIES["ghost"], positions[1]))
                    enemies.append(Enemy(ENEMIES["crab"], positions[2]))
                    enemies.append(Enemy(ENEMIES["spider"], positions[3]))
                    enemies.append(Enemy(ENEMIES["bat"], positions[4]))
                fifth_room_spawn_timer_started = False
                fifth_room_wave += 1

        # Starte nächste Welle im Fifth-Raum, wenn alle Gegner besiegt wurden
        if fifth_room_triggered and not enemies and fifth_room_wave < fifth_room_max_waves and not fifth_room_spawn_timer_started and not fifth_room_cleared:
            fifth_room_spawn_timer_started = True
            fifth_room_spawn_start_time = pygame.time.get_ticks()

        # Sixth-Raum: Elite Ghost + 2 normale Ghosts spawnen
        if sixth_room_triggered and not sixth_room_spawned:
            # Elite Ghost: 3x HP, 2.5x Größe, 2x Schaden
            elite_ghost_data = ENEMIES["ghost"].copy()
            elite_ghost_data["hp"] = 168  # 3x normal (56*3)
            elite_ghost_data["size"] = 80  # 2.5x normale Größe (32*2.5)
            elite_ghost_data["damage"] = 24  # 2x normaler Schaden (12*2)
            # Spawn Elite in der Mitte weiter oben: Reihe 6, Spalte 54
            enemies.append(Enemy(elite_ghost_data, (54*32, 6*32)))
            
            # 2 normale Ghosts: einer links, einer rechts
            enemies.append(Enemy(ENEMIES["ghost"], (50*32, 8*32)))  # Links
            enemies.append(Enemy(ENEMIES["ghost"], (58*32, 8*32)))  # Rechts
            
            sixth_room_spawned = True

        # Wenn Raum blockiert, alle Gegner tot und alle Wellen vorbei -> Wände entfernen
        if room_blocked and not enemies and current_wave >= max_waves:
            room_blocked = False
        # Extra-Raum: Wenn alle Wellen vorbei und keine Gegner mehr da, entferne die neuen Wände
        if extra_room_triggered and not enemies and extra_room_wave >= extra_room_max_waves and not extra_room_cleared:
            extra_room_blocked = False
            extra_room_cleared = True
            extra_room_triggered = False
            extra_room_entry_pos = None
            extra_room_spawn_timer_started = False

        # Third-Raum: Wenn alle Wellen vorbei, cleared setzen
        if third_room_triggered and not enemies and third_room_wave >= third_room_max_waves and not third_room_cleared:
            third_room_cleared = True

        # Fourth-Raum: Wenn alle Wellen vorbei, cleared setzen
        if fourth_room_triggered and not enemies and fourth_room_wave >= fourth_room_max_waves and not fourth_room_cleared:
            fourth_room_cleared = True

        # Fifth-Raum: Wenn alle Wellen vorbei, cleared setzen
        if fifth_room_triggered and not enemies and fifth_room_wave >= fifth_room_max_waves and not fifth_room_cleared:
            fifth_room_cleared = True

        # Sixth-Raum: Wenn alle Gegner besiegt, cleared setzen und Elite defeated
        if sixth_room_triggered and not enemies and not sixth_room_cleared:
            sixth_room_cleared = True
            elite_defeated = True

        # Boss-Raum: Wenn Boss besiegt, Sieg!
        if not enemies and map_manager.current_map == "assets/tiles/maps/boss_room.csv":
            game_won = True

        # Sixth-Raum: cleared setzen wenn Elite-Gegner besiegt
        if sixth_room_triggered and not enemies and sixth_room_cleared:
            pass  # Bereits beim Spawnen gesetzt

        # --- ENDE Raum-Blockier-Logik ---

        # --- Sliding-Kollision: Nur blockierte Achse zurücksetzen ---
        old_x, old_y = player.x, player.y
        player.update(dt, keys)
        # X-Achse prüfen
        player.rect.topleft = (int(player.x), int(old_y))
        if map_manager.check_collision(player.rect):
            player.x = old_x
        # Y-Achse prüfen
        player.rect.topleft = (int(player.x), int(player.y))
        if map_manager.check_collision(player.rect):
            player.y = old_y
        player.rect.topleft = (int(player.x), int(player.y))
        # --- ENDE Sliding ---

        for enemy in enemies:
            # map_manager für Kollisionsabfrage an Enemy übergeben
            enemy.update(dt, player.rect, map_manager)
        # Entferne tote Gegner direkt nach dem Update
        enemies[:] = [e for e in enemies if e.alive]
        
        # Überprüfe ob Spieler tot ist
        if player.hp <= 0 and not game_over:
            game_over = True
            # Vorherigen Grabstein (Tile 131) entfernen, falls vorhanden
            for tile in list(map_manager.tiles):
                if hasattr(tile, 'tile_id') and tile.tile_id == 131:
                    map_manager.tiles.remove(tile)
            # Grabstein-Tile an Spielerposition hinzufügen
            from tile import Tile
            grabstein_tile = Tile(int(player.x), int(player.y), 131, map_manager.tile_size)
            map_manager.tiles.add(grabstein_tile)
    
    # Kamera aktualisieren
    camera.update(player.rect)

    # Kollisionen zwischen Spieler und Feinden
    for enemy in enemies:
       if not enemy.alive:
           continue
       if enemy.rect.colliderect(player.rect):
          if player.invuln_timer <= 0 and enemy.hit_timer <= 0:
               dx = player.rect.centerx - enemy.rect.centerx
               dy = player.rect.centery - enemy.rect.centery
               mag = (dx * dx + dy * dy) ** 0.5
               if mag != 0:
                   dx /= mag
                   dy /= mag
               player.take_damage(enemy.damage, (dx, dy), knock_strength=16.0)
               # Enemy Attack Cooldown Start
               enemy.hit_timer = enemy.hit_cooldown + 0.2 #extra delay nach hit

    screen.fill((30, 30, 30))
    
    # Map zeichnen (VOR dem Player!)
    map_manager.draw(screen, camera)
    
    player.draw(screen, camera)
    for enemy in enemies:
        enemy.draw(screen, camera)
    for chest in chests:
        screen_rect = camera.apply(chest.rect)
        if screen_rect.colliderect(screen.get_rect()):
            screen.blit(chest.image, screen_rect)
    for item in items:
        if not item.collected:
            screen_rect = camera.apply(item.rect)
            if screen_rect.colliderect(screen.get_rect()):
                screen.blit(item.image, screen_rect)
    
    # Kamera-Offsets auf UI-Elemente anwenden (sie bleiben fixed auf dem Bildschirm)
    hp_ratio = player.hp / player.max_hp
    resource_ratio = player.resource / player.max_resource

    hp_bar.draw(screen, hp_ratio)
    stamina_bar.draw(screen, resource_ratio)

    if game_over:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Schwarzes Overlay 
        screen.blit(overlay, (0, 0))
        font = pygame.font.SysFont(None, 72)
        small = pygame.font.SysFont(None, 36)
        text = font.render("Game Over", True, (255, 80, 80))
        hint = small.render("Press R to Restart or ESC to Quit", True, (220, 220, 220))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 60))
        screen.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, SCREEN_HEIGHT//2 + 10))

    if game_won:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Schwarzes Overlay 
        screen.blit(overlay, (0, 0))
        font = pygame.font.SysFont(None, 72)
        small = pygame.font.SysFont(None, 36)
        text = font.render("You Win!", True, (80, 255, 80))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 100))
        
        # Buttons
        restart_button = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 20, 120, 50)
        menu_button = pygame.Rect(SCREEN_WIDTH//2 + 30, SCREEN_HEIGHT//2 - 20, 120, 50)
        
        mouse_pos = pygame.mouse.get_pos()
        restart_color = (150, 150, 200) if restart_button.collidepoint(mouse_pos) else (100, 100, 150)
        menu_color = (150, 150, 200) if menu_button.collidepoint(mouse_pos) else (100, 100, 150)
        
        pygame.draw.rect(screen, restart_color, restart_button, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), restart_button, 2, border_radius=5)
        pygame.draw.rect(screen, menu_color, menu_button, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), menu_button, 2, border_radius=5)
        
        restart_text = small.render("Neustart", True, (255, 255, 255))
        menu_text = small.render("Menü", True, (255, 255, 255))
        screen.blit(restart_text, (restart_button.centerx - restart_text.get_width()//2, restart_button.centery - restart_text.get_height()//2))
        screen.blit(menu_text, (menu_button.centerx - menu_text.get_width()//2, menu_button.centery - menu_text.get_height()//2))

    pygame.display.flip()

pygame.quit()
