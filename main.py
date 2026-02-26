import turtle  # Підключення графіки
import time  # Робота з часом

# НАЛАШТУВАННЯ ВІКНА
window = turtle.Screen()  # Створення ігрового вікна
window.title("Танки 2026")  # Заголовок зверху вікна
window.bgcolor("black")  # Чорний фон екрана
window.setup(width=800, height=600)  # Розмір вікна гри
window.tracer(0)  # Вимкнення авто-оновлення екрана

score1 = 0  # Очки синього танка
score2 = 0  # Очки червоного танка

# ТАБЛИЦЯ РАХУНКУ
scoreboard = turtle.Turtle()  # Об'єкт для тексту
scoreboard.speed(0)  # Миттєва поява тексту
scoreboard.color("white")  # Білий колір букв
scoreboard.penup()  # Не малювати ліній
scoreboard.hideturtle()  # Сховати стрілку черепашки
scoreboard.goto(0, 260)  # Позиція тексту зверху


def update_score():  # Функція оновлення рахунку
    scoreboard.clear()  # Стерти старий текст
    scoreboard.write(f"Синій: {score1}  |  Червоний: {score2}", align="center",
                     font=("Arial", 24, "bold"))  # Написати новий рахунок


update_score()  # Початковий показ рахунку

# ПЕРЕШКОДИ (СТІНИ)
walls = []  # Список усіх стін


def create_wall(x, y):  # Функція створення цеглини
    wall = turtle.Turtle()  # Новий об'єкт стіни
    wall.shape("square")  # Форма квадрата
    wall.color("#b35900")  # Цегляний колір блока
    wall.shapesize(stretch_wid=1.5, stretch_len=1.5)  # Збільшення розміру стіни
    wall.penup()  # Не залишати слідів
    wall.goto(x, y)  # Поставити в координати
    walls.append(wall)  # Додати в список


def build_maze():  # Функція побудови лабіринту
    for x in [-300, -200, 200, 300]:  # Координати бічних колон
        for y in range(100, 301, 35): create_wall(x, y)  # Верхні вертикальні смуги
        for y in range(-300, -99, 35): create_wall(x, y)  # Нижні вертикальні смуги
    for y in range(150, 301, 35): create_wall(0, y)  # Центральна верхня стіна
    for y in range(-200, -50, 35):  # Нижня центральна частина
        create_wall(-50, y)  # Ліва внутрішня стіна
        create_wall(50, y)  # Права внутрішня стіна
    for x in range(-50, 51, 35): create_wall(x, -50)  # Нижня перегородка
    for x in [-350, -250, -150, 150, 250, 350]:  # Горизонтальні маленькі блоки
        create_wall(x, 20)  # Розміщення бокових вставок


build_maze()  # Запуск побудови карти

# ГРАВЦІ ТА ЗБРОЯ
tank1 = turtle.Turtle()  # Об'єкт синього танка
tank1.shape("turtle")  # Вигляд черепашки (танка)
tank1.color("blue")  # Синій колір гравця
tank1.penup()  # Не малювати маршрут

tank2 = turtle.Turtle()  # Об'єкт червоного танка
tank2.shape("turtle")  # Вигляд черепашки (танка)
tank2.color("red")  # Червоний колір гравця
tank2.penup()  # Не малювати маршрут

bullet1 = turtle.Turtle()  # Куля синього танка
bullet1.shape("circle")  # Форма кола (снаряд)
bullet1.color("yellow")  # Жовтий колір пострілу
bullet1.shapesize(0.4)  # Зменшення розміру кулі
bullet1.penup()  # Не малювати лінію
bullet1.hideturtle()  # Сховати кулю спочатку
bullet1_state = "ready"  # Готовність до стрільби

bullet2 = turtle.Turtle()  # Куля червоного танка
bullet2.shape("circle")  # Форма снаряда (коло)
bullet2.color("orange")  # Помаранчевий колір пострілу
bullet2.shapesize(0.4)  # Малий розмір снаряда
bullet2.penup()  # Не малювати лінію
bullet2.hideturtle()  # Приховати до пострілу
bullet2_state = "ready"  # Можна знову стріляти


def reset_positions():  # Скидання танків на старт
    tank1.goto(-350, 250)  # Синій у верхній кут
    tank1.setheading(0)  # Дивиться праворуч
    tank2.goto(350, -250)  # Червоний у нижній кут
    tank2.setheading(180)  # Дивиться ліворуч


reset_positions()  # Поставити танки спочатку


# РУХ
def is_collision_wall(t):  # Перевірка влучання в стіну
    for wall in walls:  # Перебрати всі стіни
        if t.distance(wall) < 28: return True  # Зіткнення, якщо близько
    return False  # Зіткнення немає


def t1_up():  # Рух синього вперед
    tank1.forward(10)  # Проїхати вперед
    if is_collision_wall(tank1): tank1.backward(10)  # Відкотитися, якщо стіна


def t1_down():  # Рух синього назад
    tank1.backward(10)  # Проїхати назад
    if is_collision_wall(tank1): tank1.forward(10)  # Зупинитись об стіну


def t1_left(): tank1.left(15)  # Поворот ліворуч


def t1_right(): tank1.right(15)  # Поворот праворуч


def t2_up():  # Рух червоного вперед
    tank2.forward(10)  # Проїхати вперед
    if is_collision_wall(tank2): tank2.backward(10)  # Відкотитися від стіни


def t2_down():  # Рух червоного назад
    tank2.backward(10)  # Проїхати назад
    if is_collision_wall(tank2): tank2.forward(10)  # Зупинитись об стіну


