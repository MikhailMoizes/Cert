# Класс для игрока
import pygame
from constants import WIDTH, HEIGHT

class Player:
    def __init__(self, name, size = 30):
        self.name = name
        self.size = size
        self.score = 0
        self.rect = pygame.Rect(WIDTH //2, HEIGHT - 50, size, size)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    @property
    def position(self):
        return self.rect.x,  self.rect.y
