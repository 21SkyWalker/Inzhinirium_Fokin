import random
import pygame

class Food:
    def __init__(self, WIDTH, HEIGHT, BLOCK_SIZE):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.BLOCK_SIZE = BLOCK_SIZE
        self.x = random.randrange(0, self.WIDTH, self.BLOCK_SIZE)
        self.y = random.randrange(0, self.HEIGHT, self.BLOCK_SIZE)

    def draw(self, window):
        pygame.draw.rect(window, (26, 237, 139), (self.x, self.y, self.BLOCK_SIZE, self.BLOCK_SIZE))