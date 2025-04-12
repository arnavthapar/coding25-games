import pygame
from math import floor
from player import Player
from enemy import Enemy
from text import Text
from settings import Settings
from projectile import Bullets
from level import Level
from wait import Wait
from random import randrange
from time import sleep
from sys import argv
# Version 1.0
def check_events(player:Player, bullet:Bullets, level_time:int):
    """Respond to keypresses."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_LEFT:
                    player.x_move = -player.speed
                case pygame.K_RIGHT:
                    player.x_move = player.speed
                case pygame.K_UP:
                    player.y_move = -player.speed
                case pygame.K_DOWN:
                    player.y_move = player.speed
                case pygame.K_a:
                    if bullet.level:
                        player, bullet = level.answer(0, player, bullet)
                        wait.leveled(level_time)
                case pygame.K_b:
                    if bullet.level:
                        player, bullet = level.answer(1, player, bullet)
                        wait.leveled(level_time)
        elif event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_LEFT:
                    player.x_move = 0
                case pygame.K_RIGHT:
                    player.x_move = 0
                case pygame.K_UP:
                    player.y_move = 0
                case pygame.K_DOWN:
                    player.y_move = 0
def randomize():
    pygame.mixer.music.load(f'sound/music{randrange(1, 4)}.mp3')
if __name__ == "__main__":
    if argv[-1] == "endless":
        endless = True
    else:
        endless = False
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    randomize()
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("ATTACK")
    background = pygame.image.load('images/Grass.png') # Background
    overlay = pygame.image.load('images/overlay.svg')
    wait = Wait()
    player = Player(screen)
    enemy = Enemy(screen)
    text = Text(screen)
    bullet = Bullets()
    level = Level(text)
    settings = Settings()
    enemy.randomize(endless, True)
    timed = False
    if settings.time < 1:
        raise ValueError("Time for game must be above 0.")
    elif settings.time % 60 != 0:
        raise ValueError("Time for game must be divisible by 60.")
    if not endless:
        min_top = floor(settings.time / 60)
        sec_top = floor(settings.time % 60)
        if sec_top == 0:
            min_top -= 1
            sec_top = 59
    leveled = 0

    """" Start Game """
    pygame.mixer.music.play()
    #x = True
    while 1:
        check_events(player, bullet, leveled)
        if not bullet.level:
            if (wait.check() >= settings.time) and not endless:
                timed = True
                break
            else:
                screen.blit(background, (0, 0))
                screen.blit(background, (500, 0))
                screen.blit(background, (0, 400))
                screen.blit(background, (500, 400))
                player.frame(enemy)
                enemy.randomize(wait, endless)
                enemy.frame(player.rect.x, player.rect.y, player.rect, wait)
                player.blitme()
                enemy.blitme()
                text.write(f"LV {player.lv} | {player.xp} XP/15 XP", 20, 20)
                text.write(f"{player.hp} HP /5 HP", 800, 20)
                mins = floor(wait.check() / 60)
                if not endless:
                    a = 59 - floor(wait.check() - mins * 60)
                    text.write(f"{min_top-mins}:{"0" + str(a) if a < 10 else a}", 467, 10)
                else:
                    a = floor(wait.check() - mins * 60)
                    text.write(f"{mins}:{"0" + str(a) if a < 10 else a}", 467, 10)
                leveled = bullet.shoot(screen, enemy.location, player, enemy, level)
                if player.hp < 1: break
            if not pygame.mixer.music.get_busy():
                randomize()
                pygame.mixer.music.play()
            pygame.display.flip()
            #x = False
    pygame.mixer.music.fadeout(5000)
    if not endless:
        x = f"{min_top-mins}:{"0" + str(a) if a < 10 else a}"
    else:
        x = f"{mins}:{"0" + str(a) if a < 10 else a}"
    if not timed:
        for i in range(6):
                sleep(0.01)
                screen.blit(background, (0, 0))
                screen.blit(background, (500, 0))
                screen.blit(background, (0, 400))
                screen.blit(background, (500, 400))
                player.blitme()
                enemy.blitme()
                text.write(f"LV {player.lv} | {player.xp} XP/15 XP", 20, 20)
                text.write(f"{player.hp} HP /10 HP", 800, 20)
                text.write(x, 467, 10)
                player.explode()
                pygame.display.flip()
    screen.blit(overlay, (0, 540))
    screen.blit(overlay, (716, 0))
    screen.blit(overlay, (716, 540))
    screen.blit(overlay, (0, 0))
    if timed:
        text.write(f"You Win!", 460, 300)
    else:
        text.write(f"You lose...", screen.get_rect().centerx - 40, 300)
        text.write(f"Your time was {x}.", screen.get_rect().centerx - 90, 400)
    while True:
        check_events(player, bullet, leveled)
        pygame.display.flip()