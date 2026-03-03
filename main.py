import pygame, turtle, time, sys
from config import settings, PLAYER_CONFIGS
import templates as tmp
import mechanics as mech
import ui_screens as ui


def start_game_process(num_players):
    try:
        pygame.display.quit()
        turtle.TurtleScreen._RUNNING = True
        window = turtle.Screen()
        window.clear()
        window.bgcolor("black")
        window.setup(width=900, height=700)
        window.tracer(0)
    except:
        return

    game_running = True
    walls = []
    players = []
    bullets = []

    # Використовуємо шаблони з інших файлів
    mech.build_maze(walls, tmp.create_wall_segment)

    for i in range(num_players):
        conf = PLAYER_CONFIGS[i]
        t = tmp.create_tank(conf[0], conf[6], conf[7], conf[0])
        b = tmp.create_bullet()
        players.append(t);
        bullets.append(b)

        # Керування
        window.onkey(lambda t=t: t.forward(10) if mech.can_move(t, 10, walls) else None, conf[1])
        window.onkey(lambda t=t: t.backward(10) if mech.can_move(t, -10, walls) else None, conf[2])
        window.onkey(lambda t=t: t.left(15), conf[3])
        window.onkey(lambda t=t: t.right(15), conf[4])

        def fire(b=b, t=t):
            if b.state == "ready" and t.active:
                b.state = "fire";
                b.goto(t.pos());
                b.setheading(t.heading());
                b.showturtle()

        window.onkey(fire, conf[5])

    window.listen()

    # ГОЛОВНИЙ ЦИКЛ БОЮ
    while game_running:
        try:
            window.update()
            for i in range(num_players):
                t, b = players[i], bullets[i]
                if t.active and b.state == "fire":
                    b.forward(15)
                    # Колізії з гравцями
                    for j in range(num_players):
                        if i != j and players[j].active and b.distance(players[j]) < 22:
                            players[j].active = False;
                            players[j].hideturtle()
                            b.state = "ready";
                            b.hideturtle()
                    # Колізії зі стінами
                    for w in walls[:]:
                        if b.distance(w) < 20:
                            b.state = "ready";
                            b.hideturtle()
                            if settings["destructible_walls"]:
                                w.hideturtle();
                                walls.remove(w)
            time.sleep(0.01)
        except:
            break
    window.bye();
    main()


def main():
    while True:
        res = ui.start_menu()
        if res == "G2":
            start_game_process(2)
        elif res == "G4":
            start_game_process(4)
        elif res == "G6":
            start_game_process(6)
        elif res == "SETS":
            ui.show_settings()
        elif res == "SHOP":
            pass  # Магазин можна додати аналогічно


if __name__ == "__main__":
    main()