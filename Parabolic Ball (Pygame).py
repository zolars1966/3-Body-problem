"""

A simple Earth gravitation simulation. 
Object takes off at an angle 45 degrees to the floor
and parabolically falls down with increasing speed.
(Without air resistance)

(And yes, it will be one-file)

Created and codded by Arseny Zolotarev (Tuesday, 18 of July, 2023)

© 2019-2023 Zolars
  
"""


import pygame as pg
import random as rand
import math
import sys


class Object:
    def __init__(self, pos=[0., 0.], vel=[1., 0.], mass=1.):
        self.pos = pos
        self.vel = vel
        self.mass = mass

# global references
try:
    SIZE = WIDTH, HEIGHT = int(sys.argv[1]), int(sys.argv[2])
except IndexError:
    SIZE = WIDTH, HEIGHT = 800, 800
H_SIZE = H_WIDTH, H_HEIGHT = WIDTH / 2, HEIGHT / 2
TICK_RATE = 120
DELTA_TIME = 1 / TICK_RATE
g = 9.81


def transform_coords(position):
    return [position[0] * 10 + H_WIDTH / 2, H_HEIGHT - position[1] * 10]


def update_state(a, obj):
    a = [0, -g]
    obj.vel[0] += a[0] * DELTA_TIME
    obj.vel[1] += a[1] * DELTA_TIME
    obj.pos[0] += obj.vel[0] * DELTA_TIME
    obj.pos[1] += obj.vel[1] * DELTA_TIME


if __name__ == "__main__":
    # creating a pygame window
    screen = pg.display.set_mode(SIZE, vsync=1)
    clock = pg.time.Clock()

    # creating the game logic / environment sample
    obj = Object(mass=2.25, vel=[7.071067, 7.071067])
    a = [0, -g]

    upd_ticks = pg.time.get_ticks()

    # main cycle
    while True:
        # surfaces cleaning
        screen.fill((200, 200, 200))
        
        # checking for keyboard, window, mouse inputs or events
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_u:
                    TICK_RATE -= 1
                    upd_ticks = pg.time.get_ticks()
                if event.key == pg.K_i:
                    TICK_RATE += 1
                    upd_ticks = pg.time.get_ticks()

        # game Assets/UI/elements drawing
        pg.draw.circle(screen, (255, 0, 0), transform_coords(obj.pos), 10)

        # game environment updating
        if 0 <= pg.time.get_ticks() - upd_ticks - (1000 / TICK_RATE):
            upd_ticks = pg.time.get_ticks()
            # calling for game environment to update
            update_state(a, obj)

        pg.display.set_caption("$~MIPH ~fps: " + str(round(clock.get_fps(), 2)) + " ~tickrate: " + str(TICK_RATE))

        pg.display.flip()
        clock.tick()
