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

br_1 = BotRegistry()
br_2 = BotRegistry()
pos = [(80, const.HEIGHT / 2), (const.WIDTH - 80, const.HEIGHT / 2)]
window = pygame.display.set_mode((const.WIDTH, const.HEIGHT))

br_1.add(
    Bot(
        window,
        pos[0][0],
        pos[0][1],
        team=1,
    )
)

br_2.add(Bot(window, pos[1][0], pos[1][1], team=2))

fr = FoodRegistry()
for _ in range(const.FOOD_START):
    x = random.random() * const.WIDTH
    y = random.random() * const.HEIGHT
    fr.add(Food(window, x, y))


time: float = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()

    delta = clock.tick(const.FRAME_RATE) / 1000

    window.fill((60, 60, 60))

    all_bots = br_1.bots + br_2.bots

    for bot in all_bots:
        this_br = br_1 if bot.team == 1 else br_2
        other_br = br_1 if bot.team == 2 else br_2
        target = other_br.get_in_range(bot, bot.true_range)
        target = [
            other for other in target if bot.size / other.size > const.MIN_SIZE_DIFF
        ]

        if len(target) > 0:
            target_x = target[0].x
            target_y = target[0].y
            bot.move(target_x - bot.x, target_y - bot.y)
        elif len(fr.get_in_range(bot, bot.true_range)) > 0:
            target = fr.get_nearest_food(bot=bot)
            target_x = target.x
            target_y = target.y
            bot.move(target_x - bot.x, target_y - bot.y)
        else:
            bot.move(0, 0)

        bot.update(delta)

    for _ in range(1):
        for bot in br_1.bots:
            for other in br_2.bots:
                if bot != other and collision.is_colliding(bot, other):
                    big = max(bot.size, other.size)
                    small = min(bot.size, other.size)
                    if (big / small) >= const.MIN_SIZE_DIFF:
                        match big:
                            case bot.size:
                                bot.add_energy(other.energy)
                                br_2.remove(other)
                            case other.size:
                                other.add_energy(bot.energy)
                                br_1.remove(bot)
                    else:
                        collision.handle(bot, other)

    time += delta
    if time > const.FOOD_COOLDOWN:
        x = random.random() * const.WIDTH
        y = random.random() * const.HEIGHT
        fr.add(Food(window, x, y))
        time -= const.FOOD_COOLDOWN

    fr.check_eaten(all_bots)
    br_1.energy_cycle()
    br_2.energy_cycle()
    br_1.reproduce_cycle()
    br_2.reproduce_cycle()

    for bot in all_bots:
        bot.draw()

    for food in fr.food:
        food.draw()

    pygame.display.update()
