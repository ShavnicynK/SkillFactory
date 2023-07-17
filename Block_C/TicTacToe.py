class PointException(Exception):
    pass


#Вводим имена игроков
def input_player_name(text):
    while True:
        name = input(f"Введите имя {text} игрока: ")
        try:
            if not name or not name.isalpha():
                raise PointException()#print("Имя не указано, повторите ввод")
        except PointException:
            print("Имя не указано, повторите ввод")
        else:
            return name

#Вводим номера столбцов и строк
def input_cr(text, board_c=None):
    while True:
        num = input(f"Укажите номер {text}: ")
        if not num or not num.isdigit() or int(num) not in [1, 2, 3]:
            print(f"Неверно указан номер {text}, повторите ввод")
        elif not is_occupied(None if board_c is None else int(num) - 1, int(num) - 1 if board_c is None else board_c - 1):
            print(f"Уже занято, повторите ввод")
        else:
            return int(num)


#Проверяем на занятость выбранную ячейку
def is_occupied(board_r, board_c):
    if board_r is None:
        return board[0][board_c] == "-" or board[1][board_c] == "-" or board[2][board_c] == "-"
    else:
        return board[board_r][board_c] == "-"


#Выделение цветом
def set_color(text):
    text = "\033[32m{}\033[37m".format(text)
    return text


#Проверяем на наличие выигрышной комбинации учитывая последний символ
def is_win(board_c, board_r):
    opt_1 = board[board_r - 1]
    opt_2 = [board[0][board_c - 1], board[1][board_c - 1], board[2][board_c - 1]]
    opt_3 = [board[0][0], board[1][1], board[2][2]]
    opt_4 = [board[0][2], board[1][1], board[2][0]]
    #последний символ установлен в угловую ячейку (3 возможных выигрышных комбинации)
    if (board_r, board_c) in [(1, 1), (1, 3), (3, 1), (3, 3)]:
        return opt_1.count(marker[step % 2]) == 3 or opt_2.count(marker[step % 2]) == 3 \
            or opt_3.count(marker[step % 2]) == 3
    #последний символ установлен в среднюю ячейку крайних строк/столбцов (2 возможных выигрышных комбинации)
    elif (board_r, board_c) in [(2, 1), (2, 3), (1, 2), (3, 2)]:
        return opt_1.count(marker[step % 2]) == 3 or opt_2.count(marker[step % 2]) == 3
    #последний символ установлен в центр игрового поля (4 возможных выигрышных комбинации)
    elif (board_r, board_c) in [(2, 2)]:
        return opt_1.count(marker[step % 2]) == 3 or opt_2.count(marker[step % 2]) == 3 \
            or opt_3.count(marker[step % 2]) == 3 or opt_4.count(marker[step % 2]) == 3


#Работа с игровым полем
def board_print(board_c=0, board_r=0):
    board_pr: str = ""
    #Игровое поле с выделенными столбцами для их выбора
    if board_c == 0 and board_r == 0:
        board_pr += set_color("1  2  3\n")
        for board_r in board:
            for elem in board_r:
                board_pr += elem + "  "
            board_pr += "\n"
        return board_pr
    #Игровое поле с выделенным столбцом для выбора ячейки
    elif board_c > 0 and board_r == 0:
        for board_r in range(len(board)):
            board_pr += set_color(board_r + 1) + " "
            for elem in range(len(board[board_r])):
                board_pr += set_color(f"[{board[board_r][elem]}]") + "  " if elem == board_c - 1 \
                    else board[board_r][elem] + "  "
            board_pr += "\n"
        return board_pr
    #Добавление маркера на игровое поле
    elif board_c > 0 and board_r > 0:
        board[board_r - 1][board_c - 1] = marker[step % 2]
    #Формирование игрового поля без дополнительных элементов
    elif board_c == -1 and board_r == -1:
        for board_r in board:
            for elem in board_r:
                board_pr += elem + "  "
            board_pr += "\n"
        return board_pr


###Инициализация переменных
#Формируем список игроков
players = [input_player_name("первого"), input_player_name("второго")]
#Формируем привязку маркеров к игрокам
marker = ["X", "O"]
#Формируем игровое поле
board = [["-" for a in range(3)] for b in range(3)]
step = 0

while step <= 8:
    print("-" * 30, "\n")
    print(f"Ход игрока {set_color(players[step % 2])}", f"(ставим - {marker[step % 2]})\n")
    print(board_print())
    #Запрашиваем номер столбца
    board_col = input_cr("столбца")
    print("\n")
    print(board_print(board_col, 0))
    # Запрашиваем номер строки
    board_row = input_cr("строки", board_col)
    board_print(board_col, board_row)
    #После пятого хода начинаем проверть возможность победы
    if step >= 4 and is_win(board_col, board_row):
        print(f"{set_color(players[step % 2])} выиграл!")
        print(board_print(-1, -1))
        break
    if step == 8 and not is_win(board_col, board_row):
        print(set_color("\nНичья!"))
        print(board_print(-1, -1))
    step += 1