import pygame  # Двигун для меню
import turtle  # Графіка для бою
import time  # Робота з часом
import sys  # Повне закриття програми

# Глобальні налаштування гри
settings = {"destructible_walls": False}


def start_game_process(num_players):  # Головна функція гри
    try:
        pygame.display.quit()
        turtle.TurtleScreen._RUNNING = True
        window = turtle.Screen()
        window.clear()
        window.title("Танки 2026")
        window.bgcolor("black")
        window.setup(width=900, height=700)
        window.tracer(0)
    except:
        return

    def final_exit():
        try:
            window.bye()
        except:
            pass
        pygame.quit();
        sys.exit()

    window.getcanvas().winfo_toplevel().protocol("WM_DELETE_WINDOW", final_exit)

    def draw_menu_btn():  # Кнопка повернення
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

    draw_menu_btn()
    game_running = True

    def go_to_menu(x, y):
        nonlocal game_running
        if -440 < x < -360 and 310 < y < 340: game_running = False

    window.onclick(go_to_menu)

    walls = []  # Список стін

    def create_wall(x, y):
        w = turtle.Turtle();
        w.shape("square");
        w.color("#b35900");
        w.shapesize(1.2, 1.2);
        w.penup();
        w.goto(x, y);
        walls.append(w)

    def build_maze():  # Створення лабіринту
        for x in [-300, 0, 300]:
            for y in range(-250, 251, 40): create_wall(x, y)
        for y in [-150, 150]:
            for x in range(-400, 401, 40):
                if abs(x) > 50: create_wall(x, y)

    p_configs = [
        ("blue", "w", "s", "a", "d", "space", (-400, 300), 0),
        ("red", "Up", "Down", "Left", "Right", "Return", (400, -300), 180),
        ("green", "i", "k", "j", "l", "o", (400, 300), 180),
        ("yellow", "8", "5", "4", "6", "7", (-400, -300), 0),
        ("purple", "t", "g", "f", "h", "y", (0, 320), 270),
        ("orange", "v", "n", "b", "m", "comma", (0, -320), 90)
    ]

    players, bullets = [], []
    scores = [0] * num_players
    scoreboard = turtle.Turtle()
    scoreboard.hideturtle();
    scoreboard.penup();
    scoreboard.color("white");
    scoreboard.goto(0, 310)

    def update_scores():
        if num_players == 2:
            scoreboard.clear()
            scoreboard.write(f"Синій: {scores[0]} | Червоний: {scores[1]}", align="center", font=("Arial", 18, "bold"))

    for i in range(num_players):
        conf = p_configs[i];
        t = turtle.Turtle();
        t.shape("turtle");
        t.color(conf[0]);
        t.penup()
        t.goto(conf[6]);
        t.setheading(conf[7]);
        t.active = True;
        t.name = conf[0]
        b = turtle.Turtle();
        b.hideturtle();
        b.penup();
        b.shape("circle");
        b.shapesize(0.3);
        b.color("white");
        b.state = "ready"
        players.append(t);
        bullets.append(b)

    def reset_positions():
        for i in range(num_players):
            if players[i].active: players[i].goto(p_configs[i][6]); players[i].setheading(p_configs[i][7])
        update_scores()

    def can_move(t, dist):
        t.forward(dist)
        nx, ny = t.xcor(), t.ycor()
        if abs(nx) > 435 or abs(ny) > 335: t.backward(dist); return False
        for w in walls:
            if t.distance(w) < 26: t.backward(dist); return False
        t.backward(dist);
        return True

    def move_setup(idx):
        conf = p_configs[idx];
        t = players[idx];
        b = bullets[idx]
        window.onkey(lambda: t.forward(10) if can_move(t, 10) else None, conf[1])
        window.onkey(lambda: t.backward(10) if can_move(t, -10) else None, conf[2])
        window.onkey(lambda: t.left(15), conf[3]);
        window.onkey(lambda: t.right(15), conf[4])

        def fire():
            if b.state == "ready" and t.active:
                b.state = "fire";
                b.goto(t.pos());
                b.setheading(t.heading());
                b.showturtle()

        window.onkey(fire, conf[5])

    window.listen();
    build_maze();
    update_scores()
    for i in range(num_players): move_setup(i)

    winner_color = None
    while game_running:
        try:
            window.update()
            alive_count, last_idx = 0, -1
            for i in range(num_players):
                t, b = players[i], bullets[i]
                if t.active:
                    alive_count += 1;
                    last_idx = i
                    if b.state == "fire":
                        b.forward(15)
                        for j in range(num_players):
                            if i != j and players[j].active and b.distance(players[j]) < 22:
                                b.state = "ready";
                                b.hideturtle()
                                if num_players == 2:
                                    scores[i] += 1
                                    if scores[i] < 3:
                                        reset_positions()
                                    else:
                                        players[j].active = False; winner_color = t.name
                                else:
                                    players[j].active = False; players[j].hideturtle()

                        for w in walls[:]:  # Перевірка стін
                            if b.distance(w) < 20:
                                b.state = "ready";
                                b.hideturtle()
                                if settings["destructible_walls"]:  # ЯКЩО УКЛЮЧЕНО РУЙНУВАННЯ
                                    w.hideturtle();
                                    walls.remove(w)  # Видаляємо стіну
                        if abs(b.xcor()) > 445 or abs(b.ycor()) > 345: b.state = "ready"; b.hideturtle()

            if (num_players > 2 and alive_count <= 1) or (num_players == 2 and (scores[0] == 3 or scores[1] == 3)):
                winner_color = players[last_idx].name;
                break
            time.sleep(0.01)
        except:
            final_exit()

    if winner_color and game_running:
        window.clear();
        window.bgcolor(winner_color);
        draw_menu_btn()
        m = turtle.Turtle();
        m.hideturtle();
        m.color("white");
        m.write(f"ПЕРЕМІГ {winner_color.upper()}!", align="center", font=("Arial", 40, "bold"))
        while game_running:
            try:
                window.update(); time.sleep(0.1)
            except:
                final_exit()
    window.bye();
    main()


