import pygame

WIDTH = 10
HEIGHT = 10
CELL_SIZE = 40
FIELD_COLOR = pygame.Color('white')


class Field:
    def __init__(self, top, left):
        self.width = WIDTH
        self.height = HEIGHT
        self.board = [[0] * self.width for _ in range(self.height)]
        self.left = left
        self.top = top
        self.cell_size = CELL_SIZE

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, FIELD_COLOR, (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size), 1)

    def getFieldWidth(self):
        return self.cell_size * self.width

