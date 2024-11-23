class Settings():
	"""A class to store all settings for Alien Invasion."""

	def set_dynamic_settings(self):
		"""Initialize and reset dynamic settings."""
		self.level_speed_increase = 1 #1
		self.bullet_speed_factor = 3 #3
		self.ship_speed_factor = 1.5 #1.5
		self.alien_speed_factor = 1 #1
		self.fleet_drop_speed = 3 #3
		self.fleet_direction = 1 #1 | fleet_direction of 1 represents right; -1 represents left.

	def __init__(self):
		"""Initialize the game's settings"""
		# Screen settings
		self.screen_width = 1200 #1200
		self.screen_height = 800 # 800
		self.bg_color = (230, 230, 230) # 230, 230, 230

		# Ship settings
		self.ship_limit = 2 #2

		# Bullet settings
		self.bullet_width = 3 #3
		self.bullet_height = 15 #15
		self.bullet_color = 60, 60, 60 #60, 60, 60
		self.bullets_allowed = 3 #3


		# Scoring
		self.alien_points = 50 #50
		self.score_scale = 1.2 #1.2

		# Play button problems.
		self.back_bullet = 3 #3
		self.back_ship = 1.5 #1.5
		self.back_alien = 1 #1
		Settings.set_dynamic_settings(self)