import pygame
from typing import List
from bot import Bot
import const


class Food:
    def __init__(self, window, x: float = 20, y: float = 20, energy: float = 10):
        self.window = window
        self.x = x
        self.y = y
        self.energy = energy

        self.image = const.FOOD_IMAGE.copy()
        self.rect = self.image.get_rect()

    def draw(self):
        self.window.blit(
            self.image,
            (
                self.x - const.FOOD_SIZE / 2,
                self.y - const.FOOD_SIZE / 2,
            ),
        )

    def get_rect(self):
        return self.rect

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)

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
                if food.is_colliding(bot):
                    print(food.x, food.y)
                    print(bot.x, bot.y)
                    print(bot)
                    self.food.remove(food)
