# stolen from https://github.com/techwithtim/Pygame-Car-Racer/
# TODO: reimplement to avoid license issues

import pygame
import math

SCALE_FACTOR = 1.2


def scale_image(image):
    return pygame.transform.scale(image, (round(image.get_width() * SCALE_FACTOR),
                                          round(image.get_height() * SCALE_FACTOR)))


def scale_path(path: list) -> list:
    new_path = []
    for x, y in path:
        new_path.append((round(x * SCALE_FACTOR), round(y * SCALE_FACTOR)))
    return new_path


'''
def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)
'''


def blit_rotate_center(win, image, top_left, angle):
    # rotate the image by the given angle
    rotated_image = pygame.transform.rotate(image, angle)
    # get a rectangle object for the rotated image, centered at the top left point
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    # draw the rotated image onto the window
    win.blit(rotated_image, new_rect.topleft)
    # create a rectangle object to represent the position and size of the rotated image
    #rect = pygame.Rect(new_rect.left, new_rect.top, new_rect.width, new_rect.height)
    # draw the rectangle on the screen
    #pygame.draw.rect(win, (255, 0, 0), rect, 1)


BACKGROUND = scale_image(pygame.image.load("imgs_new/grass.jpeg"))
TRACK = scale_image(pygame.image.load("imgs_new/track.png"))
FINISH_LINE = scale_image(pygame.image.load("imgs_new/finish_line.png"))
FINISH_LINE_HITBOX = pygame.mask.from_surface(FINISH_LINE)

REDCAR = scale_image(pygame.image.load("imgs_new/red_car2.png"))
YELLOWCAR = scale_image(pygame.image.load("imgs_new/yellow_car.png"))

TRACKMASK = scale_image(pygame.image.load("imgs_new/track_mask2.png"))
TRACK_HITBOX = pygame.mask.from_surface(scale_image(pygame.image.load("imgs_new/track_mask2.png")))

WIDTH, HEIGHT = BACKGROUND.get_width(), BACKGROUND.get_height()

FPS = 60

PATH = scale_path(
    [(661, 25), (811, 25), (931, 25), (976, 41), (991, 80), (977, 113), (931, 127), (830, 115), (725, 111),
     (635, 101), (587, 115), (557, 144), (545, 180), (558, 218), (583, 249), (617, 286), (675, 340), (740, 391),
     (806, 444), (861, 498), (908, 560), (908, 636), (854, 682), (774, 697), (726, 700), (691, 715), (650, 731),
     (604, 736), (561, 730), (532, 713), (503, 677), (500, 635), (518, 591), (559, 564), (606, 584), (650, 605),
     (714, 621), (728, 583), (672, 545), (599, 503), (550, 448), (525, 378), (513, 325), (492, 280), (446, 240),
     (420, 185), (371, 161), (329, 172), (278, 227), (197, 274), (133, 270), (83, 247), (38, 207), (25, 150),
     (38, 90), (73, 45), (141, 30), (211, 25), (361, 25), (511, 25)])


class GameObject:
    def draw(self, win):
        blit_rotate_center(win, self.image, (self.pos_x, self.pos_y), math.degrees(-self.psi)+90)
