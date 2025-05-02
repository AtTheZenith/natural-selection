import pygame
import random
from bot import Bot, BotRegistry
import collision
import const
from food import Food, FoodRegistry

pygame.init()

window = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

pygame.display.set_caption("Natural Selection")

br = BotRegistry()
pos = [(20, 20), (1900, 20), (20, 1060), (1900, 1060)]
for _ in range(8):
    sel = random.choice(pos)
    br.add(
        Bot(
            window,
            sel[0],
            sel[1],
            1 + random.random() * 3,
            speed=random.random() * 2 + 1,
        )
    )

fr = FoodRegistry()
for _ in range(30):
    x = 200 + random.random() * 1420
    y = 200 + random.random() * 680
    fr.add(Food(window, x, y))


iter = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()

    window.fill((50, 120, 240))

    mag_1 = pygame.math.Vector2(br.bots[0].x, br.bots[1].y).distance_to((960, 540))
    mag_2 = pygame.math.Vector2(br.bots[1].x, br.bots[0].y).distance_to((960, 540))

    sel = min(mag_1, mag_2)

    if sel == mag_1:
        sel_bot = br.bots[0]
    else:
        sel_bot = br.bots[1]

    for bot in br.bots:
        if bot == br.bots[0] or bot == br.bots[1]:
            bot.move(1920 / 2 - bot.x, 1080 / 2 - bot.y)
        else:
            bot.move(sel_bot.x - bot.x, sel_bot.y - bot.y)
        bot.update()

    for _ in range(3):
        for bot in br.bots:
            nearby_bots = br.get_in_range(bot, const.BOT_RANGE)
            for other in nearby_bots:
                if bot != other and collision.is_colliding(bot, other):
                    collision.handle(bot, other)

    fr.check_eaten(br.bots)

    iter += 1
    if iter == 4:
        x = 200 + random.random() * 1420
        y = 200 + random.random() * 680
        fr.add(Food(window, x, y))
        iter = random.randint(0, 3)

    br.check_energy()

    for bot in br.bots:
        bot.draw()

    for food in fr.food:
        food.draw()

    pygame.display.update()
    clock.tick(const.FRAME_RATE)
