from enum import Enum
import pygame

CELL_SIZE = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = int(CELL_SIZE / 1.5)
INTERVAL_BOARD = 200
INTERVAL = 50
MARGIN_LEFT = 100
WIDTH_BOARD = 10
HEIGHT_BOARD = 10

arrow_player = pygame.transform.scale(pygame.image.load('data/sprites/arrow.png'), (80, 50))
arrow_bot = pygame.transform.rotate(arrow_player, 180)


class shipOrientation(Enum):
    NORMAL = 0
    ROTATE = 1


class BoardStat(Enum):
    NOTHING = 0
    MISS_SHOT = 1
    HARM = 2
    SHIP_AREA = 3
    DESTROYED_SHIP = 4


class gameStatus(Enum):
    ship_setup = 0
    player = 1
    bot = 2
    game_over = 3
