import random
from const import *
from ship import Ship

ships = [[4, 1], [3, 2], [2, 3], [1, 4]]


class Bot:
    def __init__(self, check_ship, set_ship):
        self.f_check_ship = check_ship
        self.f_set_ship = set_ship
        self.available_blocks = {(x, y) for x in range(10) for y in range(10)}
        self.map = [[0 for _ in range(10)] for _ in range(10)]
        self.radar = [[0 for _ in range(10)] for _ in range(10)]
        self.weight = [[1 for _ in range(10)] for _ in range(10)]

    def __create_start_block(self, available_blocks):
        orientation = random.randint(0, 1)
        # -1 is left or down, 1 is right or up
        # self.direction = random.choice((-1, 1))
        ship_len = ships[0][0]
        x, y = random.choice(tuple(available_blocks))
        return x, y, ship_len, orientation

    def auto_set_ships(self):
        while len(ships):
            ship = self.__create_start_block(self.available_blocks)
            if self.f_check_ship(ship[0], ship[1], ship[2], ship[3], coord=False):
                self.f_set_ship(ship[0], ship[1], ship[2], ship[3], coord=False)
                ships[0][1] -= 1
                if ships[0][1] <= 0:
                    ships.pop(0)

    def get_max_weight_cells(self):
        weights = {}
        max_weight = 0
        # просто пробегаем по всем клеткам и заносим их в словарь с ключом который является значением в клетке
        # заодно запоминаем максимальное значение. далее просто берём из словаря список координат с этим
        # максимальным значением weights[max_weight]
        for x in range(self.size):
            for y in range(self.size):
                if self.weight[x][y] > max_weight:
                    max_weight = self.weight[x][y]
                weights.setdefault(self.weight[x][y], []).append((x, y))

        return weights[max_weight]

    # пересчет веса клеток
    def recalculate_weight_map(self, available_ships):
        # Для начала мы выставляем всем клеткам 1.
        # нам не обязательно знать какой вес был у клетки в предыдущий раз:
        # эффект веса не накапливается от хода к ходу.
        self.weight = [[1 for _ in range(self.size)] for _ in range(self.size)]

        # Пробегаем по всем полю.
        # Если находим раненый корабль - ставим клеткам выше ниже и по бокам
        # коэффициенты умноженые на 50 т.к. логично что корабль имеет продолжение в одну из сторон.
        # По диагоналям от раненой клетки ничего не может быть - туда вписываем нули
        for x in range(self.size):
            for y in range(self.size):
                if self.radar[x][y] == Cell.damaged_ship:

                    self.weight[x][y] = 0

                    if x - 1 >= 0:
                        if y - 1 >= 0:
                            self.weight[x - 1][y - 1] = 0
                        self.weight[x - 1][y] *= 50
                        if y + 1 < self.size:
                            self.weight[x - 1][y + 1] = 0

                    if y - 1 >= 0:
                        self.weight[x][y - 1] *= 50
                    if y + 1 < self.size:
                        self.weight[x][y + 1] *= 50

                    if x + 1 < self.size:
                        if y - 1 >= 0:
                            self.weight[x + 1][y - 1] = 0
                        self.weight[x + 1][y] *= 50
                        if y + 1 < self.size:
                            self.weight[x + 1][y + 1] = 0

        # Перебираем все корабли оставшиеся у противника.
        # Это открытая инафа исходя из правил игры.  Проходим по каждой клетке поля.
        # Если там уничтоженый корабль, задамаженый или клетка с промахом -
        # ставим туда коэффициент 0. Больше делать нечего - переходим следующей клетке.
        # Иначе прикидываем может ли этот корабль с этой клетки начинаться в какую-либо сторону
        # и если он помещается прбавляем клетке коэф 1.

        for ship_size in available_ships:

            ship = Ship(ship_size, 1, 1, 0)
            # вот тут бегаем по всем клеткам поля
            for x in range(self.size):
                for y in range(self.size):
                    if self.radar[x][y] in (Cell.destroyed_ship, Cell.damaged_ship, Cell.miss_cell) \
                            or self.weight[x][y] == 0:
                        self.weight[x][y] = 0
                        continue
                    # вот здесь ворочаем корабль и проверяем помещается ли он
                    for rotation in range(0, 4):
                        ship.set_position(x, y, rotation)
                        if self.check_ship_fits(ship, FieldPart.radar):
                            self.weight[x][y] += 1
