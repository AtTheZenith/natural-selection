import pygame

FRAME_RATE = 0
WIDTH = 1920
HEIGHT = 1020

BOT_IMAGES = [
    pygame.image.load("./assets/bot.png"),
    pygame.image.load("./assets/bot_1.png"),
    pygame.image.load("./assets/bot_2.png"),
]
BOT_SIZE = 20
BOT_SPEED = 120
BOT_RANGE = 90
BOT_MIN_SIZE = 0.5
BOT_MAX_SIZE = 3
BOT_MIN_SPEED = 0.5
BOT_MAX_SPEED = 4
BOT_MIN_RANGE = 0.5
BOT_MAX_RANGE = 5

FOOD_IMAGE = pygame.image.load("./assets/food.png")
FOOD_SIZE = 10
FOOD_START = 200
FOOD_COOLDOWN = 0.03

MAX_ENERGY = 800
FOOD_ENERGY = 200
BOT_ENERGY = 300
REPRODUCTION_COST = 320
REPRODUCTION_MINIMUM = 750
MIN_SIZE_DIFF = 1.07
