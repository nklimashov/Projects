# Игра крестики - нолики

def hello():
    print('_________________________')
    print('|                       |')
    print('|Добро пожаловать в игру|')
    print('|  "Крестики - нолики"  |')
    print('|-----------------------|')
    print('|   Первыми ходит "Х"   |')
    print('|    Для выбора поля    |')
    print('|впишите его координаты |')
    print('|     в формате x y     |')
    print('|_______________________|')

field = [[" "] * 3 for i in range(3)]

def show_field():
    print("    | 0 | 1 | 2 |")
    print(" ---|---|---|---|")
    for i, row in enumerate(field):
        column = f"  {i} | {' | '.join(row)} | "
        print(column)
        print(" ---|---|---|---|")
    print()

def ask_coordinates():
    while True:
        coordintes = input('Введите координаты: ').split()

        if len(coordintes) != 2:
            print('Введите две координаты')
            continue

        x, y = coordintes

        if not(x.isdigit()) or not(y.isdigit()):
            print('Координаты должны быть числовыми')
            continue

        x, y = int(x), int(y)

        if x < 0 or x > 2 or y < 0 or y > 2:
            print('Координаты должны быть от 0 до 2')
            continue

        if field[x][y] != ' ':
            print('Эта клетка занята')
            continue

        return x, y

def check_win():
    win_coordinates = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
    for coordinates in win_coordinates:
        sym = []
        for x in coordinates:
            sym.append(field[x[0]][x[1]])
        if sym == ["X", "X", "X"]:
            print("Выиграл X!!!")
            return True
        if sym == ["0", "0", "0"]:
            print("Выиграл 0!!!")
            return True
    return False

field = [
    [" ", "X", " "],
    [" ", "X", " "],
    [" ", "X", " "]
]


hello()
field = [[" "] * 3 for i in range(3)]
motion = 0
while True:
    motion += 1
    show_field()
    if motion % 2 == 1:
        print("Ходит крестик!")
    else:
        print("Ходит нолик!")

    x, y = ask_coordinates()

    if motion % 2 == 1:
        field[x][y] = "X"
    else:
        field[x][y] = "0"

    if check_win():
        break

    if motion == 9:
        print("Ничья!")
        break
