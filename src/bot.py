import math
import pygame
from typing import List
import const


class Bot:
    def __init__(
        self,
        window,
        x: float = 20,
        y: float = 20,
        size: float = const.BOT_SIZE,
        speed: float = 1,
    ):
        self.window = window
        self.x = x
        self.y = y

        self.speed = speed * const.BOT_SPEED
        self.size = size
        self.move_direction: List[float] = [0, 0]

        self.image = const.BOT_IMAGE.copy()
        self.image = pygame.transform.scale_by(self.image, size)
        self.rect = self.image.get_rect()

    def draw(self):
        self.window.blit(
            self.image,
            (
                self.x - const.BOT_SIZE / 2 * self.size,
                self.y - const.BOT_SIZE / 2 * self.size,
            ),
        )

    def get_rect(self):
        return self.rect

    def manual_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)

    def move(self, x, y):
        if x == 0 and y == 0:
            self.move_direction[0] = 0
            self.move_direction[1] = 0
            return

        mag = math.sqrt(x**2 + y**2)
        self.move_direction[0] = x / mag
        self.move_direction[1] = y / mag

    def update_pos(self, time=1 / 60):
        self.manual_pos(
            self.x + self.move_direction[0] * self.speed * time,
            self.y + self.move_direction[1] * self.speed * time,
        )


class BotRegistry:
    def __init__(self):
        self.bots = []
        self.bot_count = len(self.bots)

    def add(self, bot):
        self.bots.append(bot)
        self.bot_count = len(self.bots)
        return bot

    def remove(self, bot):
        self.bots.remove(bot)
        self.bot_count = len(self.bots)
        return bot

    def get_nearest(self, bot, count=math.inf):
        nearest = []
        for near in self.bots:
            if near == bot:
                continue
            elif len(nearest) == 0:
                nearest.append(near)
            else:
                for comp in nearest:
                    old_mag = pygame.math.Vector2(bot.x, bot.y).distance_to((
                        comp.x,
                        comp.y,
                    ))
                    new_mag = pygame.math.Vector2(bot.x, bot.y).distance_to((
                        near.x,
                        near.y,
                    ))

                    if new_mag < old_mag:
                        nearest.insert(nearest.index(comp), near)
                        if len(nearest) > count:
                            nearest.pop(-1)
                        break

        return nearest

    def get_in_range(self, bot, distance=math.inf):
        bots = []
        for near in self.bots:
            if near == bot:
                continue
            mag = pygame.math.Vector2(bot.x, bot.y).distance_to((
                near.x,
                near.y,
            ))
            if mag < distance:
                bots.append(near)

        return bots
