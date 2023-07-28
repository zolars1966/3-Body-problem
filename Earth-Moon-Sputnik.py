"""

A simple Earth gravitation simulation. 
Moon and Sputnik are moving around the Earth
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
shift_x, shift_y = 0, 0
DELTA_TIME = 0.005
TICK_RATE = 60
coeff = 0.001
g = 9.81


def transform_coords(position):
    return [int(position[0] * coeff) + H_WIDTH + shift_x * coeff, H_HEIGHT + shift_y * coeff - int(position[1] * coeff)]


def length(vec1, vec2):
    return math.sqrt((vec1[0] - vec2[0])*(vec1[0] - vec2[0]) + (vec1[1] - vec2[1])*(vec1[1] - vec2[1]))


def length_S(vec1, vec2):
    return (vec1[0] - vec2[0])*(vec1[0] - vec2[0]) + (vec1[1] - vec2[1])*(vec1[1] - vec2[1])


def update_state(obj1, obj2, obj3):
    # acceleration
    obj2.a[0] = obj1.mass * (obj1.pos[0] - obj2.pos[0]) / pow(length(obj1.pos, obj2.pos), 3)
    obj2.a[1] = obj1.mass * (obj1.pos[1] - obj2.pos[1]) / pow(length(obj1.pos, obj2.pos), 3)

    obj3.a[0] = obj1.mass * (obj1.pos[0] - obj3.pos[0]) / pow(length(obj1.pos, obj3.pos), 3)
    obj3.a[1] = obj1.mass * (obj1.pos[1] - obj3.pos[1]) / pow(length(obj1.pos, obj3.pos), 3)

    # sputnik
    obj2.vel[0] += obj2.a[0] * DELTA_TIME
    obj2.vel[1] += obj2.a[1] * DELTA_TIME
    obj2.pos[0] += obj2.vel[0] * DELTA_TIME
    obj2.pos[1] += obj2.vel[1] * DELTA_TIME

    # planet
    obj3.vel[0] += obj3.a[0] * DELTA_TIME
    obj3.vel[1] += obj3.a[1] * DELTA_TIME
    obj3.pos[0] += obj3.vel[0] * DELTA_TIME
    obj3.pos[1] += obj3.vel[1] * DELTA_TIME


if __name__ == "__main__":
    # creating a pygame window
    screen = pg.display.set_mode(SIZE)
    clock = pg.time.Clock()

    # creating the game logic / environment sample
    planet = Object(mass=5.9736*1e4*6.6743, vel=[0, 0], pos=[0, 0])
    sputnik = Object(mass=82.61, vel=[0, 8], pos=[6659, 0])
    moon = Object(mass=7.32*1e22, vel=[0, 1], pos=[392208, 0])

    upd_ticks = pg.time.get_ticks()
    vert_ticks = pg.time.get_ticks()
    speedup = False
    trajectory_s = [transform_coords(sputnik.pos), transform_coords(sputnik.pos)]
    trajectory_m = [transform_coords(moon.pos), transform_coords(moon.pos)]


    def clear_traj():
        trajectory_s.clear()
        trajectory_s.append(transform_coords(sputnik.pos))
        trajectory_s.append(transform_coords(sputnik.pos))

        trajectory_m.clear()
        trajectory_m.append(transform_coords(moon.pos))
        trajectory_m.append(transform_coords(moon.pos))


    # main cycle
    while True:
        screen.fill((0, 0, 0))

        # checking for keyboard, window, mouse inputs or events
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                clear_traj()

                if event.key == pg.K_r:
                    speedup = not speedup
        
        # game environment updating (with vertical synchronization)
        if speedup or 0 <= pg.time.get_ticks() - upd_ticks - (DELTA_TIME * 1000):
            upd_ticks = pg.time.get_ticks()

            # calling for game environment to update
            update_state(planet, sputnik, moon)

        # game Assets/UI/elements drawing
        if 0 <= pg.time.get_ticks() - vert_ticks - (1000 / TICK_RATE):
            vert_ticks = pg.time.get_ticks()

            if keys[pg.K_w]:
                shift_y += 10 / coeff
                clear_traj()
            if keys[pg.K_a]:
                shift_x += 10 / coeff
                clear_traj()
            if keys[pg.K_s]:
                shift_y -= 10 / coeff
                clear_traj()
            if keys[pg.K_d]:
                shift_x -= 10 / coeff
                clear_traj()

            if keys[pg.K_q]:
                coeff *= 0.95
                clear_traj()
            if keys[pg.K_e]:
                coeff *= 1.05
                clear_traj()

            tc_moon = transform_coords(moon.pos)
            tc_sputnik = transform_coords(sputnik.pos)
            if trajectory_m[-1] != tc_moon: trajectory_m.append(tc_moon)
            if trajectory_s[-1] != tc_sputnik: trajectory_s.append(tc_sputnik)

            pg.draw.circle(screen, (100, 150, 255), transform_coords(planet.pos), 6371 * coeff)
            pg.draw.circle(screen, (255, 100, 100), transform_coords(sputnik.pos), 4)
            pg.draw.circle(screen, (100, 100, 100), transform_coords(moon.pos), 1737 * coeff)
            pg.draw.lines(screen, (100, 255, 100), False, trajectory_m, 3)
            pg.draw.lines(screen, (100, 255, 100), False, trajectory_s, 3)

            pg.display.set_caption("$~ MIPH ~fps: " + str(round(clock.get_fps(), 2)))
            pg.display.flip()
            clock.tick()
