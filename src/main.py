import pygame
import random
from bot import Bot, BotRegistry
import const
from food import Food, FoodRegistry

pygame.init()

window = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

pygame.display.set_caption("Natural Selection")


def handle_collision(bot1, bot2):
    rect1 = bot1.rect
    rect2 = bot2.rect

    dx = rect1.centerx - rect2.centerx
    dy = rect1.centery - rect2.centery

    overlap_x = (rect1.width + rect2.width) / 2 - abs(dx)
    overlap_y = (rect1.height + rect2.height) / 2 - abs(dy)

    if overlap_x > 0 and overlap_y > 0:
        b1_vx = bot1.move_direction[0] * bot1.speed
        b1_vy = bot1.move_direction[1] * bot1.speed
        b2_vx = bot2.move_direction[0] * bot2.speed
        b2_vy = bot2.move_direction[1] * bot2.speed

        relative_vx = b2_vx - b1_vx
        relative_vy = b2_vy - b1_vy

        max_correction = 10
        correction_factor = 0.2

        if overlap_x < overlap_y:
            move_x = overlap_x * correction_factor

            if abs(relative_vx) > 0:
                move_x = max(-max_correction, min(move_x, max_correction))
                if relative_vx > 0:
                    bot1.manual_pos(bot1.x + move_x, bot1.y)
                    bot2.manual_pos(bot2.x - move_x, bot2.y)
                else:
                    bot1.manual_pos(bot1.x - move_x, bot1.y)
                    bot2.manual_pos(bot2.x + move_x, bot2.y)
            else:
                if abs(b1_vx) > abs(b2_vx):
                    bot1.manual_pos(bot1.x + move_x, bot1.y)
                    bot2.manual_pos(bot2.x - move_x, bot2.y)
                else:
                    bot1.manual_pos(bot1.x - move_x, bot1.y)
                    bot2.manual_pos(bot2.x + move_x, bot2.y)
        else:
            move_y = overlap_y * correction_factor
            if abs(relative_vy) > 0:
                move_y = max(-max_correction, min(move_y, max_correction))
                if relative_vy > 0:
                    bot1.manual_pos(bot1.x, bot1.y + move_y)
                    bot2.manual_pos(bot2.x, bot2.y - move_y)
                else:
                    bot1.manual_pos(bot1.x, bot1.y - move_y)
                    bot2.manual_pos(bot2.x, bot2.y + move_y)
            else:
                if abs(b1_vy) > abs(b2_vy):
                    bot1.manual_pos(bot1.x, bot1.y + move_y)
                    bot2.manual_pos(bot2.x, bot2.y - move_y)
                else:
                    bot1.manual_pos(bot1.x, bot1.y - move_y)
                    bot2.manual_pos(bot2.x, bot2.y + move_y)


br = BotRegistry()

pos = [(20, 20), (1900, 20), (20, 1060), (1900, 1060)]
for _ in range(3):
    sel = random.choice(pos)
    br.add(
        Bot(window, sel[0], sel[1], random.randint(1, 3), speed=random.random() * 2 + 1)
    )

fr = FoodRegistry()

for _ in range(1):
    fr.add(Food(window, 960, 540))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()

    window.fill((50, 120, 240))

    for bot in br.bots:
        if bot == br.bots[0]:
            bot.move(1920 / 2 - bot.x, 1080 / 2 - bot.y)
        else:
            bot.move(br.bots[0].x - bot.x, br.bots[0].y - bot.y)
        bot.update_pos()

    for _ in range(2):
        for bot in br.bots:
            nearby_bots = br.get_in_range(bot, const.BOT_RANGE)
            for other in nearby_bots:
                if bot != other and bot.rect.colliderect(other.rect):
                    handle_collision(bot, other)

    fr.check_eaten(br.bots)

    for bot in br.bots:
        bot.draw()

    for food in fr.food:
        food.draw()

    pygame.display.update()
    clock.tick(60)
