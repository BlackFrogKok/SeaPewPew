from const import *
from ship import Ship

pygame.font.init()

font = pygame.font.SysFont('notosans', FONT_SIZE)
LETTERS = "ABCDEFGHIJ"
explosionImg = pygame.image.load('data/sprites/Explosion2.png')


class Field:
    def __init__(self, top, left, offset, title):
        self.board = [[BoardStat.NOTHING] * WIDTH_BOARD for _ in range(HEIGHT_BOARD)]
        self.left = left
        self.top = top
        self.cell_size = CELL_SIZE
        self.offset = offset
        self.title = title
        self.ships = []

    def render_board(self, screen):

        # отрисовка названий полей
        if self.offset > 0:
            player = font.render('Поле противника', True, WHITE)
            screen.blit(player, (self.left + 155, self.top - 30))
        else:
            player = font.render('Ваше поле', True, WHITE)
            screen.blit(player, (self.left + 190, self.top - 30))

        # отрисовка клеток
        for y in range(HEIGHT_BOARD):
            for x in range(WIDTH_BOARD):
                pygame.draw.rect(screen, WHITE, (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size), 1)

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
                                      self.top + CELL_SIZE * HEIGHT_BOARD + CELL_SIZE // 4))

    def render_cell_stat(self, screen):
        for y in range(HEIGHT_BOARD):
            for x in range(WIDTH_BOARD):
                if self.board[y][x] == BoardStat.MISS_SHOT:
                    pygame.draw.circle(screen, WHITE, (
                        x * self.cell_size + self.left + self.cell_size // 2,
                        y * self.cell_size + self.top + self.cell_size // 2),
                                       4)
                if self.board[y][x] == BoardStat.HARM or self.board[y][x] == BoardStat.DESTROYED_SHIP:
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

    def check_strike(self, x, y, coord=True):
        x_cells = (x - self.left) // CELL_SIZE if coord else y
        y_cells = (y - self.top) // CELL_SIZE if coord else x
        if self.board[y_cells][x_cells] == BoardStat.NOTHING or \
                self.board[y_cells][x_cells] == BoardStat.SHIP_AREA:
            self.board[y_cells][x_cells] = BoardStat.MISS_SHOT
            return BoardStat.MISS_SHOT
        elif self.board[y_cells][x_cells].__class__ == Ship:
            ship = self.board[y_cells][x_cells]
            self.board[y_cells][x_cells] = BoardStat.HARM
            if ship.damage():
                for x1 in range(ship.x - 1, ship.x + ship.height + 1):
                    for y1 in range(ship.y - 1, ship.y + ship.width + 1):
                        if x1 < 0 or y1 < 0 or x1 > WIDTH_BOARD - 1 or y1 > HEIGHT_BOARD - 1:
                            continue
                        elif self.board[x1][y1] == BoardStat.HARM:
                            self.board[x1][y1] = BoardStat.DESTROYED_SHIP
                            continue
                        self.board[x1][y1] = BoardStat.MISS_SHOT
                self.ships.remove(ship)
                return ship
            else:
                return BoardStat.HARM

    def check_click_corr(self, x, y):
        if self.left <= x <= self.left + CELL_SIZE * WIDTH_BOARD \
                and self.top <= y <= self.top + CELL_SIZE * HEIGHT_BOARD:
            return True
        else:
            return False

    def get_ships_count(self):
        return len(self.ships)

    def get_field_width(self):
        return self.cell_size * HEIGHT_BOARD + self.left

    def get_field_height(self):
        return self.cell_size * HEIGHT_BOARD + self.top + 50

    def set_ship(self, x, y, len_ship, orient, coord=True):
        x_cells = (x - self.left) // CELL_SIZE if coord else x
        y_cells = (y - self.top) // CELL_SIZE if coord else y
        ship = Ship(x_cells, y_cells, len_ship, orient)
        self.ships.append(ship)
        for x1 in range(ship.x, ship.x + ship.height):
            for y1 in range(ship.y, ship.y + ship.width):
                self.board[x1][y1] = ship
        self.update_ship_area()
        return self.left + x_cells * CELL_SIZE, self.top + y_cells * CELL_SIZE

    def del_ship(self, x, y, coord=True):
        x_cells = (x - self.left) // CELL_SIZE if coord else x
        y_cells = (y - self.top) // CELL_SIZE if coord else y
        try:
            ship = self.board[y_cells][x_cells]
            for x1 in range(ship.x - 1, ship.x + ship.height + 1):
                for y1 in range(ship.y - 1, ship.y + ship.width + 1):
                    if x1 < 0 or x1 >= WIDTH_BOARD or y1 < 0 or y1 >= HEIGHT_BOARD:
                        continue
                    self.board[x1][y1] = BoardStat.NOTHING
            self.ships.remove(ship)
            self.update_ship_area()
        except Exception:
            pass

    def check_collision_ship(self, x, y, len_ship, orient, coord=True):
        x_cells = (x - self.left) // CELL_SIZE if coord else x
        y_cells = (y - self.top) // CELL_SIZE if coord else y
        ship = Ship(x_cells, y_cells, len_ship, orient)
        if ship.x + ship.height - 1 >= HEIGHT_BOARD or ship.x < 0 or \
                ship.y + ship.width - 1 >= HEIGHT_BOARD or ship.y < 0:
            return False

        for x1 in range(ship.x, ship.x + ship.height):
            for y1 in range(ship.y, ship.y + ship.width):
                if self.board[x1][y1] != BoardStat.NOTHING:
                    return False
        return True

    def update_ship_area(self):
        for ship in self.ships:
            for x1 in range(ship.x - 1, ship.x + ship.height + 1):
                for y1 in range(ship.y - 1, ship.y + ship.width + 1):
                    if x1 < 0 or y1 < 0 or x1 > WIDTH_BOARD - 1 or y1 > HEIGHT_BOARD - 1:
                        continue
                    elif self.board[x1][y1].__class__ == Ship:
                        continue
                    self.board[x1][y1] = BoardStat.SHIP_AREA

    def debug_board(self):
        for i in self.board:
            for i2 in i:
                print(i2.value, end=' ')
            print()
        print()
