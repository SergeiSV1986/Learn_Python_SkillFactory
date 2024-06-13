
class BoardException(Exception):
    pass

# Исключение, возникающее при выстреле за пределы игрового поля
class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за пределы поля!"

# Исключение, возникающее при попытке повторного выстрела в уже использованную клетку
class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"

# Исключение, возникающее при неправильном размещении корабля на доске
class BoardWrongShipException(BoardException):
    def __str__(self):
        return "Нельзя поставить корабль таким образом!"

# Класс для представления точки на игровом поле
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Переопределение метода сравнения для точек
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

# Класс для представления корабля на игровом поле
class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow  # Начальная точка корабля (нос)
        self.l = l      # Длина корабля
        self.o = o      # Ориентация корабля (0 - горизонтальная, 1 - вертикальная)
        self.lives = l  # Количество жизней корабля

    # Метод для получения всех точек, занимаемых кораблем
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

# Класс для представления игровой доски
class Board:
    def __init__(self, hid=False, size=6):
        self.size = size    # Размер игрового поля
        self.hid = hid      # Флаг скрытия кораблей на доске

        self.field = [["O"] * size for _ in range(size)]  # Игровое поле

        self.busy = []      # Занятые точки на доске
        self.ships = []     # Корабли на доске

    # Метод для добавления корабля на доску
    def add_ship(self, ship):
        # Проверка на возможность размещения корабля
        for dot in ship.dots:
            if self.out(dot) or dot in self.busy:
                raise BoardWrongShipException()

        # Размещение корабля на доске
        for dot in ship.dots:
            self.field[dot.x][dot.y] = "■"
            self.busy.append(dot)

        self.ships.append(ship)
        self.contour(ship)

    # Метод для обводки корабля на доске
    def contour(self, ship, verb=False):
        # Список смежных клеток
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    # Представление доски в виде строки
    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |" + "\n"
        for i, row in enumerate(self.field):
            res += f"{i + 1} | {' | '.join(row)} |" + "\n"
        return res

    # Метод для проверки выхода точки за пределы поля
    def out(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    # Метод для обработки выстрела по доске
    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException()

        if dot in self.busy:
            raise BoardUsedException()

        self.busy.append(dot)

        for ship in self.ships:
            if dot in ship.dots:
                ship.lives -= 1
                self.field[dot.x][dot.y] = "X"
                if ship.lives == 0:
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль подбит!")
                    return True

        self.field[dot.x][dot.y] = "T"
        print("Промах!")
        return False

# Класс для представления игрока
class Player:
    def __init__(self, board, enemy_board):
        self.board = board          # Доска игрока
        self.enemy_board = enemy_board  # Доска противника

    # Метод для запроса координат выстрела
    def ask(self):
        print("Введите координаты для выстрела (например, '3,4'):")
        x, y = map(int, input().split(','))  # Ввод координат в формате 'x,y'
        return Dot(x - 1, y - 1)  # Возвращаем точку с учетом индексации с 0
    # Метод для выполнения хода
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except BoardException as e:
                print(e)

# Класс для представления игры
class Game:
    def __init__(self):
        self.board = Board()                      # Доска игрока
        self.enemy_board = Board(hid=True)       # Доска противника

        self.player = Player(self.board, self.enemy_board)   # Игрок
        self.ai = Player(self.enemy_board, self.board)       # Противник (ИИ)

    # Метод для приветствия игрока и объяснения правил игры
    def greet(self):
        print("-------------------")


        print("   Добро пожаловать в игру 'Морской бой'   ")
        print("-------------------")
        print("   Правила игры:   ")
        print("Ваша цель - потопить все корабли противника.")
        print("Удачи!")
        print("-------------------")

    # Метод для основного игрового цикла
    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.enemy_board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ход игрока!")
                repeat = self.player.move()
            else:
                print("-" * 20)
                print("Ход компьютера!")
                repeat = self.ai.move()

            if repeat:
                num -= 1

            if self.board.ships == 0:
                print("Корабли игрока уничтожены! Компьютер победил!")
                break
            elif self.enemy_board.ships == 0:
                print("Корабли компьютера уничтожены! Игрок победил!")
                break

            num += 1

    # Метод для запуска игры
    def start(self):
        self.greet()
        self.loop()

# Запуск игры
if __name__ == "__main__":
    g = Game()
    g.start()
