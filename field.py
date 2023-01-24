import pygame
import button

pygame.font.init()
WIDTH = 10
HEIGHT = 10
CELL_SIZE = 50
FIELD_COLOR = pygame.Color('white')
font_size = int(CELL_SIZE / 1.5)
font = pygame.font.SysFont('notosans', font_size)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LETTERS = "ABCDEFGHIJ"
explosionImg = pygame.image.load('data/sprites/Explosion.png')


class Field:
    def __init__(self, top, left, offset, title):
        self.board = [[1] * WIDTH for _ in range(HEIGHT)]
        self.left = left
        self.top = top
        self.cell_size = CELL_SIZE
        self.offset = offset
        self.title = title
        self.ships = []

    def render(self, screen):

        # отрисовка названий полей
        if self.offset > 0:
            player = font.render('Поле противника', True, WHITE)
            sign_width = player.get_width()
            screen.blit(player, (self.left + 155, self.top - 30))
        else:
            player = font.render('Ваше поле', True, WHITE)
            sign_width = player.get_width()
            screen.blit(player, (self.left + 190, self.top - 30))

        # отрисовка клеток
        for y in range(HEIGHT):
            for x in range(WIDTH):
                pygame.draw.rect(screen, FIELD_COLOR, (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size), 1)
                if self.board[y][x] == 2:
                    pygame.draw.circle(screen, WHITE, (
                        x * self.cell_size + self.left + self.cell_size // 2,
                        y * self.cell_size + self.top + self.cell_size // 2),
                                       4)
                if self.board[y][x] == 3:
                    pygame.draw.line(screen, WHITE,
                                     (x * self.cell_size + self.left + 3, y * self.cell_size + self.top + 3),
                                     (x * self.cell_size + self.left + self.cell_size - 5,
                                      y * self.cell_size + self.top + self.cell_size - 4), width=4)
                    pygame.draw.line(screen, WHITE,
                                     (x * self.cell_size + self.left + 3,
                                      y * self.cell_size + self.top + self.cell_size - 4),
                                     (x * self.cell_size + self.left + self.cell_size - 5,
                                      y * self.cell_size + self.top + 3), width=4)
                    # отрисовка взрыва
                    screen.blit(explosionImg, (x * self.cell_size + self.left, y * self.cell_size + self.top))

        # отрисовка цифр и букв
        for i in range(10):
            num_ver = font.render(str(i + 1), True, WHITE)
            letters_hor = font.render(LETTERS[i], True, WHITE)
            num_ver_width = num_ver.get_width()
            num_ver_height = num_ver.get_height()
            letters_hor_width = letters_hor.get_width()

            # Numbers (vertical)
            screen.blit(num_ver, (self.left - CELL_SIZE // 2,
                                  CELL_SIZE * i + self.top + CELL_SIZE // 3))
            # Letters (horizontal)
            screen.blit(letters_hor, (CELL_SIZE * i + self.left + CELL_SIZE // 4,
                                      self.top + CELL_SIZE * HEIGHT + CELL_SIZE // 4))

    def check_strike(self, x, y):
        x_cells = (x - self.left) // CELL_SIZE
        y_cells = (y - self.top) // CELL_SIZE
        if self.board[y_cells][x_cells] == 0:
            self.board[y_cells][x_cells] = 2
        elif self.board[y_cells][x_cells] == 1:
            self.board[y_cells][x_cells] = 3

    def check_click_corr(self, x, y):
        if self.left <= x <= self.left + CELL_SIZE * WIDTH and self.top <= y <= self.top + CELL_SIZE * HEIGHT:
            return True
        else:
            return False

    def get_field_width(self):
        return self.cell_size * HEIGHT + self.left

    def get_field_height(self):
        return self.cell_size * HEIGHT + self.top + 50

    def set_ship(self, x, y, len_ship):
        x_cells = (x - self.left) // CELL_SIZE
        y_cells = (y - self.top) // CELL_SIZE
        self.ships.append((x_cells, y_cells, len_ship))
        for i in range(y_cells, y_cells + len_ship):
            self.board[i][x_cells] = 1
        self.update_ship_area()
        return self.left + x_cells * CELL_SIZE, self.top + y_cells * CELL_SIZE

    def del_ship(self, x, y, len_ship):
        x_cells = (x - self.left) // CELL_SIZE
        y_cells = (y - self.top) // CELL_SIZE
        for y1 in range(y_cells - 1, y_cells + len_ship + 1):
            for x1 in range(x_cells - 1, x_cells + 2):
                if x1 < 0 or y1 < 0 or x1 > WIDTH - 1 or y1 > HEIGHT - 1:
                    continue
                self.board[y1][x1] = 0
        self.ships.remove((x_cells, y_cells, len_ship))
        self.update_ship_area()

    def check_collision_ship(self, x, y):
        x_cells = (x - self.left) // CELL_SIZE
        y_cells = (y - self.top) // CELL_SIZE
        return True if self.board[y_cells][x_cells] == 0 else False

    def update_ship_area(self):
        for i in self.ships:
            for y1 in range(i[1] - 1, i[1] + i[2] + 1):
                for x1 in range(i[0] - 1, i[0] + 2):
                    if x1 < 0 or y1 < 0 or x1 > WIDTH - 1 or y1 > HEIGHT - 1:
                        continue
                    elif self.board[y1][x1] == 1:
                        continue
                    self.board[y1][x1] = 2


'''    def debug_board(self):
        for i in self.board:
            for i2 in i:
                print(i2, end=' ')
            print()
        print()'''
