import pygame
import turtle
import time
import sys
import os
import random  # Додано для випадкових мап

# Глобальні налаштування
settings = {"destructible_walls": False}
BACKGROUND_IMAGE = "tanks.gif"
SHOOT_SOUND = "shoot.wav"
EXPLOSION_SOUND = "explosion.wav"
VICTORY_SOUND = "victory.wav"

# --- Ініціалізація звуку ---
pygame.mixer.init()


def load_sound(file):
    try:
        return pygame.mixer.Sound(file)
    except:
        return None


shoot_fx = load_sound(SHOOT_SOUND)
explosion_fx = load_sound(EXPLOSION_SOUND)
victory_fx = load_sound(VICTORY_SOUND)


def start_game_process(num_players):
    try:
        pygame.display.quit()
        turtle.TurtleScreen._RUNNING = True
        window = turtle.Screen()
        window.clear()
        window.title("Танки 2026")

        if os.path.exists(BACKGROUND_IMAGE):
            try:
                window.bgpic(BACKGROUND_IMAGE)
            except:
                window.bgcolor("black")
        else:
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
        pygame.quit()
        sys.exit()

    window.getcanvas().winfo_toplevel().protocol("WM_DELETE_WINDOW", final_exit)

    def draw_menu_btn():
        btn = turtle.Turtle();
        btn.hideturtle();
        btn.speed(0)
        btn.color("white");
        btn.penup();
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

    walls = []

    def create_wall(x, y):
        w = turtle.Turtle()
        w.shape("square")
        # Новий вигляд: Неоновий кристал (колір контуру і заливки)
        w.color("#00fbff", "#00008b")
        w.shapesize(1.3, 1.3)
        w.penup()
        w.goto(x, y)
        walls.append(w)

    def build_maze():
        # Список точок, де з'являються танки (спавни)
        spawns = [(-400, 300), (400, -300), (400, 300), (-400, -300), (0, 320), (0, -320)]

        # Генеруємо стіни по сітці
        for x in range(-360, 361, 60):
            for y in range(-280, 281, 60):
                # Перевіряємо, щоб стіна не закрила танк на старті
                safe = True
                for sx, sy in spawns:
                    if abs(x - sx) < 100 and abs(y - sy) < 100:
                        safe = False

                # 25% шанс появи стіни в цій клітинці
                if safe and random.random() < 0.25:
                    create_wall(x, y)

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
    scoreboard = turtle.Turtle();
    scoreboard.hideturtle();
    scoreboard.penup()
    scoreboard.color("white");
    scoreboard.goto(0, 310)

    def update_scores():
        if num_players == 2:
            scoreboard.clear()
            scoreboard.write(f"Синій: {scores[0]} | Червоний: {scores[1]}", align="center", font=("Arial", 18, "bold"))

    for i in range(num_players):
        conf = p_configs[i]
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
        b.shape("circle")
        b.shapesize(0.3);
        b.color("white");
        b.state = "ready"
        players.append(t);
        bullets.append(b)

    def can_move(t, dist):
        t.forward(dist)
        nx, ny = t.xcor(), t.ycor()
        if abs(nx) > 435 or abs(ny) > 335: t.backward(dist); return False
        for w in walls:
            if t.distance(w) < 28: t.backward(dist); return False
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
                if shoot_fx: shoot_fx.play()
                b.state = "fire";
                b.goto(t.pos());
                b.setheading(t.heading());
                b.showturtle()

        window.onkey(fire, conf[5])

    window.listen()
    build_maze()
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
                                if explosion_fx: explosion_fx.play()
                                b.state = "ready";
                                b.hideturtle()
                                if num_players == 2:
                                    scores[i] += 1
                                    if scores[i] < 3:
                                        for k in range(num_players):
                                            if players[k].active: players[k].goto(p_configs[k][6])
                                        update_scores()
                                    else:
                                        players[j].active = False; winner_color = t.name
                                else:
                                    players[j].active = False;
                                    players[j].hideturtle()

                        for w in walls[:]:
                            if b.distance(w) < 20:
                                b.state = "ready";
                                b.hideturtle()
                                if settings["destructible_walls"]: w.hideturtle(); walls.remove(w)
                        if abs(b.xcor()) > 445 or abs(b.ycor()) > 345: b.state = "ready"; b.hideturtle()

            if (num_players > 2 and alive_count <= 1) or (num_players == 2 and (scores[0] == 3 or scores[1] == 3)):
                if alive_count > 0: winner_color = players[last_idx].name
                break
            time.sleep(0.01)
        except:
            final_exit()

    if winner_color and game_running:
        if victory_fx: victory_fx.play()
        window.clear();
        window.bgcolor(winner_color);
        draw_menu_btn()
        m = turtle.Turtle();
        m.hideturtle();
        m.color("white")
        m.write(f"ПЕРЕМІГ {winner_color.upper()}!", align="center", font=("Arial", 40, "bold"))
        while game_running:
            try:
                window.update(); time.sleep(0.1)
            except:
                final_exit()
    window.bye();
    main()


# --- ФУНКЦІЇ МЕНЮ (Pygame) ---
def draw_bg_pygame(screen):
    try:
        bg = pygame.image.load(BACKGROUND_IMAGE)
        bg = pygame.transform.scale(bg, (screen.get_width(), screen.get_height()))
        screen.blit(bg, (0, 0))
    except:
        screen.fill((15, 15, 15))


def show_settings():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont("Arial", 30, bold=True)
    back_btn = pygame.Rect(50, 50, 150, 50)
    toggle_btn = pygame.Rect(300, 250, 200, 60)
    while True:
        draw_bg_pygame(screen)
        pygame.draw.rect(screen, (200, 200, 200), back_btn)
        screen.blit(font.render("НАЗАД", True, (0, 0, 0)), (70, 60))
        label = font.render("РУЙНУВАННЯ СТІН:", True, (255, 255, 255))
        screen.blit(label, (250, 200))
        status = "ТАК" if settings["destructible_walls"] else "НІ"
        color = (0, 255, 0) if settings["destructible_walls"] else (255, 0, 0)
        pygame.draw.rect(screen, color, toggle_btn)
        screen.blit(font.render(status, True, (0, 0, 0)), (360, 265))
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(ev.pos): return
                if toggle_btn.collidepoint(ev.pos): settings["destructible_walls"] = not settings["destructible_walls"]
        pygame.display.flip()


def show_shop():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    back_btn = pygame.Rect(50, 50, 150, 50)
    while True:
        draw_bg_pygame(screen)
        pygame.draw.rect(screen, (200, 200, 200), back_btn)
        screen.blit(pygame.font.SysFont("Arial", 25).render("НАЗАД", True, (0, 0, 0)), (75, 60))
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
        draw_bg_pygame(screen)
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


if __name__ == "__main__":
    main()