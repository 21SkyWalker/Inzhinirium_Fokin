import pygame
import sys
import random
from snake import Snake
from food import Food
from database import Database
import sqlite3

# Инициализация pygame
pygame.init()

WIDTH, HEIGHT = 480, 480
BLOCK_SIZE = 20
GRID_BLOCKS = WIDTH // BLOCK_SIZE
VELOCITY = 20
SNAKE_COLOR = (255, 0, 0)
FOOD_COLOR = (26, 237, 139)
WHITE = (255, 255, 255)

# Создание окна
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("eSnake Fokin")

# Функция для ввода никнейма игрока
def get_user_nickname():
    nickname = ""
    input_box = pygame.Rect(150, 200, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        window.fill(WHITE)
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        window.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(window, color, input_box, 2)
        pygame.display.flip()

# Создание объекта базы данных
db = Database()

# Функция для отображения лучших результатов
def show_top_scores(db):
    top_scores = db.get_top_scores()
    font = pygame.font.Font(None, 36)
    y = 50

    window.fill(WHITE)
    for i, (nickname, score) in enumerate(top_scores, 1):
        text = f"{i}. {nickname}: {score}"
        score_text = font.render(text, True, (0, 0, 0))
        window.blit(score_text, (150, y))
        y += 40

    pygame.display.flip()
    pygame.time.delay(5000)

# Главная функция игры
def main():
    nickname = get_user_nickname()
    snake = Snake(WIDTH, HEIGHT, BLOCK_SIZE)
    food = Food(WIDTH, HEIGHT, BLOCK_SIZE)
    score = 0
    font = pygame.font.SysFont("comicsansms", 32)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db.conn.close()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction("up")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("down")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("left")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("right")

        snake.move()

        snake.grow()
        if snake.x == food.x and snake.y == food.y:
            score += 1
            food = Food(WIDTH, HEIGHT, BLOCK_SIZE)
        else:
            snake.body.pop(0)

        window.fill(WHITE)
        food.draw(window)
        snake.draw(window)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        window.blit(score_text, (10, 10))
        pygame.display.update()
        pygame.time.delay(100)

        if snake.collision():
            db.insert_score(nickname, score)
            show_top_scores(db)

if __name__ == "__main__":
    main()