import pygame
from typing import List
from bot import Bot
import collision
import const


class Food:
    def __init__(self, window, x: float = 20, y: float = 20, energy: float = 10):
        self.window = window
        self.x = x
        self.y = y
        self.energy = energy

        self.image = const.FOOD_IMAGE.copy()
        self.image = pygame.transform.scale_by(self.image, const.FOOD_SIZE / self.image.get_size()[1])
        self.get_rect = self.image.get_rect

    def draw(self):
        self.window.blit(
            self.image,
            (
                self.x - const.FOOD_SIZE / 2,
                self.y - const.FOOD_SIZE / 2,
            ),
        )

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.get_rect().center = (self.x, self.y)

    def is_colliding(self, bot: Bot):
        return const.BOT_SIZE + const.FOOD_SIZE > pygame.math.Vector2(
            bot.x, bot.y
        ).distance_to((
            self.x,
            self.y,
        ))


class FoodRegistry:
    def __init__(self):
        self.food: List[Food] = []
        self.food_count = len(self.food)

    def add(self, food):
        self.food.append(food)
        self.food_count = len(self.food)
        return food

    def remove(self, food):
        self.food.remove(food)
        self.food_count = len(self.food)
        return food

    def check_eaten(self, bots: List[Bot]):
        for bot in bots:
            for food in self.food:
                if collision.is_colliding(bot, food):
                    self.food.remove(food)
                    bot.add_energy(const.FOOD_ENERGY)
                    self.check_eaten(bots)

    def get_nearest(self, bot, count=5):
        nearest = []
        for near in self.food:
            if len(nearest) == 0:
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

    def get_in_range(self, bot, distance: float=const.BOT_RANGE):
        in_range = []
        for sel in self.food:
            if sel == bot:
                continue
            mag = pygame.math.Vector2(bot.x, bot.y).distance_to((
                sel.x,
                sel.y,
            ))
            if mag < distance:
                in_range.append(sel)

        return in_range
