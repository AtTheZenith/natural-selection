import pygame
from bot import Bot
from food import Food


def old_collide(entity_1: Bot | Food, entity_2: Bot | Food):
    return pygame.Rect.colliderect(entity_1.get_rect(), entity_2.get_rect())


def is_colliding(entity_1: Bot | Food, entity_2: Bot | Food):
    rect_1 = entity_1.get_rect()
    rect_2 = entity_2.get_rect()

    dx = entity_2.x - entity_1.x
    dy = entity_2.y - entity_1.y

    overlap_x = (rect_1.width + rect_2.width) / 2 - abs(dx)
    overlap_y = (rect_1.height + rect_2.height) / 2 - abs(dy)

    return overlap_x > 0 and overlap_y > 0


def handle(bot_1: Bot, bot_2: Bot):
    rect_1 = bot_1.get_rect()
    rect_2 = bot_2.get_rect()

    dx = bot_2.x - bot_1.x
    dy = bot_2.y - bot_1.y

    overlap_x = (rect_1.width + rect_2.width) / 2 - abs(dx)
    overlap_y = (rect_1.height + rect_2.height) / 2 - abs(dy)

    if overlap_x > 0 and overlap_y > 0:
        b1_vx = bot_1.move_direction[0] * bot_1.speed * bot_1.size
        b1_vy = bot_1.move_direction[1] * bot_1.speed * bot_1.size
        b2_vx = bot_2.move_direction[0] * bot_2.speed * bot_2.size
        b2_vy = bot_2.move_direction[1] * bot_2.speed * bot_2.size

        relative_vx = b2_vx - b1_vx
        relative_vy = b2_vy - b1_vy

        max_correction = 5
        correction_factor = 0.3

        if overlap_x < overlap_y:
            move_x = overlap_x * correction_factor

            if abs(relative_vx) > 0:
                move_x = max(-max_correction, min(move_x, max_correction))
                if relative_vx > 0:
                    bot_1.manual_pos(bot_1.x + move_x, bot_1.y)
                    bot_2.manual_pos(bot_2.x - move_x, bot_2.y)
                else:
                    bot_1.manual_pos(bot_1.x - move_x, bot_1.y)
                    bot_2.manual_pos(bot_2.x + move_x, bot_2.y)
            else:
                if abs(b1_vx) > abs(b2_vx):
                    bot_1.manual_pos(bot_1.x + move_x, bot_1.y)
                    bot_2.manual_pos(bot_2.x - move_x, bot_2.y)
                else:
                    bot_1.manual_pos(bot_1.x - move_x, bot_1.y)
                    bot_2.manual_pos(bot_2.x + move_x, bot_2.y)
        else:
            move_y = overlap_y * correction_factor
            if abs(relative_vy) > 0:
                move_y = max(-max_correction, min(move_y, max_correction))
                if relative_vy > 0:
                    bot_1.manual_pos(bot_1.x, bot_1.y + move_y)
                    bot_2.manual_pos(bot_2.x, bot_2.y - move_y)
                else:
                    bot_1.manual_pos(bot_1.x, bot_1.y - move_y)
                    bot_2.manual_pos(bot_2.x, bot_2.y + move_y)
            else:
                if abs(b1_vy) > abs(b2_vy):
                    bot_1.manual_pos(bot_1.x, bot_1.y + move_y)
                    bot_2.manual_pos(bot_2.x, bot_2.y - move_y)
                else:
                    bot_1.manual_pos(bot_1.x, bot_1.y - move_y)
                    bot_2.manual_pos(bot_2.x, bot_2.y + move_y)
