import random
import pygame
from bot import Bot, BotRegistry
import collision
import const
from food import Food, FoodRegistry

pygame.init()

window = pygame.display.set_mode((1920, 1020))
clock = pygame.time.Clock()

pygame.display.set_caption("Natural Selection")

br = BotRegistry()
pos = [(220, 220), (1700, 220), (220, 860), (1700, 860)]
for _ in range(2):
    selected_pos = random.choice(pos)
    br.add(
        Bot(
            window,
            selected_pos[0],
            selected_pos[1],
            size=1,
            speed=1,
        )
    )

fr = FoodRegistry()
for _ in range(const.FOOD_START):
    x = random.random() * 1920
    y = random.random() * 1080
    fr.add(Food(window, x, y))


iter = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()

    window.fill((60, 60, 60))

    for bot in br.bots:
        target = fr.get_nearest(bot, 1)
        if target[0]:
            target_x = target[0].x
            target_y = target[0].y
        else:
            target_x = 0
            target_y = 0

        bot.move(target_x - bot.x, target_y - bot.y)
        bot.update()

    for _ in range(3):
        for bot in br.bots:
            nearby_bots = br.get_in_range(bot, const.BOT_RANGE)
            for other in nearby_bots:
                if bot != other and collision.is_colliding(bot, other):
                    big = max(bot.size, other.size)
                    small = min(bot.size, other.size)
                    if (big / small) >= const.MIN_SIZE_DIFF:
                        match big:
                            case bot.size:
                                bot.add_energy(other.energy)
                                br.remove(other)
                            case other.size:
                                other.add_energy(bot.energy)
                                br.remove(bot)
                    else:
                        collision.handle(bot, other)

    iter += 1
    if iter == const.FOOD_COOLDOWN * const.FRAME_RATE:
        x = random.random() * 1920
        y = random.random() * 1080
        fr.add(Food(window, x, y))
        iter = 0

    fr.check_eaten(br.bots)
    br.energy_cycle()
    br.reproduce_cycle()
    

    for bot in br.bots:
        bot.draw()

    for food in fr.food:
        food.draw()

    pygame.display.update()
    clock.tick(const.FRAME_RATE)
