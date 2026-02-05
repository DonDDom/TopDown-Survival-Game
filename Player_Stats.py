CHARACTERS = {
    "knight": {
        "sprite": "assets/images/player/knight.png",
        "hp": 150,
        "attack": 14,
        "speed": 4.0,
        "resource": "stamina",
        "resource_max": 100,
        "resource_regen": 5,
        "skill": {
            "name": "Dash",
            "cooldown": 3,
            "cost": 30,
            "description": "Quick dash to evade attacks or close distance."
        }
    },

    "mage": {
        "sprite": None, # Placeholder for mage sprite
        "hp": 100,
        "attack": 11,
        "speed": 4.6,
        "resource": "mana",
        "resource_max": 150,
        "resource_regen": 10,
        "skill": {
            "name": "Fire Nova",
            "cooldown": 5,
            "cost": 50,
            "description": "Unleash a burst of fire damaging nearby enemies."
        }
    }
    # Add more character classes if needed
}