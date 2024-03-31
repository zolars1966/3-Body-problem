"""

A simple 16-body system simulation (now in 3D). 
Some space objects are randomly generated
and interacting with each of the others.

(And yes, it will be one-file)

Created by Arseny Zolotarev (Tuesday, 18 of July, 2023)

© 2019-2024 Zolars
  
"""


import pygame as pg
import numpy as np
import random as rand
import sys
import time
from math import *
from decimal import Decimal


def sort_triangles(triangle1):
    return -sum(triangle1[0][:, 2])


def sort_triangles_c(triangle1):
    return -max(triangle1[:, 2])


def matrix_multiply(inp_tri, matrix):    
    return inp_tri @ matrix[:3, :3] + matrix[3, :3]


def rotate_x(fTheta, triangle):
    rotate_x_matrix = np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, cos(fTheta), sin(fTheta), 0.0],
        [0.0, -sin(fTheta), cos(fTheta), 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])

    return matrix_multiply(triangle, rotate_x_matrix)


def rotate_z(fTheta, triangle):
    rotate_z_matrix = np.array([
        [cos(fTheta), sin(fTheta), 0.0, 0.0],
        [-sin(fTheta), cos(fTheta), 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])
    
    return matrix_multiply(triangle, rotate_z_matrix)


def rotate_y(fTheta, triangle):
    rotate_y_matrix = np.array([
        [cos(fTheta), 0.0, sin(fTheta), 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [-sin(fTheta), 0.0, cos(fTheta), 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])

    return matrix_multiply(triangle, rotate_y_matrix)


def get_normals(translated_vec):
    point = translated_vec[:, 0]
    normal = np.cross(translated_vec[:, 1] - point, translated_vec[:, 2] - point)
    return normal / np.linalg.norm(normal, axis=1)[:, np.newaxis]


def point_at(pos, direction, up):
    newUp = up - direction * np.sum(up @ direction)
    newUp /= np.linalg.norm(newUp)

    atm = np.zeros((4, 4))
    atm[:, :3] = [np.cross(newUp, direction), newUp, direction, pos]
    atm[3, 3] = 1

    return atm


def quick_inverse(m):
    qim = np.zeros([4, 4])
    qim[:3, :3] = np.flipud(np.rot90(m[:3, :3]))

    qim[3, :3] = np.sum(-np.flipud(np.rot90(qim[:3, :3])) * m[3, :3], axis=1)
    qim[3, 3] = 1

    return qim


light = np.asarray([0.57735027, 0.57735027, 0.57735027])
# camera_position = np.array([4.875, 0.0, 60.0])
camera_position = np.array([0, 0, -500.0])
camera_direction = np.array([0.0, 0.0, 1.0])
upvector = np.array([0.0, 1.0, 0.0])
forwardvector = camera_direction * 0.1
fYaw = 0
fXaw = 0


def light_diff(normal, factor=0):
    diff = -((normal @ light) - factor) / (1.0 + factor)
    diff[diff < 0] = 0
    return diff


def light_reflect(normal):
    return -(camera_direction - (normal * 2 * (normal @ camera_direction)[:, np.newaxis]))


def highlight(normal, degree=1):
    I = light_reflect(normal) @ light
    I[I < 0] = 0
    return np.power(I, degree)


def blinn_highlight(normal, degree=1):
    h = light + camera_direction
    h /= np.linalg.norm(h)
    I = -(normal @ h)
    I[I < 0] = 0
    return np.power(I, degree)


light_ambient = 0.25


def lambert(normal):
    return light_diff(normal) * 0.75 + light_ambient


def wrap(normal):
    return light_diff(normal, 0.75)


def phong(normal):
    return light_diff(normal) * 0.5 + highlight(normal, 30) + light_ambient


def blinn(normal):
    return light_diff(normal) * 0.5 + blinn_highlight(normal, 30) + light_ambient


def metal(normal):
    return blinn_highlight(normal, 5) + light_ambient


lightning_model = phong


class Object:
    def __init__(self, pos=[0, 0, 0], vel=[1, 0, 0], mass=1., rad=1, color=(255, 255, 255), acl=[0, 0, 0]):
        self.pos = list(map(Decimal, pos))
        self.fpos = list(map(float, self.pos))
        self.vel = list(map(Decimal, vel))
        self.mass = Decimal(mass)
        self.a = [Decimal(0), Decimal(0), Decimal(0)]
        self.rad = rad
        self.color = color

    def __str__(self):
        return "Object(pos=" + str(self.pos) + ", vel=" + str(self.vel) + ", mass=" + str(self.mass) + ", rad=" + str(self.rad) + ", color=" + str(self.color) + ", acl=" + str(self.a) + ")"

    def update(self, dt):
        self.vel[0] += (self.a[0] * dt) / 1000
        self.vel[1] += (self.a[1] * dt) / 1000
        self.vel[2] += (self.a[2] * dt) / 1000

        self.pos[0] += (self.vel[0] * dt) / 1000
        self.pos[1] += (self.vel[1] * dt) / 1000
        self.pos[2] += (self.vel[2] * dt) / 1000

        self.a = [Decimal(0), Decimal(0), Decimal(0)]

        self.fpos = list(map(float, self.pos))


# global references
W_SCALE = 1
try:
    SIZE = WIDTH, HEIGHT = int(sys.argv[1]), int(sys.argv[2])
except IndexError:
    SIZE = WIDTH, HEIGHT = 2560 // W_SCALE, 1440 // W_SCALE
H_SIZE = H_WIDTH, H_HEIGHT = WIDTH / 2, HEIGHT / 2
l_press, r_press = False, False
l_press_el, r_press_el = pg.time.get_ticks(), pg.time.get_ticks()
shift_x, shift_y = 0, 0
M_DELTA_TIME = 1000 / 60
DELTA_TIME = M_DELTA_TIME / 1000
FPS = 60
FPS_DT = 1000 / FPS
coeff = 0.05
g = 9.81

FOV = 90

perspective_matrix = np.array([
        [(1.0 / tan(FOV / 720 * pi)), 0.0, 0.0],
        [0.0, (WIDTH / HEIGHT) * (1.0 / tan(FOV / 720 * pi)), 0.0],
        [0.0, 0.0, 1.0]
    ])


def get_projections(translated_vec):
    return ((translated_vec @ perspective_matrix + [0.0, 0.0, -1.0]) / translated_vec[:, :, 2, np.newaxis] + 1.0) * [H_WIDTH, H_HEIGHT, 1.]


def get_projection_x(translated_vec):
    return (translated_vec + [WIDTH / HEIGHT, 1.0, 1.0]) * H_HEIGHT


def cliping(translated_vecs, normals):
    to = np.sum(translated_vecs, axis=1) - camera_position * 3
    tol = np.linalg.norm(to, axis=1)

    return np.where((np.dot(to / tol[:, np.newaxis], camera_direction) > cos(FOV / 720 * HEIGHT / H_WIDTH * pi)) &
                    (tol >= 1) & (tol <= 20000) & (np.dot(normals, camera_direction) <= 0))[0]


def length(vec1, vec2):
    return Decimal.sqrt((vec1[0] - vec2[0]) * (vec1[0] - vec2[0]) + 
                        (vec1[1] - vec2[1]) * (vec1[1] - vec2[1]) + 
                        (vec1[2] - vec2[2]) * (vec1[2] - vec2[2]))


class Environment:
    def __init__(self, *objects):
        self.objects = objects
        self.objects_count = self.n = self.number = self.num = len(self.objects)

    def __str__(self):
        s = "Environment(\n"

        for obj in self.objects:
            s = s + str(obj) + ",\n"

        return s + ")\n"

    def add(self, object):
        self.objects.append(object)
        self.objects_count += 1

    def update(self):
        for i in range(self.objects_count):
            for j in range(i + 1, self.objects_count):
                l = length(self.objects[i].pos, self.objects[j].pos)**3

                d = [(self.objects[i].pos[0] - self.objects[j].pos[0]), 
                     (self.objects[i].pos[1] - self.objects[j].pos[1]),
                     (self.objects[i].pos[2] - self.objects[j].pos[2])]

                # acceleration
                self.objects[i].a[0] += self.objects[j].mass * -d[0] / l
                self.objects[i].a[1] += self.objects[j].mass * -d[1] / l
                self.objects[i].a[2] += self.objects[j].mass * -d[2] / l

                self.objects[j].a[0] += self.objects[i].mass * d[0] / l
                self.objects[j].a[1] += self.objects[i].mass * d[1] / l
                self.objects[j].a[2] += self.objects[i].mass * d[2] / l

            self.objects[i].update(Decimal(5))


def left_click(event):
    global l_press, l_press_el
    
    if event.type == pg.MOUSEBUTTONDOWN:
        if event.button == 1:
            l_press = True
    
    elif event.type == pg.MOUSEBUTTONUP and l_press:
        if event.button == 1:
            l_press = False
            l_press_dt = pg.time.get_ticks() - l_press_el
            l_press_el = pg.time.get_ticks()
            out = l_press_dt <= 200
            return out
    
    l_press_el = pg.time.get_ticks()
    
    return False


def right_click(event):
    global r_press, r_press_el
    
    if event.type == pg.MOUSEBUTTONDOWN:
        if event.button == 3:
            r_press = True
    
    elif event.type == pg.MOUSEBUTTONUP and r_press:
        if event.button == 3:
            r_press = False
            r_press_dt = pg.time.get_ticks() - r_press_el
            r_press_el = pg.time.get_ticks()
            out = r_press_dt <= 200
            return out
    
    r_press_el = pg.time.get_ticks()
    
    return False


def open_model(file):
    tx_model, vertex, faces, colors, colorsi = open(file, "r"), [], [], [], []

    if file.split(".")[-1] == "obj":
        for line in tx_model:
            if line.startswith("v "):
                vertex.append([float(point) for point in line.split()[1:]] + [1])
            elif line.startswith("f "):
                faces_ = line.split()[1:]
                faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
            elif line.startswith("c "):
                colors.append(list(map(int, line[2:].split(" ")[1].split("/"))))
                colorsi.append(int(line[2:].split(" ")[0]))
    elif file.split(".")[-1] == "mdl":
        for line in tx_model:
            if line.startswith("p "):
                vertex.append([float(point) for point in line.split()[1:]] + [1])
            elif line.startswith("f ") or line.startswith("ff "):
                faces_ = line.split()[1]
                faces.append([int(face_) for face_ in faces_.split("/")])
            elif line.startswith("c "):
                colors.append(list(map(int, line[2:].split(" ")[1].split("/"))))
                colorsi.append(int(line[2:].split(" ")[0]))

    mdl, obj = [vertex, faces], []

    for i in range(len(mdl[1])):
        for j in range(len(mdl[1][i])):
            line = []
            for element in mdl[1][i]:
                line.append(np.array([float(mdl[0][element][0]), float(mdl[0][element][1]), float(mdl[0][element][2])], dtype=np.float64))
            obj.append(np.array(line))

    color = [None for i in range(len(obj))]
    
    for i, j in enumerate(colorsi):
        color[j] = colors[i]

    if len(colorsi) != 0:
        for i in range(0, max(colorsi) + 1):
            if i not in colorsi:
                color[i] = [1, 1, 1]
    else:
        for i in range(0, len(obj)):
            color[i] = [1, 1, 1]

    return np.asarray(obj), np.asarray(color)


if __name__ == "__main__":
    # creating a pygame window
    screen = pg.display.set_mode(SIZE, pg.SCALED)
    # mWIDTH, mHEIGHT = mSIZE = (min(SIZE) // 3, min(SIZE) // 3)
    mWIDTH, mHEIGHT = mSIZE = (min(SIZE) // 3, min(SIZE) // 3)
    mH_WIDTH, mH_HEIGHT = mH_SIZE = mWIDTH // 2, mHEIGHT // 2
    mPOS = mX, mY = WIDTH - mSIZE[0], HEIGHT - mSIZE[1]
    minimap = pg.Surface(mSIZE)
    cursor_free = False
    pg.mouse.set_visible(cursor_free)
    clock = pg.time.Clock()
    mtx, mty = 0, 0
    title = "$~ MIPH Paused. time: "


    def dec(n):
        z = 1

        while n != int(n):
            z *= 10
            n *= 10

        return Decimal(int(n)) / z


    # creating the game logic / environment sample
    env = Environment(
                Object(pos=[Decimal('-33.3'), Decimal('-12.5'), Decimal('-74.2')], vel=[Decimal('3.771453977868634'), Decimal('0.8664209658798098'), Decimal('-2.2190536102057404')], mass=3923, rad=9.8075, color=(173, 112, 141), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
                Object(pos=[Decimal('59.4'), Decimal('-68.6'), Decimal('-47.9')], vel=[Decimal('1.507607190926868'), Decimal('0.6354575350990272'), Decimal('2.753377682987071')], mass=3742, rad=9.355, color=(83, 162, 162), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
                Object(pos=[Decimal('44.8'), Decimal('17.5'), Decimal('20.4')], vel=[Decimal('-2.885198536485182'), Decimal('-0.2554423015247326'), Decimal('2.0810116549327564')], mass=533, rad=1.3325, color=(246, 17, 185), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
                Object(pos=[Decimal('85.8'), Decimal('-64.9'), Decimal('15.2')], vel=[Decimal('-1.0360955444243116'), Decimal('1.1147698367029228'), Decimal('-2.941000510766889')], mass=875, rad=2.1875, color=(114, 160, 100), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
                Object(pos=[Decimal('-29.1'), Decimal('-29.3'), Decimal('-99.5')], vel=[Decimal('-0.8107635747044631'), Decimal('4.161754146417981'), Decimal('0.1302179543934221')], mass=4265, rad=10.6625, color=(243, 218, 98), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
                Object(pos=[Decimal('5.2'), Decimal('-22.7'), Decimal('49.1')], vel=[Decimal('-2.1964531499509888'), Decimal('-0.96647750165637'), Decimal('0.33542630965336256')], mass=1942, rad=4.855, color=(0, 191, 184), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
                Object(pos=[Decimal('-8.4'), Decimal('55.1'), Decimal('72.1')], vel=[Decimal('-3.003655245630295'), Decimal('-3.4566349215641476'), Decimal('-4.2972879710872424')], mass=2012, rad=5.03, color=(232, 42, 143), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
                Object(pos=[Decimal('-84.7'), Decimal('-42.6'), Decimal('-95.2')], vel=[Decimal('-2.0518070063922624'), Decimal('4.6862157812406'), Decimal('1.3459528714003488')], mass=2711, rad=6.7775, color=(56, 155, 55), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
                Object(pos=[Decimal('-66.9'), Decimal('2.9'), Decimal('-1')], vel=[Decimal('-0.763764465973007'), Decimal('3.8865858618429424'), Decimal('1.8649638151175484')], mass=2999, rad=7.4975, color=(163, 237, 6), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
                Object(pos=[Decimal('-2.2'), Decimal('-78.3'), Decimal('-76.3')], vel=[Decimal('-2.091663667841348'), Decimal('-2.2458151402064704'), Decimal('-1.5862961230628422')], mass=4997, rad=12.4925, color=(71, 163, 23), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
                Object(pos=[Decimal('71.1'), Decimal('27.6'), Decimal('-83.6')], vel=[Decimal('3.107687114467957'), Decimal('-2.0230607473842544'), Decimal('-3.381248975439456')], mass=1896, rad=4.74, color=(221, 62, 213), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
                Object(pos=[Decimal('-4.2'), Decimal('0.9'), Decimal('60.7')], vel=[Decimal('0.9987880436627262'), Decimal('1.2326779868511896'), Decimal('-2.2738387930237')], mass=4631, rad=11.5775, color=(120, 192, 14), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
                Object(pos=[Decimal('27.3'), Decimal('54.4'), Decimal('65.8')], vel=[Decimal('0.3030065883894394'), Decimal('-3.735274048342836'), Decimal('-1.5317262756905244')], mass=801, rad=2.0025, color=(39, 210, 246), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
                Object(pos=[Decimal('-73.1'), Decimal('-15.2'), Decimal('61.9')], vel=[Decimal('-3.456507726511911'), Decimal('-4.958673988193928'), Decimal('3.2403461478732756')], mass=2919, rad=7.2975, color=(12, 240, 144), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
                Object(pos=[Decimal('-23.4'), Decimal('-5.9'), Decimal('33.6')], vel=[Decimal('-4.355568434642154'), Decimal('0.5431340973433043'), Decimal('0.05305653047606106')], mass=2283, rad=5.7075, color=(224, 225, 232), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
                Object(pos=[Decimal('-63.5'), Decimal('-27.6'), Decimal('-43.4')], vel=[Decimal('1.264601227865459'), Decimal('-4.22460731683138'), Decimal('2.3942717516074476')], mass=4758, rad=11.895, color=(250, 131, 95), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
                      )
  
    for i in range(len(env.objects)):
       env.objects[i].rad = int(env.objects[i].mass) / 400

    print(env)

    upd_ticks = pg.time.get_ticks()
    vert_ticks = pg.time.get_ticks()
    start_time = pg.time.get_ticks()
    upd_time = time.perf_counter_ns()
    delta_ticks = 1
    delta_time = 1
    speedup = False
    slow_speedup = False
    pause = True
    enlarge_minimap = False

    mmr_scale = 1
    mmr_pos = [0, 0]
    mmr_scaled = False
    minimappos = np.asarray([0, 0])

    colors = np.asarray([1, 1, 1])
    # obj = np.asarray([[planet.pos, sputnik.pos, moon.pos]])
    tetrahedron, colors = open_model("/Users/zolars/Documents/Projects/miph/obj/tetrahedron.mdl")
    cube, colors = open_model("/Users/zolars/Documents/Projects/miph/obj/cube.obj")
    octahedron, colors = open_model("/Users/zolars/Documents/Projects/miph/obj/octahedron.mdl")
    sphere, colors = open_model("/Users/zolars/Documents/Projects/miph/obj/sphere.obj")

    cube /= 4
    tetrahedron = (tetrahedron - np.sum(tetrahedron, axis=1)[:, None] / 4) / 1.25

    for _ in range(2):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        pg.mouse.set_pos((H_WIDTH, H_HEIGHT))
        pg.display.flip()

    # main cycle
    while True:
        # checking for keyboard, window, mouse inputs or events
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.mouse.set_pos(H_SIZE)
                    cursor_free ^= 1
                    pg.mouse.set_visible(cursor_free)

                if event.key == pg.K_r:
                    speedup ^= 1
                    FPS = [60, 10][speedup]
                    FPS_DT = 1000 / FPS
                
                if event.key == pg.K_o:
                    slow_speedup ^= 1
                    M_DELTA_TIME = (100 / 6, 0)[slow_speedup]

                if event.key == pg.K_p:
                    start_time = pg.time.get_ticks()
                    pause ^= 1
                    title = "$~ MIPH Paused. time: " if pause else "$~ MIPH time: "

                if event.key == pg.K_m:
                    enlarge_minimap ^= 1

                    mWIDTH, mHEIGHT = mSIZE = min(SIZE) // (3 - 2 * enlarge_minimap), min(SIZE) // (3 - 2 * enlarge_minimap)
                    mH_WIDTH, mH_HEIGHT = mH_SIZE = mWIDTH // 2, mHEIGHT // 2
                    mPOS = mX, mY = (WIDTH - mSIZE[0]) // (1 + enlarge_minimap), HEIGHT - mSIZE[1]
                    minimap = pg.Surface(mSIZE)
        
            if event.type == pg.MOUSEWHEEL and cursor_free:
                x, y = pg.mouse.get_pos()

                if x >= mX and x <= mX + mWIDTH and y >= mY and y <= mY + mHEIGHT:
                    mmr_scale *= (100 - event.x - event.y) / 100
                    mmr_scaled = True

            if event.type == pg.MOUSEMOTION and cursor_free:
                x, y = pg.mouse.get_pos()

                if x >= mX and x <= mX + mWIDTH and y >= mY and y <= mY + mHEIGHT and pg.mouse.get_pressed()[0] and mmr_scaled:
                    mmr_pos[0] -= event.rel[0] / 0.9 / mmr_scale
                    mmr_pos[1] -= event.rel[1] / 0.9 / mmr_scale

                    mood_cam = rotate_y(pi / 2, camera_direction)
                    x = minimappos[0] + mmr_pos[0]
                    y = minimappos[1] + mmr_pos[1]
                    z = -mH_HEIGHT * 4.5 / mmr_scale

                    camera_position = rotate_y(fYaw, rotate_x(fXaw, [x, y, z]))

            if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
                if left_click(event) and cursor_free:
                    x, y = pg.mouse.get_pos()

                    if x >= mX and x <= mX + mWIDTH and y >= mY and y <= mY + mHEIGHT:
                        mood_cam = rotate_y(pi / 2, camera_direction)
                        x = (x - mX - mH_WIDTH) / 0.9 / mmr_scale + minimappos[0] + mmr_pos[0]
                        y = (y - mY - mH_HEIGHT) / 0.9 / mmr_scale + minimappos[1] + mmr_pos[1]
                        z = -mH_HEIGHT * 4.5 / mmr_scale

                        camera_position = rotate_y(fYaw, rotate_x(fXaw, [x, y, z]))
            
                if event.type == pg.MOUSEBUTTONDOWN:
                    mtx, mty = (x - mX - mH_WIDTH) / 0.9 / mmr_scale, (y - mY - mH_HEIGHT) / 0.9 / mmr_scale

                # if right_click(event):
                #     # do something
                #     pass

        # game environment updating (with vertical synchronization)
        if (speedup or M_DELTA_TIME <= pg.time.get_ticks() - upd_ticks) and not pause:
            delta_time = -upd_time
            upd_time = time.perf_counter_ns()
            delta_time += upd_time

            delta_ticks = -upd_ticks
            upd_ticks = pg.time.get_ticks()
            delta_ticks += upd_ticks

            # calling for game environment to update
            env.update()

        # game Assets/UI/elements drawing
        if FPS_DT <= pg.time.get_ticks() - vert_ticks:
            elapsed_ticks = pg.time.get_ticks() - vert_ticks
            vert_ticks = pg.time.get_ticks()


            def index(body):
                if body <= 3000:
                    return sphere
                elif body <= 4500:
                    return octahedron
                elif body <= 5750:
                    return cube

                return tetrahedron

          
            obj = np.concatenate([index(np.linalg.norm(camera_position - body.fpos)) * body.rad + body.fpos for body in env.objects])
            colors = np.concatenate([np.zeros(index(np.linalg.norm(camera_position - body.fpos)).shape[:2]) + body.color for body in env.objects])

            screen.fill((12, 12, 12))
            minimap.fill((15, 20, 30))
            
            if True in keys:
                speed = 2 * elapsed_ticks / 10

                if keys[pg.K_LSHIFT]:
                    speed = 10 * elapsed_ticks / 10
                if keys[pg.K_LCTRL]:
                    speed = 5 * elapsed_ticks / 100

                if keys[pg.K_w]:
                    camera_position += forwardvector * speed
                elif keys[pg.K_s]:
                    camera_position -= forwardvector * speed

                speed /= 2

                if keys[pg.K_e]:
                    camera_position[1] -= speed
                elif keys[pg.K_q]:
                    camera_position[1] += speed

                if keys[pg.K_a]:
                    camera_position[0] -= forwardvector[2] * speed
                    camera_position[1] += forwardvector[1] * speed
                    camera_position[2] += forwardvector[0] * speed
                elif keys[pg.K_d]:
                    camera_position[0] += forwardvector[2] * speed
                    camera_position[1] -= forwardvector[1] * speed
                    camera_position[2] -= forwardvector[0] * speed

                if keys[pg.K_0]:
                    lightning_model = "carcass"
                elif keys[pg.K_1]:
                    lightning_model = light_diff
                elif keys[pg.K_2]:
                    lightning_model = lambert
                elif keys[pg.K_3]:
                    lightning_model = wrap
                elif keys[pg.K_4]:
                    lightning_model = phong
                elif keys[pg.K_5]:
                    lightning_model = blinn
                elif keys[pg.K_6]:
                    lightning_model = highlight
                elif keys[pg.K_7]:
                    lightning_model = blinn_highlight
                elif keys[pg.K_8]:
                    lightning_model = metal
                elif keys[pg.K_9]:
                    lightning_model = light_reflect

            if pg.mouse.get_focused() and not cursor_free:
                differenceX = pg.mouse.get_pos()[0] - H_WIDTH
                differenceY = pg.mouse.get_pos()[1] - H_HEIGHT
                pg.mouse.set_pos((H_WIDTH, H_HEIGHT))
                fYaw -= differenceX / 32400 * W_SCALE * FOV
                fXaw -= differenceY / 32400 * W_SCALE * FOV
                fXaw = max(-pi / 2 + 0.001, min(pi / 2 - 0.001, fXaw))

                upvector[...] = [0.0, 1.0, 0.0]
                camera_direction = rotate_y(fYaw, rotate_x(fXaw, [0.0, 0.0, 1.0]))
                # light = rotate_y(fYaw, rotate_x(fXaw, [0.57735027, 0.57735027, 0.57735027]))
                forwardvector[...] = [camera_direction[0], 0.0, camera_direction[2]]
                forwardvector /= np.linalg.norm(forwardvector)

            camera_matrix = quick_inverse(point_at(camera_position, camera_direction, upvector))

            bodypos = matrix_multiply(np.asarray([body.fpos for body in env.objects]), quick_inverse(point_at([0, 0, 0], camera_direction, upvector)))
            mp_indexes = np.argsort(-bodypos[:, 2])
            bodypos = bodypos[:, :2]

            if not mmr_scaled:
                minimappos = np.average(bodypos, axis=0)
            bodypos -= minimappos + mmr_pos
            # bdm = bodypos.flat[np.abs(bodypos).argmax()]
            mScale = mH_WIDTH / np.absolute(bodypos).max()
            
            if mmr_scale > mScale and mmr_scaled:
                mScale = mmr_scale
            else:
                mmr_scaled = False
                mmr_scale = mScale
                mmr_pos = [0, 0]

            bodypos *= mScale * 0.9
            bodypos = bodypos + mH_SIZE

            translated_vecs = obj
            normals = get_normals(translated_vecs)

            viewed = matrix_multiply(translated_vecs, camera_matrix)
            indexes = cliping(translated_vecs, normals)

            if len(indexes) != 0:
                viewed = viewed[indexes]
                colors = colors[indexes]

                normals = normals[indexes]
                projection_vecs = get_projections(viewed)

                if lightning_model != "carcass":
                    dps = lightning_model(normals)
                    dps[dps > 1] = 1

                    indexes = np.argsort(-projection_vecs[:, :, 2].max(axis=1))

                    if lightning_model == light_reflect:
                        dps[dps < 0] = 0
                        dps *= 255

                        for i in indexes:
                            pg.draw.polygon(screen, dps[i], projection_vecs[i, :, :2])
                    else:
                        dps = colors * dps[:, None]

                        for i in indexes:
                            pg.draw.polygon(screen, dps[i], projection_vecs[i, :, :2])
                else:
                    for polygon in projection_vecs:
                        pg.draw.polygon(screen, "black", polygon[:, :2], 1)

            for i in mp_indexes:
                pg.draw.circle(minimap, env.objects[i].color, bodypos[i], max(4, env.objects[i].rad * mScale))

            screen.blit(minimap, mPOS)

            pg.display.set_caption(title + str(pg.time.get_ticks() - start_time) + " ~fps: " + str(round(clock.get_fps(), 2)) + " ~sfps: " + str(round(1000000000 / delta_time, 2)))

            pg.display.flip()
        
            clock.tick()
