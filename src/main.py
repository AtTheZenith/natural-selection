import math
from typing import List
import pygame
import random

pygame.init()

window = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

pygame.display.set_caption("Natural Selection")

bot_img = pygame.image.load("./assets/images/bot.png")
bot_img_size = 40


class Bot:
    def __init__(self, x: float = 20, y: float = 20, size: float = 1, speed: float = 1):
        self.x = x
        self.y = y

        self.speed = speed * 150
        self.size = size
        self.move_direction: List[float] = [0, 0]

        self.image = bot_img.copy()
        self.image = pygame.transform.scale_by(self.image, size)
        self.rect = self.image.get_rect()

    def draw(self):
        window.blit(
            self.image,
            (
                self.x - bot_img_size / 2 * self.size,
                self.y - bot_img_size / 2 * self.size,
            ),
        )

    def get_rect(self):
        return self.rect

    def manual_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)

    def move(self, x, y):
        if x == 0 and y == 0:
            self.move_direction[0] = 0
            self.move_direction[1] = 0
            return

        mag = math.sqrt(x**2 + y**2)
        self.move_direction[0] = x / mag
        self.move_direction[1] = y / mag

    def update_pos(self, time=1 / 60):
        self.manual_pos(
            self.x + self.move_direction[0] * self.speed * time,
            self.y + self.move_direction[1] * self.speed * time,
        )


class BotRegistry:
    def __init__(self):
        self.bots = []
        self.bot_count = len(self.bots)

    def add(self, bot):
        self.bots.append(bot)
        self.bot_count = len(self.bots)
        return bot

    def remove(self, bot):
        self.bots.remove(bot)
        self.bot_count = len(self.bots)
        return bot

    def get_nearest(self, bot, count=math.inf):
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

    def get_in_range(self, bot, distance=math.inf):
        bots = []
        for near in self.bots:
            if near == bot:
                continue
            mag = pygame.math.Vector2(bot.x, bot.y).distance_to((
                near.x,
                near.y,
            ))
            if mag < distance:
                bots.append(near)

        return bots


br = BotRegistry()


def spawn_bots(count):
    pos = [(20, 20), (580, 20), (20, 380), (580, 380)]
    for _ in range(count):
        sel = random.choice(pos)
        br.add(Bot(sel[0], sel[1], random.randint(1, 3), speed=random.random() * 2 + 1))


spawn_bots(4)




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
        bot.draw()

    for _ in range(2):
        for bot in br.bots:
            nearby_bots = br.get_in_range(bot, 100)
            for other in nearby_bots:
                if bot != other and bot.rect.colliderect(other.rect):
                    handle_collision(bot, other)

    pygame.display.update()
    clock.tick(60)
