import pygame

# Глобальні стани
settings = {"destructible_walls": False}

# Шаблон параметрів: (Колір, Вперед, Назад, Ліво, Право, Постріл, Позиція, Кут)
PLAYER_CONFIGS = [
    ("blue", "w", "s", "a", "d", "space", (-400, 300), 0),
    ("red", "Up", "Down", "Left", "Right", "Return", (400, -300), 180),
    ("green", "i", "k", "j", "l", "o", (400, 300), 180),
    ("yellow", "8", "5", "4", "6", "7", (-400, -300), 0),
    ("purple", "t", "g", "f", "h", "y", (0, 320), 270),
    ("orange", "v", "n", "b", "m", "comma", (0, -320), 90)
]