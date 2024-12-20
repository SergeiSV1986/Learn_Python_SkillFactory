# Приветствие
def welcome():
    print("Добро пожаловать в игру крестики-нолики!")
    print("Игровое поле имеет следующий вид:")
    print("--------------")
    print("| 1 | 2 | 3 |")
    print("--------------")
    print("| 4 | 5 | 6 |")
    print("--------------")
    print("| 7 | 8 | 9 |")
    print("--------------")
    print("Вы играете крестиками (X), противник играет ноликами (O).")
    print("Введите номер клетки, куда хотите поставить крестик.")
# Создаем игровок поле
board = list(range(1, 10))
wins_coord = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)]

# Вывод текущего состояни доски
def draw_board():
    print("--------------")
    for i in range(3):
        print("|", board[0 + i * 3],"|", board[1 + i * 3],"|", board[2 + i * 3], "|")
        print("--------------")

# Получает значение от пользователя и ставит на доску
def take_input(player_token):
    while True:
        value = input("Куда поставить: "+ player_token + " ")
        if value not in "123456789":
            print("Ошибочный ввод повторите.")
            continue
        value = int(value)
        if str(board[value - 1]) in "XO":
            print("Эта клетка уже занята")
            continue
        board[value - 1] = player_token
        break
# Проверка на победителя
def check_win():
    for each in wins_coord:
        if board[each[0]-1] == board[each[1]-1] == board[each[2]-1]:
            return board[each[0]-1]
    return False

# Чередование ходов
def game():
    counter = 0
    welcome() # Вызываем функцию приветствия перед началом игры
    while True:
        draw_board()
        if counter % 2 == 0:
            take_input("X")
        else:
            take_input("O")
        if counter > 3:
            winner = check_win()
            if winner:
                draw_board()
                print(winner, "Выиграл!")
                break
        counter += 1
        if counter == 9:
            draw_board()
            print("Ничья!")

game()
