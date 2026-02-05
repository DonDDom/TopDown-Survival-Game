ENEMIES = {
    "ghost": {
        "hp": 56,
        "speed": 2.6,
        "damage": 12,
        "xp": 8,
        "sprite": "assets/images/enemy/ghost.png",
        "hit_cooldown": 0.8
    },
    "cyclop": {
        "hp": 120,
        "speed": 1.6,
        "damage": 22,
        "xp": 25,
        "sprite": "assets/images/enemy/cyclop.png",
        "hit_cooldown": 1.2
    },
    "crab": {
        "hp": 55,
        "speed": 1.9,
        "damage": 14,
        "xp": 12,
        "sprite": "assets/images/enemy/crab.png",
        "hit_cooldown": 0.9
    },
    "bat": {
        "hp": 25,
        "speed": 2.8,
        "damage": 8,
        "xp": 6,
        "sprite": "assets/images/enemy/bat.png",
        "hit_cooldown": 0.8
    },
    "spider": {
        "hp": 40,
        "speed": 2.3,
        "damage": 10,
        "xp": 9,
        "sprite": "assets/images/enemy/spider.png",
        "hit_cooldown": 0.7
    },
    "rat": {
        "hp": 20,
        "speed": 2.8,
        "damage": 7,
        "xp": 5,
        "sprite": "assets/images/enemy/rat.png",
        "hit_cooldown": 0.4
    },
    "boss": {
        "hp": 500,
        "speed": 2.3,
        "damage": 35,
        "xp": 100,
        "sprite": "assets/images/boss/boss_room1.png",
        "hit_cooldown": 1.5,
        "size": 80,
        "rush_cooldown": 5.0,  # Sekunden zwischen Rushes
        "rush_windup": 0.5,    # Windup-Zeit
        "rush_speed": 12.0,    # Dash-Geschwindigkeit
        "rush_duration": 0.3   # Dash-Dauer
    },
    # Add more enemy types as needed
}
