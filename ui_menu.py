import pygame  # Графіка меню
import sys  # Вихід із системи
from config import BACKGROUND_IMAGE, settings  # Імпорт налаштувань


def draw_bg(screen):  # Малювання фону меню
    try:
        bg = pygame.image.load(BACKGROUND_IMAGE)  # Завантаження картинки
        bg = pygame.transform.scale(bg, (screen.get_width(), screen.get_height()))  # Розтягування
        screen.blit(bg, (0, 0))  # Відображення
    except:
        screen.fill((15, 15, 15))  # Якщо немає фото — чорний фон


def show_settings():  # Вікно налаштувань
    screen = pygame.display.set_mode((800, 600))  # Розмір вікна
    font = pygame.font.SysFont("Arial", 30, bold=True)  # Шрифт
    back_btn = pygame.Rect(50, 50, 150, 50)  # Координати кнопки "Назад"
    toggle_btn = pygame.Rect(300, 250, 200, 60)  # Кнопка перемикача стін
    while True:  # Цикл вікна
        draw_bg(screen)  # Малюємо фон
        pygame.draw.rect(screen, (200, 200, 200), back_btn)  # Кнопка назад
        screen.blit(font.render("НАЗАД", True, (0, 0, 0)), (70, 60))  # Текст назад

        st_text = "ТАК" if settings["destructible_walls"] else "НІ"  # Текст статусу стін
        color = (0, 255, 0) if settings["destructible_walls"] else (255, 0, 0)  # Колір статусу
        pygame.draw.rect(screen, color, toggle_btn)  # Малюємо перемикач
        screen.blit(font.render(st_text, True, (0, 0, 0)), (360, 265))  # Текст на кнопці

        for ev in pygame.event.get():  # Обробка подій
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()  # Закриття
            if ev.type == pygame.MOUSEBUTTONDOWN:  # Клік мишкою
                if back_btn.collidepoint(ev.pos): return  # Повернення в меню
                if toggle_btn.collidepoint(ev.pos): settings["destructible_walls"] = not settings["destructible_walls"]
        pygame.display.flip()  # Оновлення екрана


def start_menu():  # Головне меню
    pygame.init()  # Запуск Pygame
    screen = pygame.display.set_mode((800, 600))  # Вікно
    font = pygame.font.SysFont("Arial", 22, bold=True)  # Шрифт
    btns = [  # Список кнопок меню
        (pygame.Rect(275, 100, 250, 50), "1 VS 1", "G2"),
        (pygame.Rect(275, 170, 250, 50), "BATTLE ROYALE (4)", "G4"),
        (pygame.Rect(275, 240, 250, 50), "BATTLE ROYALE (6)", "G6"),
        (pygame.Rect(275, 310, 250, 50), "МАГАЗИН", "SHOP"),
        (pygame.Rect(275, 380, 250, 50), "НАЛАШТУВАННЯ", "SETS")
    ]
    while True:
        draw_bg(screen)
        for br, txt, val in btns:  # Малюємо всі кнопки зі списку
            pygame.draw.rect(screen, (255, 255, 255), br, 2)  # Контур кнопки
            screen.blit(font.render(txt, True, (255, 255, 255)), (br.x + 20, br.y + 12))  # Текст
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                for br, tx, v in btns:  # Перевірка кліку по кнопках
                    if br.collidepoint(ev.pos): return v  # Повертаємо вибір
        pygame.display.flip()