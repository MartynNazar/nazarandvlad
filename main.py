import ui_menu # Файл інтерфейсу
import game_engine # Файл гри
import pygame # Базова бібліотека
import sys # Системні функції

def main(): # Головна точка входу
    while True: # Нескінченний цикл програми
        choice = ui_menu.start_menu() # Отримуємо вибір користувача з меню
        if choice in ["G2", "G4", "G6"]: # Якщо вибрано гру
            num = int(choice[1]) # Визначаємо кількість гравців із рядка
            game_engine.start_game(num) # Запускаємо гру
        elif choice == "SETS": # Якщо вибрано налаштування
            ui_menu.show_settings() # Відкриваємо вікно налаштувань
        elif choice == "SHOP": # Якщо магазин
            pass # (Можна додати пізніше)

if __name__ == "__main__": # Перевірка прямого запуску
    main() # Виклик головної функції