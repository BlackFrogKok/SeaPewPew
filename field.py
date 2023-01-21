import pygame


pygame.font.init()
WIDTH = 10
HEIGHT = 10
CELL_SIZE = 40
FIELD_COLOR = pygame.Color('white')
font_size = int(CELL_SIZE / 1.5)
font = pygame.font.SysFont('notosans', font_size)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
left_margin = 2.5 * CELL_SIZE
upper_margin = 1.3 * CELL_SIZE
LETTERS = "ABCDEFGHIJ"




class Field:
    def __init__(self, top, left, offset, title):
        self.width = WIDTH
        self.height = HEIGHT
        self.board = [[0] * self.width for _ in range(self.height)]
        self.left = left
        self.top = top
        self.cell_size = CELL_SIZE
        self.offset = offset
        self.title = title


    def render(self, screen):

        #отрисовка названий полей
        if self.offset > 0:
            player = font.render('Поле противника', True, WHITE)
            sign_width = player.get_width()
            screen.blit(player, (self.left + 125, self.top - 20))
        else:
            player = font.render('Ваше поле', True, WHITE)
            sign_width = player.get_width()
            screen.blit(player, (self.left + 150, self.top - 20))

        #отрисовка клеток
        for y in range(self.height):
            for x in range(self.width):
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


        #отрисовка цифр и букв
        for i in range(10):

            num_ver = font.render(str(i + 1), True, WHITE)
            letters_hor = font.render(LETTERS[i], True, WHITE)
            num_ver_width = num_ver.get_width()
            num_ver_height = num_ver.get_height()
            letters_hor_width = letters_hor.get_width()

            # Numbers (vertical)
            screen.blit(num_ver, (left_margin - (CELL_SIZE // 2 + num_ver_width // 2) + self.offset * CELL_SIZE,
                                  upper_margin + i * CELL_SIZE + (CELL_SIZE // 2 - num_ver_height // 2)))
            # Letters (horizontal)
            screen.blit(letters_hor, (left_margin + i * CELL_SIZE + (CELL_SIZE // 2 -
                                                                      letters_hor_width // 2) + self.offset * CELL_SIZE, upper_margin + 10 * CELL_SIZE))

    def check_strike(self, x, y, screen):
        x_cells = (x - self.left) // CELL_SIZE
        y_cells = (y - self.top) // CELL_SIZE
        if self.board[y_cells][x_cells] == 0:
            self.board[y_cells][x_cells] = 2
        if self.board[y_cells][x_cells] == 1:
            self.board[y_cells][x_cells] = 3

    def check_click_corr(self, x, y):
        if self.left <= x <= self.left + CELL_SIZE * WIDTH and self.top <= y <= self.top + CELL_SIZE * HEIGHT:
            return True
        else:
            return False

    def get_field_width(self):
        return self.cell_size * self.width

    def get_field_height_coord(self):
        return self.cell_size * self.height + self.top

    def set_ship(self, x, y):
        x_cells = (x - self.left) // CELL_SIZE
        y_cells = (y - self.top) // CELL_SIZE

        return self.left + x_cells * CELL_SIZE - 5, self.top + y_cells * CELL_SIZE

