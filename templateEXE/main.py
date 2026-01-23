import sys
import os
import pygame

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def main():
    pygame.init()
    pygame.mixer.init()

    SCREEN_W, SCREEN_H = 1216, 768
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("My Game")

    clock = pygame.time.Clock()

    from TowerDefense.tower import Game

    game = Game(screen, clock, resource_path)
    game.run()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()