def show_settings():  # Вікно налаштувань
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont("Arial", 30, bold=True)
    back_btn = pygame.Rect(50, 50, 150, 50)
    toggle_btn = pygame.Rect(300, 250, 200, 60)

    while True:
        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, (200, 200, 200), back_btn)
        screen.blit(font.render("НАЗАД", True, (0, 0, 0)), (70, 60))

        status = "ТАК" if settings["destructible_walls"] else "НІ"
        color = (0, 255, 0) if settings["destructible_walls"] else (255, 0, 0)

        screen.blit(font.render("РУЙНУВАННЯ СТІН:", True, (255, 255, 255)), (250, 200))
        pygame.draw.rect(screen, color, toggle_btn)
        screen.blit(font.render(status, True, (0, 0, 0)), (360, 265))

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(ev.pos): return
                if toggle_btn.collidepoint(ev.pos): settings["destructible_walls"] = not settings["destructible_walls"]
        pygame.display.flip()


def show_shop():  # Вікно магазину
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont("Arial", 40, bold=True)
    back_btn = pygame.Rect(50, 50, 150, 50)

    while True:
        screen.fill((10, 10, 25))
        pygame.draw.rect(screen, (200, 200, 200), back_btn)
        screen.blit(pygame.font.SysFont("Arial", 25).render("НАЗАД", True, (0, 0, 0)), (75, 60))
        screen.blit(font.render("МАГАЗИН ПОКИ ПУСТИЙ", True, (255, 255, 0)), (150, 250))
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(ev.pos): return
        pygame.display.flip()


def start_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont("Arial", 22, bold=True)
    btns = [
        (pygame.Rect(275, 100, 250, 50), "1 VS 1", "G2"),
        (pygame.Rect(275, 170, 250, 50), "BATTLE ROYALE (4)", "G4"),
        (pygame.Rect(275, 240, 250, 50), "BATTLE ROYALE (6)", "G6"),
        (pygame.Rect(275, 310, 250, 50), "МАГАЗИН", "SHOP"),
        (pygame.Rect(275, 380, 250, 50), "НАЛАШТУВАННЯ", "SETS")
    ]

    while True:
        screen.fill((15, 15, 15))
        for br, txt, val in btns:
            pygame.draw.rect(screen, (255, 255, 255), br, 2)
            screen.blit(font.render(txt, True, (255, 255, 255)), (br.x + 20, br.y + 12))
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                for br, tx, v in btns:
                    if br.collidepoint(ev.pos): return v
        pygame.display.flip()


def main():
    while True:
        res = start_menu()
        if res == "G2":
            start_game_process(2)
        elif res == "G4":
            start_game_process(4)
        elif res == "G6":
            start_game_process(6)
        elif res == "SHOP":
            show_shop()
        elif res == "SETS":
            show_settings()


if __name__ == "__main__": main()