import pygame

class Snake:
    def __init__(self, WIDTH, HEIGHT, BLOCK_SIZE):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.BLOCK_SIZE = BLOCK_SIZE
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.body = []
        self.direction = "right"

    def move(self):
        if self.direction == "right":
            self.x = (self.x + self.BLOCK_SIZE) % self.WIDTH
        elif self.direction == "left":
            self.x = (self.x - self.BLOCK_SIZE) % self.WIDTH
        elif self.direction == "up":
            self.y = (self.y - self.BLOCK_SIZE) % self.HEIGHT
        elif self.direction == "down":
            self.y = (self.y + self.BLOCK_SIZE) % self.HEIGHT

    def change_direction(self, new_direction):
        if (new_direction == "right" and self.direction != "left") or \
           (new_direction == "left" and self.direction != "right") or \
           (new_direction == "up" and self.direction != "down") or \
           (new_direction == "down" and self.direction != "up"):
            self.direction = new_direction

    def collision(self):
        if self.x >= self.WIDTH or self.x < 0 or self.y >= self.HEIGHT or self.y < 0:
            return True
        for segment in self.body[:-1]:
            if segment == (self.x, self.y):
                return True
        return False

    def grow(self):
        self.body.append((self.x, self.y))

    def draw(self, window):
        for segment in self.body:
            pygame.draw.rect(window, (255, 0, 0), (segment[0], segment[1], self.BLOCK_SIZE, self.BLOCK_SIZE))
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.BLOCK_SIZE, self.BLOCK_SIZE))