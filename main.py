import pygame
import sys

from field import Field


pygame.font.init()
CELL_SIZE = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font_size = int(CELL_SIZE / 1.5)


def main():
    pygame.init()
    bg = pygame.image.load("data/sprites/background.png")
    screen = pygame.display.set_mode((1000, 600))
    score = 0

    font = pygame.font.SysFont('notosans', font_size)
    board1 = Field(50, 100, 0, 'Ваше поле')
    board2 = Field(50, board1.getFieldWidth() + 150, 11.3, 'Поле противника')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if board2.check_click_corr(x, y):
                    board2.check_strike(x, y, screen)
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        screen.blit(bg, (0, 0))
        board1.render(screen)
        board2.render(screen)
        score_render = font.render(f'Очки: {score}', True, WHITE)
        screen.blit(score_render, (490,  525))
        pygame.display.flip()


if __name__ == '__main__':
    main()
