import pygame
import sys

from field import Field


def main():
    pygame.init()
    bg = pygame.image.load("data/sprites/background.png")
    screen = pygame.display.set_mode((1000, 600))
    board1 = Field(10, 100)
    board2 = Field(10, board1.getFieldWidth() + 150)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        screen.blit(bg, (0, 0))
        board1.render(screen)
        board2.render(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
