class Settings():
    def __init__(self):
        """ Settings """
        # Bullets
        self.bullet_color = (255, 255, 255) # RGB Value
        self.homing_bullet_color = (255, 255, 0) # RGB Value
        self.bullet_time = 50 # Time between bullets without any upgrades

        # Enemies
        self.enemy_cooldown = 70 # Cooldown at start
        self.enemy_health = 1 # Health at start

        # Time
        self.time = 300 # How long the game is in seconds