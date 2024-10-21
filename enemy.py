# класс врага
import random
from constants import *


class Point:
    def __init__(self, object_size=5, y=HEIGHT // 4):
        self.object_size = object_size
        self.x = random.randint(0, WIDTH - object_size)
        self.y = y

    def __repr__(self):
        return f"{self.x} {self.y}"

    def __add__(self, other):
        self.y += other

    def __lt__(self, player):
        player_x, player_y = player.position
        return ((player_x < self.x < player_x + player.size or player_x < self.x
                 + self.object_size < player_x + player.size) and
                (player_y < self.y < player_y + player.size or player_y < self.y
                 + self.object_size < player_y + player.size))

    def __gt__(self, player):
        player_x, player_y = player.position
        return (self.y > player_y + player.size)


class Enemy:
    def __init__(self, object_size=5, enemy=50):
        self.object_size = object_size
        self.enemy = enemy
        # добавляем врагов
        self.objects = [Point(self.object_size, random.randint(0, HEIGHT // 4)) for _ in range(enemy)]

    def add(self, level):
        for _ in range(level * 5):
            self.objects.append(Point(self.object_size, random.randint(0, HEIGHT // 5)))
        i = 0
        self.enemy = len(self.objects)
        while i < self.enemy:

            if len(self.objects) and (self.objects[i].x < 0 or self.objects[i].x > WIDTH or
                                      self.objects[i].y < 0 or self.objects[i].y > HEIGHT):
                del self.objects[i]
                self.enemy -= 1
                continue
            i += 1
