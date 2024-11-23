import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf

# LEADERBOARD
# ADVIKA'S HIGH SCORE: 33836
# GAUTAUM'S HIGH SCORE: 34078
# ARNAV'S HIGH SCORE: 39581

def run_game():
	# Initialize pygame, setting, and screen object.
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	play_button = Button(ai_settings, screen, "Play")
	# Create an instance to store game statistics and make a scoreboard.
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)

	# Make a ship, a group of bullets, and a group of aliens.
	ship = Ship(ai_settings, screen)
	bullets = Group()
	aliens = Group()

	# Create the fleet of aliens.
	gf.create_fleet(ai_settings, screen, ship, aliens)

	# Start the main loop for the game.
	GameStats.game_active = False
	gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

	while True:
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
			gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
			gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()
