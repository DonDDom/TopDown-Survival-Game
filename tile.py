import pygame

# Cache für geladene Bilder
_image_cache = {}

def get_tile_image(tile_id, tile_size=32):
    """Lädt das Bild für einen Tile-Typ"""
    if tile_id in _image_cache:
        return _image_cache[tile_id]
    
    # Mapping von Tile-ID zu Dateiname
    tile_files = {
            # Zaun (Fence)
            140: "assets/images/tiles/zaun_links.png",
            141: "assets/images/tiles/zaun_mitte.png",
            142: "assets/images/tiles/zaun_rechts.png",
        # Basis Tiles
        49: "assets/images/tiles/boden.png",
        41: "assets/images/tiles/wand.png",
        1: "assets/images/tiles/decke.png",
        13: "assets/images/tiles/decke.png",

        # Böden mit Dekor
        50: "assets/images/tiles/boden_mit_dekor_steinen.png",
        
        #chest
        45: "assets/images/chest/chest.png",
        # Decken Varianten
        51: "assets/images/tiles/decke_mit_flecken.png",
        52: "assets/images/tiles/decke_mit_steine.png",

        # Wand Dekoration
        60: "assets/images/tiles/wand_mit_decke_(ecke _oben_links).png",
        61: "assets/images/tiles/wand_mit_decke_(ecke_oben_rechts).png",
        62: "assets/images/tiles/wand_mit_decke_(unten_links).png",
        63: "assets/images/tiles/wand_mit_decke_(unten_rechts).png",
        64: "assets/images/tiles/wand_mit_banner_(dekor).png",
        65: "assets/images/tiles/wand_mit_loch_(dekor).png",
        66: "assets/images/tiles/wand_deckor_(mit_wasser).png",
        67: "assets/images/tiles/wand_deckor_(ohne_wasser).png",
        68: "assets/images/tiles/wand_mit_dekor_kopf.png",
        69: "assets/images/tiles/wand_mit_dekor_kopf_mit_wasser.png",
        70: "assets/images/tiles/wand_abschnitt_links_(nur_kombinierbar_mit_abschnitt_rechts).png",
        71: "assets/images/tiles/wand_abschnitt_rechts_(nur_kombinierbar_mit_abschnitt_links).png",

        # Säulen
        80: "assets/images/tiles/saeule_mit_boden(nur_mit_den_anderen_saeulen_kombinierbar).png",
        81: "assets/images/tiles/saeule_mit_wand_(nur_mit_den_anderen_saeulen_kombinierbar).png",
        82: "assets/images/tiles/saeule_mit_decke_und_wand_(oberer_teil)_(nur_mit_den_anderen_saeulen_kombinierbar).png",

        # Türen und Durchgänge
        90: "assets/images/tiles/durchgang_einzelnd.png",
        91: "assets/images/tiles/durchgang_doubledoor_links(nicht_durchgehbar).png",
        92: "assets/images/tiles/durchgang_doubledoor_rechts(nicht_durchgehbar).png",
        93: "assets/images/tiles/wand_mit_tür_(nicht_begehbar)_offen.png",
        94: "assets/images/tiles/wand_mit_doubledoor_links_offen_(nicht_begehbar).png",
        95: "assets/images/tiles/wand_mit_doubledoor_rechts_offen_(nicht_begehbar).png",

        # Treppen
        100: "assets/images/tiles/treppe_links.png",
        101: "assets/images/tiles/treppe_mitte.png",
        102: "assets/images/tiles/treppe_rechts.png",

        # Möbel
        110: "assets/images/tiles/tisch.png",
        111: "assets/images/tiles/stuhl_für_tisch.png",

        # Behälter und zerstörbare Objekte
        120: "assets/images/tiles/box(zerstoerbar).png",
        121: "assets/images/tiles/fass_zerstoerbar.png",

        # Dekor und Fallen
        130: "assets/images/tiles/grabstein_dekor.png",
        131: "assets/images/tiles/grabstein_mit_kreuz(kommt_wenn_der_maincharacter_stirbt).png",
        132: "assets/images/tiles/stachel_falle_(man_bekommt_schaden_beim_durchgehen).png",
    }
    
    if tile_id not in tile_files:
        # Fallback wenn Tile-ID unbekannt
        img = pygame.Surface((tile_size, tile_size))
        img.fill((100, 100, 100))
        return img
    
    try:
        img = pygame.image.load(tile_files[tile_id])
        img = pygame.transform.scale(img, (tile_size, tile_size))
        _image_cache[tile_id] = img
        return img
    except Exception as e:
        # Fallback wenn Datei nicht geladen werden kann
        print(f"Fehler beim Laden von Tile {tile_id}: {e}")
        img = pygame.Surface((tile_size, tile_size))
        img.fill((150, 0, 0))
        return img

class Tile(pygame.sprite.Sprite):
    """Einzelnes Tile für die Map"""
    def __init__(self, x, y, tile_id, tile_size=32):
        super().__init__()
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.tile_id = tile_id
        
        # Lade Tile-Bild
        self.image = get_tile_image(tile_id, tile_size)
        self.rect = self.image.get_rect(topleft=(x, y))
        
    def is_walkable(self):
        """Bestimmt, ob ein Tile begehbar ist"""
        # Nicht begehbar: Wände, Türen, Durchgänge, Möbel, Fallen
        non_walkable = [
            41,  # Wand
            60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,  # Wand Dekor
            80, 81, 82,  # Säulen
            90, 91, 92, 93, 94, 95,  # Türen/Durchgänge
            110, 111,  # Möbel (Tisch, Stuhl)
            120, 121,  # Behälter (Box, Fass)
            132,  # Stachelfalle
            140, 141, 142,  # Zaun
        ]
        return self.tile_id not in non_walkable
