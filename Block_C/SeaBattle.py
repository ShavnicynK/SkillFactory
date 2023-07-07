from random import randint


# Классы исключений
class SeaBattleException(Exception):
    pass


# Исключение при выстреле мимо доски
class BoardOutException(SeaBattleException):
    def __str__(self):
        return "Ваш выстрел улетел мимо доски, прицельтесь получше!"


# Исключение при выстреле в уже использовавшуюся клетку
class BoardOccupiedCellException(SeaBattleException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку. Соберитесь!"


# Исключение при расстановке кораблей
class ShipAddException(SeaBattleException):
    def __str__(self):
        return "Ошибка расстановки"


# Исключение при выборе режима игры
class ModeSelectException(SeaBattleException):
    pass


# Исключение для итератора досок
class BoardIteratorException(SeaBattleException):
    pass


# Класс точка
class Dot:
    def __init__(self, coord_x, coord_y):
        self.coord_x = coord_x
        self.coord_y = coord_y

    def __eq__(self, dot):
        return self.coord_x == dot.coord_x and self.coord_y == dot.coord_y


# Класс корабль
class Ship:
    def __init__(self, width, dot_start, direction):
        self.width = width  # Длина корабля
        self.dot_start = dot_start  # Координты начала корабля
        self.direction = direction  # Направление корабля: 0 - вертикальное, 1 - горизонтальное
        self.health = width

    # Получение точек корабля
    @property
    def dots(self):
        ship_dots = []
        for w in range(self.width):
            coord_x = self.dot_start.coord_x
            coord_y = self.dot_start.coord_y

            if self.direction == 0:
                coord_x += w
            elif self.direction == 1:
                coord_y += w

            ship_dots.append(Dot(coord_x, coord_y))

        return ship_dots


# Итератор свойств объектов класса доска
class BoardIterator:
    def __init__(self, objects):
        self.objects = objects
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < len(self.objects):
            res = self.objects[self.current]
            self.current += 1
            return res
        raise StopIteration


# Класс доска
class Board:
    def __init__(self, size=6, live_ships=7, hid=False):
        self.size = size  # Размер доски
        self.hid = hid  # Скрыть/показать корабли
        self.live_ships = live_ships  # Количество живых кораблей

        self.board = [["O"] * size for _ in range(size)]

        self.busy_list = []  # Список занятых точек
        self.ships_list = []  # Список кораблей

    # Метод проверки на выстрел мимо доски
    def dot_out(self, dot):
        return not ((0 <= dot.coord_x < self.size) and (0 <= dot.coord_y < self.size))

    # Метод добавления корабля на доску
    def add_ship(self, ship):
        for d in ship.dots:
            if self.dot_out(d) or d in self.busy_list:
                raise ShipAddException()
        for d in ship.dots:
            self.board[d.coord_x][d.coord_y] = "■"
            self.busy_list.append(d)

        self.ships_list.append(ship)
        self.contour(ship)

    # Метод расстановки контура вокруг корабля
    def contour(self, ship, ship_death=False):
        outline = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for d in ship.dots:
            for o_x, o_y in outline:
                cur_coord = Dot(d.coord_x + o_x, d.coord_y + o_y)
                if not self.dot_out(cur_coord) and cur_coord not in self.busy_list:
                    if ship_death:
                        self.board[cur_coord.coord_x][cur_coord.coord_y] = self.set_color("●", "yellow")
                    self.busy_list.append(cur_coord)

    # Метод осуществляющий выстрел
    def shot(self, dot):
        if self.dot_out(dot):
            raise BoardOutException()

        if dot in self.busy_list:
            raise BoardOccupiedCellException()

        self.busy_list.append(dot)

        for ship in self.ships_list:
            if dot in ship.dots:
                ship.health -= 1
                self.board[dot.coord_x][dot.coord_y] = self.set_color("X", "red")
                if ship.health == 0:
                    self.live_ships -= 1
                    self.contour(ship, ship_death=True)
                    print("Корабль потоплен!")
                    return False
                else:
                    print("Корабль подбит, добьем его!")
                    return True

        self.board[dot.coord_x][dot.coord_y] = self.set_color("●", "yellow")
        print("Промазал!")
        return False

    # Метод обнуления списка занятых при старте игры (после расстановки кораблей)
    def start(self):
        self.busy_list = []

    # Метод окраски некоторых симовлов доски
    @classmethod
    def set_color(cls, text, color):
        if color == "green":
            return "\033[32m{}\033[37m".format(text)
        elif color == "red":
            return "\033[31m{}\033[37m".format(text)
        elif color == "yellow":
            return "\033[33m{}\033[37m".format(text)
        elif color == "blue":
            return "\033[34m{}\033[37m".format(text)

    # Метод печати досок
    def print_board(self, player_board, ai_board):
        width_print_board = player_board.size * 6
        pl_board_iter = self.__iter__(player_board.board)
        ai_board_iter = self.__iter__(ai_board.board)
        body = ""
        body += f"{'Доска пользователя:': <{width_print_board}}"
        body += f"{'Доска компьютера:': <{width_print_board}}\n"
        body += f"{'-' * 20: <{width_print_board}}"
        body += f"{'-' * 20: <{width_print_board}}\n"
        body_temp = self.set_color("  |", "green")
        for i in range(1, player_board.size + 1):
            body_temp += self.set_color(f" {i} |", "green")
        body += body_temp + " " * 9 + body_temp + "\n"
        body_temp = ""
        for i in range(1, player_board.size + 1):
            body_temp += f"{self.set_color(i, 'green')} | " + " | ".join(next(pl_board_iter)).replace("■",
                                                                                                      self.set_color(
                                                                                                          "■",
                                                                                                          "blue")) + " |" + " " * 9
            body_temp += f"{self.set_color(i, 'green')} | " + " | ".join(next(ai_board_iter)).replace("■", "O") + " |\n"
        body += body_temp

        return body

    def __iter__(self, objects):
        return BoardIterator(objects)


# Класс игрок
class Player:
    def __init__(self, own_board, enemy_board, size_board):
        self.own_board = own_board  # Своя доска
        self.enemy_board = enemy_board  # Доска соперника
        self.size_board = size_board  # Размер доски

    # Метод запроса координат выстрела (определен в дочерних классах)
    def ask(self):
        raise NotImplementedError()

    # Метод осуществления хода игрока
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except SeaBattleException as e:
                print(e)


# Класс игрока Компютер
class AI(Player):
    def ask(self):
        dot = Dot(randint(0, self.size_board), randint(0, self.size_board))
        print(f"Компьютер ударил в точку: {dot.coord_x + 1} {dot.coord_y + 1}")
        return dot


# Класс игрока Пользователь
class User(Player):
    def ask(self):
        while True:
            coord_list = input("Ваш ход: ").split()
            if len(coord_list) != 2:
                print("Нужно ввести две координаты через пробел")
                continue

            coord_x, coord_y = coord_list

            if not (coord_x.isdigit()) or not (coord_y.isdigit()):
                print("Нужно ввести числа")
                continue

            coord_x, coord_y = int(coord_x), int(coord_y)

            return Dot(coord_x - 1, coord_y - 1)


# Класс игры
class Game:
    # Параметры игры
    type_mode = 0  # Режим игры по умолчанию
    size_board = [6, 8, 10]  # Размеры досок
    ships_mode = [[3, 2, 2, 1, 1, 1, 1], [4, 3, 2, 2, 1, 1, 1, 1], [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]]  # Кол-во кораблей

    def __init__(self):
        self.greet()
        self.mode = self.ships_mode[self.type_mode]
        self.size = self.size_board[self.type_mode]

        player_board = self.random_board()
        ai_board = self.random_board()
        ai_board.hid = True

        self.ai = AI(ai_board, player_board, self.size)
        self.player = User(player_board, ai_board, self.size)

    # Метод гарантированной генерации доски
    def random_board(self):
        board = None
        while board is None:
            board = self.generate_board()
        return board

    # Метод генерации доски с ограничением на количество попыток генерации
    def generate_board(self):
        lens = self.mode
        board = Board(size=self.size, live_ships=len(self.mode))

        iterations = 0
        for l in lens:
            while True:
                iterations += 1
                if iterations > 1000:
                    return None
                ship = Ship(l, Dot(randint(0, self.size), randint(0, self.size)), randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except ShipAddException:
                    pass

        board.start()
        return board

    # Метод приветствия с возможностью выбора режима игры
    def greet(self):
        print("------------------------------------------------------------------")
        print("  Приветсвуем вас в игре \"Морской бой\"")
        print("  В данной игре предусмотрено три уровня сложности:")
        print("  1. Поле 6 х 6 клеток и 7 кораблей")
        print("  2. Поле 8 х 8 клеток и 8 кораблей")
        print("  1. Поле 10 х 10 клеток и 10 кораблей")
        print("------------------------------------------------------------------")
        print("  Выстрелы осуществляются вводом координат клетки в формате: x y ")
        print("  x - номер строки  ")
        print("  y - номер столбца ")
        print("------------------------------------------------------------------")
        print("  Для начала игры выберите уровень сложности:")
        while True:
            num = input("  Введите число 1, 2 или 3: ")
            try:
                if num not in ('1', '2', '3'):
                    raise ModeSelectException()
            except ModeSelectException:
                print("  Введите одно из указанных чисел")
            else:
                self.type_mode = int(num) - 1
                return

    # Метод с главным игровым циклом
    def loop(self):
        step = 0
        while True:
            print(Board().print_board(self.player.own_board, self.ai.own_board))
            if step % 2 == 0:
                print("-" * 20)
                repeat = self.player.move()
            else:
                print("-" * 20)
                repeat = self.ai.move()

            if not repeat:
                step += 1

            if self.ai.own_board.live_ships == 0:
                print(Board().print_board(self.player.own_board, self.ai.own_board))
                print("-" * 20)
                print("Вы выиграли!")
                break

            if self.player.own_board.live_ships == 0:
                print(Board().print_board(self.player.own_board, self.ai.own_board))
                print("-" * 20)
                print("Компьютер выиграл!")
                break

    def start(self):
        self.loop()


battle = Game()
battle.start()
