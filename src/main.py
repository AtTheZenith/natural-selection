import random
import pygame
from bot import Bot, BotRegistry
import collision
import const
from food import Food, FoodRegistry

pygame.init()

window = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Natural Selection")

br = BotRegistry()
pos = [(80, const.HEIGHT / 2), (const.WIDTH - 80, const.HEIGHT / 2)]
window = pygame.display.set_mode((const.WIDTH, const.HEIGHT))

for x in range(2):
    selected_pos = pos[x]
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
    x = random.random() * const.WIDTH
    y = random.random() * const.HEIGHT
    fr.add(Food(window, x, y))


time = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()

    delta = clock.tick(const.FRAME_RATE) / 1000

    window.fill((60, 60, 60))

    for bot in br.bots:
        target = br.get_in_range(bot, bot.true_range)
        target = [other for other in target if bot.size / other.size > const.MIN_SIZE_DIFF]
        
        num_1 = len(target)
        num_2 = len(fr.get_in_range(bot, bot.true_range))
        
        if num_1 > 0:
            target_x = target[0].x
            target_y = target[0].y
            bot.move(target_x - bot.x, target_y - bot.y)
        elif num_2 > 0:
            target = fr.get_nearest(bot, 1)
            target_x = target[0].x
            target_y = target[0].y
            bot.move(target_x - bot.x, target_y - bot.y)
        else:
            bot.move(0, 0)

        bot.update(delta)

    for _ in range(1):
        for bot in br.bots:
            nearby_bots = br.get_in_range(bot, int(bot.true_size * 1.5))
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

    time += delta
    if time > const.FOOD_COOLDOWN:
        x = random.random() * const.WIDTH
        y = random.random() * const.HEIGHT
        fr.add(Food(window, x, y))
        time -= const.FOOD_COOLDOWN

    fr.check_eaten(br.bots)
    br.energy_cycle()
    br.reproduce_cycle()

    for bot in br.bots:
        bot.draw()

    for food in fr.food:
        food.draw()

    pygame.display.update()