def t2_left(): tank2.left(15)  # Поворот ліворуч


def t2_right(): tank2.right(15)  # Поворот праворуч


def fire_bullet1():  # Постріл синього
    global bullet1_state  # Зміна статусу кулі
    if bullet1_state == "ready":  # Якщо можна стріляти
        bullet1_state = "fire"  # Зміна на "летить"
        bullet1.goto(tank1.xcor(), tank1.ycor())  # Поява в танку
        bullet1.setheading(tank1.heading())  # Напрямок як у танка
        bullet1.showturtle()  # Показати снаряд


def fire_bullet2():  # Постріл червоного
    global bullet2_state  # Зміна статусу кулі
    if bullet2_state == "ready":  # Якщо готова до пуску
        bullet2_state = "fire"  # Зміна стану польоту
        bullet2.goto(tank2.xcor(), tank2.ycor())  # Переліт до танка
        bullet2.setheading(tank2.heading())  # Напрямок за танком
        bullet2.showturtle()  # Показати снаряд на екрані


def move_bullets():  # Рух випущених куль
    global bullet1_state, bullet2_state  # Глобальні стани куль
    if bullet1_state == "fire":  # Якщо синя летить
        bullet1.forward(15)  # Швидкість польоту кулі
        for wall in walls:  # Перевірка на стіни
            if bullet1.distance(wall) < 20:  # Влучання в стіну
                bullet1.hideturtle()
                bullet1_state = "ready"  # Сховати та скинути
        if abs(bullet1.xcor()) > 400 or abs(bullet1.ycor()) > 300:  # Виліт за екран
            bullet1.hideturtle()
            bullet1_state = "ready"  # Сховати та скинути

    if bullet2_state == "fire":  # Якщо червона летить
        bullet2.forward(15)  # Рух снаряда вперед
        for wall in walls:  # Перевірка кожної стіни
            if bullet2.distance(wall) < 20:  # Попадання в цеглу
                bullet2.hideturtle()
                bullet2_state = "ready"  # Приховати та скинути
        if abs(bullet2.xcor()) > 400 or abs(bullet2.ycor()) > 300:  # Межа вікна
            bullet2.hideturtle()
            bullet2_state = "ready"  # Приховати та скинути


# КЕРУВАННЯ
window.listen()  # Слухати натискання клавіш
window.onkey(t1_up, "w")
window.onkey(t1_down, "s")  # Синій: W/S
window.onkey(t1_left, "a")
window.onkey(t1_right, "d")  # Синій: A/D
window.onkey(fire_bullet1, "space")  # Синій: Пробіл - вогонь

window.onkey(t2_up, "Up")
window.onkey(t2_down, "Down")  # Червоний: Стрілки
window.onkey(t2_left, "Left")
window.onkey(t2_right, "Right")  # Червоний: Стрілки
window.onkey(fire_bullet2, "Return")  # Червоний: Enter - вогонь

# ГОЛОВНИЙ ЦИКЛ
game_on = True  # Стан роботи гри
while game_on:  # Поки гра активна
    window.update()  # Малювання кадру
    move_bullets()  # Оновлення руху куль
    time.sleep(0.01)  # Коротка затримка процесу

    if bullet1.distance(tank2) < 20 and bullet1_state == "fire":  # Синій влучив
        score1 += 1  # Плюс бал синьому
        bullet1.hideturtle()  # Сховати кулю
        bullet1.goto(1000, 1000)  # Викид за карту
        bullet1_state = "ready"  # Куля знову готова
        update_score()  # Показ нового рахунку
        if score1 < 3:  # Якщо ще не фінал
            window.update()  # Показати оновлення
            time.sleep(1)  # Пауза після вбивства
            reset_positions()  # Новий раунд

    if bullet2.distance(tank1) < 20 and bullet2_state == "fire":  # Червоний влучив
        score2 += 1  # Плюс бал червоному
        bullet2.hideturtle()  # Сховати кулю
        bullet2.goto(1000, 1000)  # Викид снаряда
        bullet2_state = "ready"  # Перезарядка завершена
        update_score()  # Оновлення таблиці балів
        if score2 < 3:  # Якщо гра триває
            window.update()  # Візуальне оновлення
            time.sleep(1)  # Секунда тиші
            reset_positions()  # Повернення на старт

    if score1 == 3 or score2 == 3:  # Перевірка ліміту 3
        for wall in walls: wall.hideturtle()  # Прибрати всі стіни
        tank1.hideturtle()  # Сховати синій танк
        tank2.hideturtle()  # Сховати червоний танк
        bullet1.hideturtle()  # Прибрати синю кулю
        bullet2.hideturtle()  # Прибрати червону кулю
        scoreboard.clear()  # Очистити дрібний рахунок

        if score1 == 3:  # Виграв синій
            window.bgcolor("blue")  # Фон стає синім
            result_text = "СИНІЙ ВИГРАВ!"  # Текст перемоги
        else:  # Виграв червоний
            window.bgcolor("red")  # Фон стає червоним
            result_text = "ЧЕРВОНИЙ ВИГРАВ!"  # Текст перемоги

        scoreboard.goto(0, 0)  # Текст у центр
        scoreboard.color("white")  # Білий колір напису
        scoreboard.write(result_text, align="center", font=("Arial", 50, "bold"))  # Показ ПЕРЕМОГИ
        window.update()  # Фінальне оновлення екрана
        game_on = False  # Вимкнення циклу гри

window.mainloop()  # Тримати вікно відкритим