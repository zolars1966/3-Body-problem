"""

A simple Earth gravitation simulation. 
Sputnik moving around the planet 
(no effects to the planet applied).

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
l_press, r_press = False, False
DELTA_TIME = 1 / TICK_RATE
g = 9.81


def transform_coords(position):
    return [position[0] * 20 + H_WIDTH, H_HEIGHT - position[1] * 20]


def update_state(a, obj1, obj2):
    # acceleration
    a[0] = obj1.mass * obj2.pos[0] / -(obj2.pos[0] * obj2.pos[0] + obj2.pos[1] * obj2.pos[1])
    a[1] = obj1.mass * obj2.pos[1] / -(obj2.pos[0] * obj2.pos[0] + obj2.pos[1] * obj2.pos[1])
    
    # sputnik
    obj2.vel[0] += a[0] * DELTA_TIME
    obj2.vel[1] += a[1] * DELTA_TIME
    obj2.pos[0] += obj2.vel[0] * DELTA_TIME
    obj2.pos[1] += obj2.vel[1] * DELTA_TIME


if __name__ == "__main__":
    # creating a pygame window
    screen = pg.display.set_mode(SIZE, vsync=1)
    clock = pg.time.Clock()

    # creating the game logic / environment sample
    planet = Object(mass=27, vel=[0, 0])
    sputnik = Object(vel=[0, 5], pos=[15, 0])
    a = [planet.mass / -sputnik.pos[0], 0]

    col = (rand.randint(0, 255), rand.randint(0, 255), rand.randint(0, 255))
    old_coords = transform_coords([15, 0])

    upd_ticks = pg.time.get_ticks()
    screen.fill((200, 200, 200))
    pg.draw.circle(screen, (255, 100, 100), transform_coords([0, 0]), 25)

    # main cycle
    while True:
        # checking for keyboard, window, mouse inputs or events
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_c:
                    screen.fill((200, 200, 200))

                # restarting the simulation environment
                if event.key == pg.K_d or event.key == pg.K_r:
                    if event.key == pg.K_d:
                        DELTA_TIME = float(input("Write new time period: "))
                        TICK_RATE = 1 / DELTA_TIME

                    planet = Object(mass=3, vel=[0, 0])
                    sputnik = Object(vel=[0, 15], pos=[15, 0])
                    a = [0.2, 0]

                    old_coords = transform_coords([15, 0])
                    col = (rand.randint(0, 255), rand.randint(0, 255), rand.randint(0, 255))

        # game Assets/UI/elements drawing
        pg.draw.line(screen, col, old_coords, transform_coords(sputnik.pos), 5)
        old_coords = transform_coords(sputnik.pos)

        # game environment updating (with vertical synchronization)
        if 0 <= pg.time.get_ticks() - upd_ticks - (DELTA_TIME * 1000):
            upd_ticks = pg.time.get_ticks()

            # calling for game environment to update
            update_state(a, planet, sputnik)

        pg.display.set_caption("$~MIPH ~fps: " + str(round(clock.get_fps(), 2)) + " ~tickrate: " + str(TICK_RATE))

        pg.display.flip()
        clock.tick()
