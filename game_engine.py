import turtle  # Графічне ядро гри
import time  # Затримки
import random  # Випадкові числа
import pygame  # Для звуків
from config import *  # Імпорт усіх налаштувань


def start_game(num_players):  # Головна функція гри
    pygame.display.quit()  # Закриваємо вікно меню Pygame
    window = turtle.Screen()  # Створюємо вікно Turtle
    window.clear()  # Очищення
    window.setup(900, 700)  # Розмір вікна гри
    window.tracer(0)  # Вимикаємо анімацію для швидкості

    if os.path.exists(BACKGROUND_IMAGE):
        window.bgpic(BACKGROUND_IMAGE)  # Фон
    else:
        window.bgcolor("black")

    walls = []  # Список об'єктів стін

    def create_wall(x, y):  # Функція створення одного блоку
        w = turtle.Turtle("square")  # Квадратна форма
        w.color("#00fbff", "#00008b")  # Неоновий коліr
        w.shapesize(1.3, 1.3);
        w.penup();
        w.goto(x, y)  # Розмір та позиція
        walls.append(w)

    def build_maze():  # Генерація випадкової мапи
        spawns = [P_CONFIGS[i][6] for i in range(num_players)]  # Координати танків
        for x in range(-360, 361, 60):  # Сітка по X
            for y in range(-280, 281, 60):  # Сітка по Y
                safe = True  # Перевірка безпечної зони навколо спавну
                for sx, sy in spawns:
                    if abs(x - sx) < 100 and abs(y - sy) < 100: safe = False
                if safe and random.random() < 0.25: create_wall(x, y)  # 25% шанс стіни

    players, bullets = [], []  # Списки танків та куль
    scores = [0] * num_players  # Рахунок гравців

    for i in range(num_players):  # Створення гравців
        conf = P_CONFIGS[i]  # Беремо конфіг
        t = turtle.Turtle("turtle");
        t.color(conf[0]);
        t.penup()  # Танк-черепашка
        t.goto(conf[6]);
        t.setheading(conf[7]);
        t.active = True;
        t.name = conf[0]
        b = turtle.Turtle("circle");
        b.hideturtle();
        b.penup();
        b.shapesize(0.3)  # Куля
        b.color("white");
        b.state = "ready"  # Готовність до пострілу
        players.append(t);
        bullets.append(b)

    def can_move(t, dist):  # Перевірка на зіткнення зі стінами та краєм
        t.forward(dist)
        if abs(t.xcor()) > 435 or abs(t.ycor()) > 335: t.backward(dist); return False
        for w in walls:
            if t.distance(w) < 28: t.backward(dist); return False
        t.backward(dist);
        return True

    def move_setup(idx):  # Прив'язка клавіш до кожного гравця
        c = P_CONFIGS[idx];
        t = players[idx];
        b = bullets[idx]
        window.onkey(lambda: t.forward(10) if can_move(t, 10) else None, c[1])  # Вперед
        window.onkey(lambda: t.backward(10) if can_move(t, -10) else None, c[2])  # Назад
        window.onkey(lambda: t.left(15), c[3]);
        window.onkey(lambda: t.right(15), c[4])  # Повороти

        def f():  # Функція пострілу
            if b.state == "ready" and t.active:
                if shoot_fx: shoot_fx.play()  # Звук
                b.state = "fire";
                b.goto(t.pos());
                b.setheading(t.heading());
                b.showturtle()

        window.onkey(f, c[5])  # Клавіша вогню

    # Кнопка МЕНЮ всередині Turtle
    btn = turtle.Turtle();
    btn.hideturtle();
    btn.speed(0);
    btn.color("white");
    btn.penup()
    btn.goto(-440, 310);
    btn.begin_fill()
    for _ in range(2): btn.forward(80); btn.left(90); btn.forward(30); btn.left(90)
    btn.end_fill();
    btn.color("black");
    btn.goto(-400, 315)
    btn.write("МЕНЮ", align="center", font=("Arial", 10, "bold"))

    game_running = True

    def exit_to_menu(x, y):  # Повернення в меню при кліку на кнопку
        nonlocal game_running
        if -440 < x < -360 and 310 < y < 340: game_running = False

    window.onclick(exit_to_menu)  # Реакція на клік
    window.listen();
    build_maze()  # Запуск прослуховування клавіш та мапи
    for i in range(num_players): move_setup(i)  # Активація управління

    winner_color = None
    while game_running:  # Основний ігровий цикл
        window.update()  # Оновлення кадрів
        alive, last_idx = 0, -1  # Підрахунок живих
        for i in range(num_players):
            t, b = players[i], bullets[i]
            if t.active:
                alive += 1;
                last_idx = i
                if b.state == "fire":  # Політ кулі
                    b.forward(15)
                    for j in range(num_players):  # Влучання в ворога
                        if i != j and players[j].active and b.distance(players[j]) < 22:
                            if explosion_fx: explosion_fx.play()  # Звук вибуху
                            b.state = "ready";
                            b.hideturtle()  # Куля зникає
                            if num_players == 2:  # Режим 1 на 1
                                scores[i] += 1
                                if scores[i] < 3:
                                    for k in range(2): players[k].goto(P_CONFIGS[k][6])  # Респавн
                                else:
                                    players[j].active = False; winner_color = t.name  # Фінал
                            else:
                                players[j].active = False; players[j].hideturtle()  # Battle Royale
                    for w in walls[:]:  # Влучання в стіну
                        if b.distance(w) < 20:
                            b.state = "ready";
                            b.hideturtle()
                            if settings["destructible_walls"]: w.hideturtle(); walls.remove(w)
                    if abs(b.xcor()) > 445 or abs(b.ycor()) > 345: b.state = "ready"; b.hideturtle()

        if (num_players > 2 and alive <= 1) or (num_players == 2 and max(scores) >= 3):
            if alive > 0: winner_color = players[last_idx].name
            game_running = False  # Зупинка циклу
        time.sleep(0.01)

    if winner_color:  # Екран переможця
        if victory_fx: victory_fx.play()
        window.clear();
        window.bgcolor(winner_color)
        m = turtle.Turtle();
        m.hideturtle();
        m.color("white")
        m.write(f"ПЕРЕМІГ {winner_color.upper()}!", align="center", font=("Arial", 40, "bold"))
        time.sleep(3)
    window.bye()  # Закриття Turtle