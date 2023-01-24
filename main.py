import pygame
import sys

from field import Field
from shipChoice import ShipChoice
import button


pygame.font.init()
CELL_SIZE = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font_size = int(CELL_SIZE / 1.5)


def start_screen():
    res = width, height = (640, 512)

    fps = 60
    fpsClock = pygame.time.Clock()

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


    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()

        for object in button.objects:
            object.process()

        pygame.display.flip()
        fpsClock.tick(fps)
        pygame.display.update()


def main():
    pygame.init()
    start_screen()


def new_game():
    pygame.mixer.music.stop()
    ships_setup = True
    bg = pygame.image.load("data/sprites/background.png")
    all_sprites = pygame.sprite.Group()
    screen = pygame.display.set_mode((1500, 750))
    score = 0
    font = pygame.font.SysFont('notosans', font_size)
    board1 = Field(50, 100, 0, 'Ваше поле')
    board2 = Field(50, board1.get_field_width() + 250, 13, 'Поле противника')
    ship_choice_bar = ShipChoice(all_sprites)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                sp = event.pos
                if ships_setup:
                    ship_choice_bar.start_motion(sp)
                else:
                    x, y = event.pos
                    if board2.check_click_corr(x, y):
                        board2.check_strike(x, y, screen)

            elif event.type == pygame.MOUSEMOTION and ship_choice_bar.get_motion_flag():
                pos = event.rel
                ship_choice_bar.motion(pos)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and ship_choice_bar.get_motion_flag():
                sp = event.pos
                ship_choice_bar.stop_motion(sp, board1.check_click_corr, board1.set_ship)
        screen.blit(bg, (0, 0))
        board1.render(screen)
        board2.render(screen)
        score_render = font.render(f'Очки: {score}', True, WHITE)
        screen.blit(score_render, (620, 600))
        all_sprites.draw(screen)
        pygame.display.flip()





if __name__ == '__main__':
    main()
