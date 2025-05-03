import pygame

FRAME_RATE = 60

BOT_SPEED = 150
BOT_RANGE = 200
BOT_IMAGE = pygame.image.load("./assets/images/bot.png")
BOT_SIZE = 40

FOOD_IMAGE = pygame.image.load("./assets/images/food.png")
FOOD_SIZE = 30
FOOD_COOLDOWN = 1

MAX_ENERGY = 1000
FOOD_ENERGY = 400
BOT_ENERGY = 600
MIN_SIZE_DIFF = 1.2
