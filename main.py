import pygame
import sys

from field import Field
from shipChoice import ShipChoice
from button import Button

pygame.font.init()
CELL_SIZE = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font_size = int(CELL_SIZE / 1.5)
INTERVAL = 150


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

    dog_surf_nad = pygame.image.load('data/sprites/mrboi2.png')
    dog_rect_nad = dog_surf_nad.get_rect(
        bottomright=(120, 100))
    sc.blit(dog_surf_nad, dog_rect)

    pygame.mixer.music.load("data/music/noize.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    buttons = [Button(175, 150, 300, 100, 'Играть!', onclickFunction=new_game),
               Button(175, 270, 300, 100, 'Об авторах')]

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()

        for object in buttons:
            object.process(screen)

        pygame.display.flip()
        fps_clock.tick(fps)
        pygame.display.update()


def main():
    pygame.init()
    start_screen()


def new_game():
    pygame.mixer.music.stop()
    pygame.init()
    ships_setup = True
    bg = pygame.image.load("data/sprites/background.png")
    all_sprites = pygame.sprite.Group()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    score = 0
    font = pygame.font.SysFont('notosans', font_size)
    board1 = Field(50, 100, 0, 'Ваше поле')
    board2 = Field(50, board1.get_field_width() + INTERVAL, 11.3, 'Поле противника')
    ship_choice_bar = ShipChoice(all_sprites, board1.get_field_height())
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                sp = event.pos
                if ships_setup:
                    ship_choice_bar.start_motion(sp, board1.del_ship)
                else:
                    x, y = event.pos
                    if board2.check_click_corr(x, y):
                        board2.check_strike(x, y)

            elif event.type == pygame.MOUSEMOTION and ship_choice_bar.get_motion_flag():
                pos = event.rel
                ship_choice_bar.motion(pos)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and ship_choice_bar.get_motion_flag():
                sp = event.pos
                ship_choice_bar.stop_motion(sp, board1.check_click_corr,
                                            board1.set_ship, board1.check_collision_ship)
        screen.blit(bg, (0, 0))
        board1.render(screen)
        board2.render(screen)
        score_render = font.render(f'Очки: {score}', True, WHITE)
        screen.blit(score_render, (board1.get_field_width() + INTERVAL // 4, board1.get_field_height()))
        all_sprites.draw(screen)
        ship_choice_bar.render(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
