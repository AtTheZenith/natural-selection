import math
import random
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
        range: float = 1,
        energy: float = 1,
        team: int = 1,
    ):
        self.window = window
        self.x = x
        self.y = y
        self.energy: float = energy * const.MAX_ENERGY

        self.speed = min(const.BOT_MAX_SPEED, max(const.BOT_MIN_SPEED, speed))
        self.true_speed = speed * const.BOT_SPEED
        self.size = min(const.BOT_MAX_SIZE, max(const.BOT_MIN_SIZE, size))
        self.true_size = size * const.BOT_SIZE
        self.range = range
        self.true_range = range * const.BOT_RANGE + (self.true_size * 0.75)
        self.team = team
        self.move_direction: List[float] = [0, 0]

        self.image = const.BOT_IMAGES[team].copy()
        self.image = pygame.transform.scale_by(
            self.image, size * (const.BOT_SIZE / self.image.get_size()[1])
        )

    def draw(self):
        if self.energy <= 0:
            return
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

    def update(self, time: float = const.FRAME_RATE):
        self.manual_pos(
            self.x + self.move_direction[0] * self.true_speed * time,
            self.y + self.move_direction[1] * self.true_speed * time,
        )

        self.energy -= (
            (
                (self.size**2) * 10
                + (
                    math.hypot(self.move_direction[0], self.move_direction[1])
                    * self.speed**2
                )
                * 2
                + (self.range**2.5) * 3  # + self.range
            )
            * time
            * 2
        )

    def add_energy(self, energy: float):
        self.energy = min(self.energy + energy, const.MAX_ENERGY)

    def reproduce(self):
        self.energy -= const.REPRODUCTION_COST
        new_bot = Bot(
            self.window,
            self.x,
            self.y,
            self.size + (random.random() / 5 - 0.1),
            # self.size,
            self.speed + (random.random() * 2 / 5 - 0.2),
            self.range + (random.random() / 5 - 0.1),
            self.energy / 2 / const.MAX_ENERGY,
            self.team,
        )
        print(
            f"New bot created:\nSize: {new_bot.size}\nSpeed: {new_bot.speed}\nRange: {new_bot.range}"
        )

        return new_bot


class BotRegistry:
    def __init__(self):
        self.bots: List[Bot] = []
        self.bot_count = len(self.bots)

    def add(self, bot: Bot):
        self.bots.append(bot)
        self.bot_count = len(self.bots)
        return bot

    def remove(self, bot: Bot):
        if bot and isinstance(bot, Bot) and bot in self.bots:
            self.bots.remove(bot)
            self.bot_count = len(self.bots)
            return bot
        else:
            return False

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

    def get_in_range(self, bot, distance: float = const.BOT_RANGE):
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

    def energy_cycle(self):
        for bot in self.bots:
            if bot.energy <= 0:
                self.bots.remove(bot)
                self.energy_cycle()

    def reproduce_cycle(self):
        for bot in self.bots:
            if bot.energy >= const.REPRODUCTION_MINIMUM:
                self.add(bot.reproduce())
                self.reproduce_cycle()
