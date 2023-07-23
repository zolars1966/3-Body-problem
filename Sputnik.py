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
        self.a = [0, 0]


# global references
try:
    SIZE = WIDTH, HEIGHT = int(sys.argv[1]), int(sys.argv[2])
except IndexError:
    SIZE = WIDTH, HEIGHT = 800, 800
H_SIZE = H_WIDTH, H_HEIGHT = WIDTH / 2, HEIGHT / 2
l_press, r_press = False, False
DELTA_TIME = 0.01
g = 9.81


def transform_coords(position):
    return [position[0] * 20 + H_WIDTH, H_HEIGHT - position[1] * 20]


def length(vec1, vec2):
    return math.sqrt((vec1[0] - vec2[0])*(vec1[0] - vec2[0]) + (vec1[1] - vec2[1])*(vec1[1] - vec2[1]))


def length_S(vec1, vec2):
    return math.sqrt((vec1[0] - vec2[0])*(vec1[0] - vec2[0]) + (vec1[1] - vec2[1])*(vec1[1] - vec2[1]))


def update_state(obj1, obj2):
    # acceleration
    obj2.a[0] = obj1.mass * obj2.mass * obj2.pos[0] / -length_S(obj1.pos, obj2.pos)
    obj2.a[1] = obj1.mass * obj2.mass * obj2.pos[1] / -length_S(obj1.pos, obj2.pos)

    obj1.a[0] = obj1.mass * obj2.mass * obj1.pos[0] / -length_S(obj1.pos, obj2.pos)
    obj1.a[1] = obj1.mass * obj2.mass * obj1.pos[1] / -length_S(obj1.pos, obj2.pos)

    # sputnik
    obj2.vel[0] += obj2.a[0] * DELTA_TIME
    obj2.vel[1] += obj2.a[1] * DELTA_TIME
    obj2.pos[0] += obj2.vel[0] * DELTA_TIME
    obj2.pos[1] += obj2.vel[1] * DELTA_TIME

    # planet
    obj1.vel[0] += obj1.a[0] * DELTA_TIME
    obj1.vel[1] += obj1.a[1] * DELTA_TIME
    obj1.pos[0] += obj1.vel[0] * DELTA_TIME
    obj1.pos[1] += obj1.vel[1] * DELTA_TIME


if __name__ == "__main__":
    # creating a pygame window
    screen = pg.display.set_mode(SIZE, vsync=1)
    clock = pg.time.Clock()

    # creating the game logic / environment sample
    planet = Object(mass=5, vel=[0., -0.25], pos=[0, 0])
    sputnik = Object(mass=1, vel=[0, 6.75], pos=[10, 0])

    upd_ticks = pg.time.get_ticks()
    speedup = False
    trajectory_s = [transform_coords(sputnik.pos), transform_coords(sputnik.pos)]
    trajectory_p = [transform_coords(planet.pos), transform_coords(planet.pos)]

    # main cycle
    while True:
        screen.fill((200, 200, 200))

        # checking for keyboard, window, mouse inputs or events
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_c:
                    trajectory_s = [transform_coords(sputnik.pos), transform_coords(sputnik.pos)]
                    trajectory_p = [transform_coords(planet.pos), transform_coords(planet.pos)]

                if event.key == pg.K_s:
                    speedup = not speedup

                # restarting the simulation environment
                if event.key == pg.K_d or event.key == pg.K_r:
                    if event.key == pg.K_d:
                        DELTA_TIME = float(input("Write new time period: "))

                    planet = Object(mass=5, vel=[0., -0.25], pos=[0, 0])
                    sputnik = Object(mass=1, vel=[0, 6.75], pos=[10, 0])

                    trajectory_s = [transform_coords(sputnik.pos), transform_coords(sputnik.pos)]
                    trajectory_p = [transform_coords(planet.pos), transform_coords(planet.pos)]

        # game Assets/UI/elements drawing
        pg.draw.circle(screen, (255, 100, 100), transform_coords(planet.pos), 25)
        pg.draw.circle(screen, (255, 100, 100), transform_coords(sputnik.pos), 5)
        # trajectories
        pg.draw.lines(screen, (100, 255, 100), False, trajectory_p, 3)
        pg.draw.lines(screen, (100, 255, 100), False, trajectory_s, 3)

        # game environment updating (with vertical synchronization)
        if 0 <= pg.time.get_ticks() - upd_ticks - (DELTA_TIME * (speedup and 100 or 1000)):
            upd_ticks = pg.time.get_ticks()

            # calling for game environment to update
            update_state(planet, sputnik)
            trajectory_p.append(transform_coords(planet.pos))
            trajectory_s.append(transform_coords(sputnik.pos))

        pg.display.set_caption("$~MIPH ~fps: " + str(round(clock.get_fps(), 2)))

        pg.display.flip()
        clock.tick()
