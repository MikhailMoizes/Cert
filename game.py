
import time
import pygame
from constants import *
from BD import Database
from player import Player
from enemy import Enemy


# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Настройки шрифта
font = pygame.font.Font(None, 36)

pygame.display.set_caption("Регистрация")
player_name = ''


# Функция для отображения текста на экране
def draw_text(surface, text, pos):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, 'black')
    surface.blit(text_surface, pos)


def registration():
    global player_name
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if input_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Нажатие Enter
                        input_active = False  # Завершение регистрации
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]  # Удаление последнего символа
                    else:
                        player_name += event.unicode  # Добавление символа

        screen.fill(WHITE)
        draw_text(screen, 'Введите имя пользователя:', (20, 50))
        draw_text(screen, player_name, (20, 100))
        draw_text(screen, 'Нажмите Enter для завершения', (20, 150))
        draw_text(screen, f'Для управления игрой клавиши управления курсора', (20, 200))
        pygame.display.flip()


# старт игры
def game():
    def draw_multiline_text(surface, text_lines, position):
        y_offset = 0
        for line in text_lines:
            text_surface = font.render(line, True, BLACK)
            surface.blit(text_surface, (position[0], position[1] + y_offset))
            y_offset += text_surface.get_height()

    # Запрос имени игрока
    player = Player(player_name)

    db = Database()
    pygame.display.set_caption("Приветствую игрока " + player.name)
    clock = pygame.time.Clock()
    objects = Enemy(10, 10)
    start_time_enemy = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1, 0)

        if keys[pygame.K_RIGHT]:
            player.move(1, 0)

        if keys[pygame.K_UP]:
            player.move(0, -1)

        if keys[pygame.K_DOWN]:
            player.move(0, 1)

        screen.fill(WHITE)

        # Отображение игрока
        pygame.draw.rect(screen, GREEN, player.rect)

        # Движение объектов вниз
        for obj in objects.objects:
            obj += 1

        for obj in objects.objects:
            pygame.draw.circle(screen, 'RED', (obj.x, obj.y), objects.object_size // 2)

        # Отображение очков
        draw_text(screen, f"Очки: {player.score:.2f} ",
                  (10, 10))

        # добавляем врага, удаляем пролетевших мимо
        current_time = pygame.time.get_ticks()
        if current_time - start_time_enemy >= spawn_time:
            start_time_enemy = current_time
            objects.add(level=1)

        # Проверка условий выигрыша/проигрыша (например, выход за границы)
        for obj in objects.objects:
            player_x, player_y = player.position
            # подсчитываем пролетевших мимо
            if obj > player and obj.object_size:
                player.score += 1
                obj.object_size = 0
            # Проверка на столкновение
            if obj < player or (player_x < 0 or player_x > WIDTH or player_y < 0 or player_y > HEIGHT):
                draw_text(screen, "Игра закончилась!", (WIDTH // 2 - 50, HEIGHT // 2))

                db.add_score(player.name, player.score)
                # Вывод топ-5 игроков
                top_scores = db.get_top_scores()
                text = ["Топ-5 игроков:"]
                for i, (name, score) in enumerate(top_scores, 1):
                    text.append(f"{i}. {name} - {score:.2f}")

                draw_multiline_text(screen, text, (50, 50))
                running = False

        pygame.display.flip()
        clock.tick(FPS)

    db.close()
    time.sleep(5)
    pygame.quit()


if __name__ == "__main__":
    registration()  # Переход к окну регистрации
    game()  # Переход к игровому окну
