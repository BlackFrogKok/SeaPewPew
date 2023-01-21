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




    def getFieldWidth(self):
        return self.cell_size * self.width

