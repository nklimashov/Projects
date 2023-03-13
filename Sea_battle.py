from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass


class OutBoardException(BoardException):
    def __str__(self):
        return "Стрельба за границы доски запрещена!"


class UsedBoardException(BoardException):
    def __str__(self):
        return "Вы уже обстреливали эту точку!"


class WrongShipBoardException(BoardException):
    pass


class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shoot(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["0"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):
        for d in ship.dots:
            if self.outBoard(d) or d in self.busy:
                raise WrongShipBoardException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near_dots = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near_dots:
                tab = Dot(d.x + dx, d.y + dy)
                if not(self.outBoard(tab)) and tab not in self.busy:
                    if verb:
                        self.field[tab.x][tab.y] = "."
                    self.busy.append(tab)

    def __str__(self):
        tab = ""
        tab += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            tab += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            tab = tab.replace("■", "0")
        return tab

    def outBoard(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.outBoard(d):
            raise OutBoardException()

        if d in self.busy:
            raise UsedBoardException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль подбит!")
                    return True

        self.field[d.x][d.y] = "."
        print("Промах!")
        return False

    def start(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Введите координаты: ").split()

            if len(cords) != 2:
                print("Введите ДВЕ координаты в формате x y")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа!")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size = 6):
        self.size = size
        player = self.random_board()
        comp = self.random_board()
        comp.hid = True

        self.ai = AI(comp, player)
        self.user = User(player, comp)

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except WrongShipBoardException:
                    pass
        board.start()
        return board

    def greet(self):
        print("------------------------")
        print("|   Добро пожаловать   |")
        print("|        в игру        |")
        print('|     "Морской бой"    |')
        print("|----------------------|")
        print("|      Вам нужно       |")
        print("|  вводить координаты  |")
        print("|    в формате: x y    |")
        print('|где "x" - номер строки|')
        print('| а "y" - номер столбца|')
        print("------------------------")

    def cycle(self):
        num = 0
        while True:
            print("-" * 20)
            print("Ваша доска:")
            print(self.user.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-" * 20)
            if num % 2 == 0:
                print("Ваш ход!")
                repeat = self.user.move()
            else:
                print("Ход компьютера!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.defeat():
                print("-" * 20)
                print("Вы выиграли! Поздравляю!")
                break

            if self.user.board.defeat():
                print("-" * 20)
                print("Увы, Вы проиграли!")
                break
            num += 1

    def start(self):
        self.greet()
        self.cycle()


g = Game()
g.start()