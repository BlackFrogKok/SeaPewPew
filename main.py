import pygame
import sys

from field import Field
from shipChoice import ShipChoice
from button import Button
from bot import Bot
from const import *

creators = False
ships_setup = True

pygame.font.init()


def start_screen():
    res = width, height = (640, 512)
    fps = 60
    fps_clock = pygame.time.Clock()
    sc = pygame.display.set_mode((width, height))
    screen = pygame.display.set_mode(res)
    dog_surf = pygame.image.load('data/sprites/mor.gif')
    dog_rect = dog_surf.get_rect(
        bottomright=(width, height))
    sc.blit(dog_surf, dog_rect)

    if not creators:
        dog_surf_nad = pygame.image.load('data/sprites/mrboi2.png')
        dog_rect_nad = dog_surf_nad.get_rect(
            bottomright=(120, 100))
        sc.blit(dog_surf_nad, dog_rect)

    pygame.mixer.music.load("data/music/noize.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    buttons = [Button(175, 150, 300, 100, 'Играть!', onclickFunction=new_game),
               Button(175, 270, 300, 100, 'Об авторах', onclickFunction=creators_change), ]

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
        if not creators:
            for button in buttons:
                button.process(screen)
        if creators:
            table_creators_surf = pygame.image.load('data/sprites/table2.png')
            table_creators_rect = table_creators_surf.get_rect(
                bottomright=(500, 500))
            sc.blit(table_creators_surf, (120, 0))
        pygame.display.flip()
        fps_clock.tick(fps)
        pygame.display.update()


def creators_change():
    global creators
    creators = True


def main():
    pygame.init()
    start_screen()



def end_screen(vic_or_def):
    res = width, height = (640, 512)
    fps = 60
    fps_clock = pygame.time.Clock()
    sc = pygame.display.set_mode((width, height))
    global screen
    screen = pygame.display.set_mode(res)
    dog_surf = pygame.image.load('data/sprites/background.png')
    dog_rect = dog_surf.get_rect(
        bottomright=(width, height))
    sc.blit(dog_surf, dog_rect)
    if vic_or_def:
        dog_surf_nad = pygame.image.load('data/sprites/Victory.png')
        dog_rect_nad = dog_surf_nad.get_rect(
            bottomright=(600, 250))
        sc.blit(dog_surf_nad, (20, 50))
    else:
        dog_surf_nad = pygame.image.load('data/sprites/Defeat.png')
        dog_rect_nad = dog_surf_nad.get_rect(
            bottomright=(600, 250))
        sc.blit(dog_surf_nad, (20, 50))

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
        pygame.display.flip()
        fps_clock.tick(fps)
        pygame.display.update()


def change_stat(val):
    global ships_setup
    ships_setup = val


def show_go_screen(screen):
    run = True
    bg = pygame.image.load("data/sprites/background.png")
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # if the user hits the mouse button
                run = False

        # This will draw text displaying the score to the screen.
        screen.blit(bg, (0, 0))
        largeFont = pygame.font.SysFont('comicsans', 80)  # creates a font object
        lastScore = largeFont.render('Best Score: ' + str(100), 1,
                                     (255, 255, 255))  # We will create the function updateFile later
        currentScore = largeFont.render('Score: ' + str(50), 1, (255, 255, 255))
        screen.blit(lastScore, (screen.get_width() / 2 - lastScore.get_width() / 2, 150))
        screen.blit(currentScore, (screen.get_width() / 2 - currentScore.get_width() / 2, 240))
        pygame.display.update()
        end_screen(True)
    score = 0


def new_game():
    pygame.mixer.music.stop()
    pygame.init()

    score = 0
    bg = pygame.image.load("data/sprites/background.png")
    all_sprites = pygame.sprite.Group()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    font = pygame.font.SysFont('notosans', FONT_SIZE)
    board1 = Field(50, 100, 0, 'Ваше поле')
    board2 = Field(50, board1.get_field_width() + INTERVAL_BOARD, 11.3, 'Поле противника')

    bot = Bot(board2.check_collision_ship, board2.set_ship)
    bot.auto_set_ships()

    ship_choice_bar = ShipChoice(all_sprites, board1.get_field_height(), change_stat)

    button_close = Button(screen.get_width() - 60, 10, 50, 50,
                          icon=pygame.image.load('data/sprites/img3.png'), onclickFunction=pygame.quit)

    while True:
        if board2.get_ships_count() == 0 or board1.get_ships_count() == 0 and not ships_setup:
            show_go_screen(screen)
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                sp = event.pos
                if ships_setup:
                    ship_choice_bar.start_motion(sp, board1.del_ship)
                else:
                    x, y = event.pos
                    if board2.check_click_corr(x, y):
                        board2.check_strike(x, y)

            if event.type == pygame.MOUSEMOTION and ship_choice_bar.get_motion_flag():
                pos = event.rel
                ship_choice_bar.motion(pos)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and ship_choice_bar.get_motion_flag():
                sp = event.pos
                ship_choice_bar.stop_motion(sp, board1.check_click_corr,
                                            board1.set_ship, board1.check_collision_ship)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c \
                    and ship_choice_bar.current_ship is not None:
                ship_choice_bar.rotate_ship()
        screen.blit(bg, (0, 0))
        board1.render(screen)
        board2.render(screen)
        score_render = font.render(f'Очки: {score}', True, WHITE)
        screen.blit(score_render, (board1.get_field_width() + INTERVAL // 4, board1.get_field_height()))
        all_sprites.draw(screen)
        button_close.process(screen)
        ship_choice_bar.render(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
