import pygame
import sys
from config import settings


def show_settings():
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