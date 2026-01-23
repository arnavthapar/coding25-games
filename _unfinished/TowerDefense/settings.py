class Settings():
    def __init__(self):
        """Settings"""
        # Basic
        self.startingLevel = 1

        # Enemies
        self.ENEMY_SPEED = 2 #? pixels per frame (must be 1, 2, 4, 8, 16, 32, or 64)
        self.BASE_HEALTH = 5

        # Towers
        self.BASE_BULLET_SPEED = 2 #? best options are 1, 2, 4, and 8, as others can go through enemies