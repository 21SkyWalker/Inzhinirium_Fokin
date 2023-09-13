import pygame
import sys
import random
import sqlite3

pygame.init()


WIDTH, HEIGHT = 480, 480
BLOCK_SIZE = 20
GRID_BLOCKS = WIDTH // BLOCK_SIZE
VELOCITY = 20
SNAKE_COLOR = (255, 0, 0)
FOOD_COLOR = (26, 237, 139)
WHITE = (255, 255, 255)


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("eSnake Fokin")

class Food:
    def __init__(self):
        self.x = random.randrange(0, GRID_BLOCKS) * BLOCK_SIZE
        self.y = random.randrange(0, GRID_BLOCKS) * BLOCK_SIZE

    def draw(self):
        pygame.draw.rect(window, FOOD_COLOR, (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))

class Snake:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.body = []
        self.direction = "right"

    def move(self):
        if self.direction == "right":
            self.x += VELOCITY
        elif self.direction == "left":
            self.x -= VELOCITY
        elif self.direction == "up":
            self.y -= VELOCITY
        elif self.direction == "down":
            self.y += VELOCITY

    def change_direction(self, new_direction):
        if (new_direction == "right" and self.direction != "left") or \
           (new_direction == "left" and self.direction != "right") or \
           (new_direction == "up" and self.direction != "down") or \
           (new_direction == "down" and self.direction != "up"):
            self.direction = new_direction

    def collision(self):
        if self.x >= WIDTH or self.x < 0 or self.y >= HEIGHT or self.y < 0:
            return True
        for segment in self.body[:-1]:
            if segment == (self.x, self.y):
                return True
        return False

    def grow(self):
        self.body.append((self.x, self.y))

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(window, SNAKE_COLOR, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(window, SNAKE_COLOR, (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))


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
        nn_txt = font.render(f"Enter your nickname:", True, ('dodgerblue2'))
        window.blit(nn_txt, (10, 10))
        pygame.draw.rect(window, color, input_box, 2)
        pygame.display.flip()
    return nickname


conn = sqlite3.connect("snake_scores.db")
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS scores (nickname TEXT, score INT)''')
conn.commit()


def show_top_scores():
    top_scores = cursor.execute('''SELECT nickname, score FROM scores ORDER BY score DESC LIMIT 5''').fetchall()
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

def main():
    nickname = get_user_nickname()  
    snake = Snake()
    food = Food()
    score = 0
    font = pygame.font.SysFont("comicsansms", 32)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                conn.close()
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
            food = Food()
        else:
            snake.body.pop(0)

        window.fill(WHITE)
        food.draw()
        snake.draw()
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        window.blit(score_text, (10, 10))
        pygame.display.update()
        pygame.time.delay(100)

        if snake.collision():
            cursor.execute("INSERT INTO scores (nickname, score) VALUES (?, ?)", (nickname, score))
            conn.commit()
            show_top_scores()

if __name__ == "__main__":
    main()