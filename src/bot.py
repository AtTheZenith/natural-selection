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
        size: float = 1,
        speed: float = 1,
        range: float = 3,
    ):
        self.window = window
        self.x = x
        self.y = y
        self.energy: float = const.MAX_ENERGY

        self.speed = speed
        self.true_speed = speed * const.BOT_SPEED
        self.size = size
        self.true_size = size * const.BOT_SIZE
        self.range = range
        self.true_range = range * const.BOT_SIZE / 4 + (
            self.true_size * math.sqrt(2) / 2
        )
        self.move_direction: List[float] = [0, 0]

        self.image = const.BOT_IMAGE.copy()
        self.image = pygame.transform.scale_by(self.image, size)

    def draw(self):
        self.window.blit(
            self.image,
            (
                self.x - const.BOT_SIZE / 2 * self.size,
                self.y - const.BOT_SIZE / 2 * self.size,
            ),
        )

    def get_rect(self):
        return self.image.get_rect()

    def manual_pos(self, x, y):
        self.x = x
        self.y = y
        self.image.get_rect().center = (self.x, self.y)

    def move(self, x, y):
        if x == 0 and y == 0:
            self.move_direction[0] = 0
            self.move_direction[1] = 0
            return

        mag = math.sqrt(x**2 + y**2)
        self.move_direction[0] = x / mag
        self.move_direction[1] = y / mag

    def update(self, time=const.FRAME_RATE):
        self.manual_pos(
            self.x + self.move_direction[0] * self.true_speed / time,
            self.y + self.move_direction[1] * self.true_speed / time,
        )

        self.energy -= (
            (self.size * 10) * (self.speed**2) + self.true_range
        ) / const.FRAME_RATE

    def add_energy(self, energy: float):
        self.energy = min(self.energy + energy, const.MAX_ENERGY)


class BotRegistry:
    def __init__(self):
        self.bots: List[Bot] = []
        self.bot_count = len(self.bots)

    def add(self, bot):
        self.bots.append(bot)
        self.bot_count = len(self.bots)
        return bot

    def remove(self, bot):
        self.bots.remove(bot)
        self.bot_count = len(self.bots)
        return bot

    def get_nearest(self, bot, count=5):
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

    def get_in_range(self, bot, distance=const.BOT_RANGE):
        in_range = []
        for sel in self.bots:
            if sel == bot:
                continue
            mag = pygame.math.Vector2(bot.x, bot.y).distance_to((
                sel.x,
                sel.y,
            ))
            if mag < distance:
                in_range.append(sel)

        return in_range

    def check_energy(self):
        for bot in self.bots:
            if bot.energy <= 0:
                self.bots.remove(bot)
                self.check_energy()
