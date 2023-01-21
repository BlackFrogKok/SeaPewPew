import pygame
import sys

from field import Field
from shipChoice import ShipChoice


pygame.font.init()
CELL_SIZE = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font_size = int(CELL_SIZE / 1.5)


def main():
    pygame.init()
    bg = pygame.image.load("data/sprites/background.png")
    all_sprites = pygame.sprite.Group()
    screen = pygame.display.set_mode((1000, 750))
    score = 0
    font = pygame.font.SysFont('notosans', font_size)
    board1 = Field(50, 100, 0, 'Ваше поле')
    board2 = Field(50, board1.get_field_width() + 150, 11.3, 'Поле противника')
    ship_choice_bar = ShipChoice(all_sprites)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                sp = event.pos
                ship_choice_bar.start_motion(sp)
                x, y = event.pos
                if board2.check_click_corr(x, y):
                    board2.check_strike(x, y, screen)

            elif event.type == pygame.MOUSEMOTION and ship_choice_bar.get_motion_flag():
                pos = event.rel
                ship_choice_bar.motion(pos)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                sp = event.pos
                ship_choice_bar.stop_motion(sp, board1.check_click_corr, board1.set_ship)
        screen.blit(bg, (0, 0))
        board1.render(screen)
        board2.render(screen)
        score_render = font.render(f'Очки: {score}', True, WHITE)
        screen.blit(score_render, (490,  525))
        all_sprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
