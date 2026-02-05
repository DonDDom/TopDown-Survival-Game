import pygame
import csv
from tile import Tile

class MapManager:
    """Verwaltet Tiles und rendert die Map"""
    
    def __init__(self, tile_size=32):
        self.tile_size = tile_size
        self.tiles = pygame.sprite.Group()  # Boden/Wände
        self.decor_tiles = pygame.sprite.Group()  # Decken (werden oben gerendert)
        self.collision_map = {}  # Für schnelle Kollisionsprüfung
        self.current_map = None
    
    def load_map_from_csv(self, filepath):
        """
        Lädt eine Map aus einer CSV-Datei
        
        Tile-IDs:
        49 = Boden
        41 = Wand
        1, 13 = Decke (wird rings um Wände gerendert)
        """
        self.current_map = filepath
        self.tiles.empty()
        self.decor_tiles.empty()
        self.collision_map.clear()
        
        # Erste Pass: Lade alle Tiles
        tile_grid = {}  # Speichert Tile-IDs nach Position
        
        import random
        try:
            with open(filepath, 'r') as file:
                reader = csv.reader(file)
                y = 0
                for row in reader:
                    x = 0
                    for tile_id_str in row:
                        tile_id = int(tile_id_str) if tile_id_str.strip() else -1
                        # Randomly replace some normal floor tiles (49) with decorated floor (50)
                        if tile_id == 49 and random.random() < 0.08:
                            tile_id = 50
                        if tile_id >= 0:
                            tile_grid[(x, y)] = tile_id
                        x += 1
                    y += 1
            
            # Zweite Pass: Erstelle Tiles und place Decken
            for (x, y), tile_id in tile_grid.items():
                world_x = x * self.tile_size
                world_y = y * self.tile_size
                tile = Tile(world_x, world_y, tile_id, self.tile_size)
                
                # Decken nur hinzufügen wenn kein Wand-Tile schon da ist
                if tile_id in [1, 13]:
                    self.decor_tiles.add(tile)
                else:
                    self.tiles.add(tile)
                
                # Speichere Kollisionsinfo
                if not tile.is_walkable():
                    self.collision_map[(x, y)] = tile
            
            # Entfernt: Automatische Decken-Generierung um Wände
            total_tiles = len(self.tiles) + len(self.decor_tiles)
            print(f"Map geladen: {total_tiles} Tiles ({len(self.decor_tiles)} Decken)")
            
        except FileNotFoundError:
            print(f"Fehler: {filepath} nicht gefunden!")
            self._create_default_map()
    
    def _create_default_map(self):
        """Erstellt eine Test-Map wenn CSV nicht geladen werden kann"""
        width, height = 40, 22
        
        for y in range(height):
            for x in range(width):
                if x == 0 or x == width-1 or y == 0 or y == height-1:
                    tile_id = 41  # Wand
                else:
                    tile_id = 49  # Boden
                
                tile = Tile(x * self.tile_size, y * self.tile_size, tile_id, self.tile_size)
                self.tiles.add(tile)
    
    def draw(self, surface, camera):
        """Zeichnet alle Tiles: zuerst Boden/Wände, dann Decken"""
        # Boden und Wände
        for tile in self.tiles:
            screen_rect = camera.apply(tile.rect)
            if screen_rect.colliderect(surface.get_rect()):
                surface.blit(tile.image, screen_rect)
        
        # Decken oben drüber
        for tile in self.decor_tiles:
            screen_rect = camera.apply(tile.rect)
            if screen_rect.colliderect(surface.get_rect()):
                surface.blit(tile.image, screen_rect)
    
    def check_collision(self, rect):
        for tile in self.tiles:
            if not tile.is_walkable() and rect.colliderect(tile.rect):
                return True
        return False
    
    def get_map_width(self):
        """Gibt die Breite der Map in Pixeln zurück"""
        all_tiles = list(self.tiles) + list(self.decor_tiles)
        if all_tiles:
            max_x = max(tile.rect.right for tile in all_tiles)
            return max_x
        return 0
    
    def get_map_height(self):
        """Gibt die Höhe der Map in Pixeln zurück"""
        all_tiles = list(self.tiles) + list(self.decor_tiles)
        if all_tiles:
            max_y = max(tile.rect.bottom for tile in all_tiles)
            return max_y
        return 0
