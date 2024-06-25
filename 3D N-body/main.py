"""

A simple N-body system simulation (now in 3D). 
Some space objects are randomly generated
and interacting with each of the others.

(And yes, it's finally is multifile!)

Created by Arseny Zolotarev (Tuesday, 18 of July, 2023)

© 2019-2024 Zolars
  
"""


import pygame as pg
import sys
import time
from environment import *
from sengine import *
from globals import *


def get_projections(translated_vec):
    return ((translated_vec @ perspective_matrix + [0.0, 0.0, -1.0]) / translated_vec[:, :, 2, np.newaxis] + 1.0) * [H_WIDTH, H_HEIGHT, 1.]


def get_projection_x(translated_vec):
    return (translated_vec + [WIDTH / HEIGHT, 1.0, 1.0]) * H_HEIGHT


def cliping(translated_vecs, normals):
    to = np.sum(translated_vecs, axis=1) - camera_position * 3
    tol = np.linalg.norm(to, axis=1)

    return np.where((np.dot(to / tol[:, np.newaxis], camera_direction) > cos(FOV / 720 * HEIGHT / H_WIDTH * pi)) &
                    (tol >= 1) & (tol <= 21000) & (np.dot(normals, camera_direction) <= 0))[0]


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


def check_pressed():
    global camera_position, lightning_model

    keys = pg.key.get_pressed()

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
            camera_position += rotate_y(pi / 2, forwardvector * speed)
        elif keys[pg.K_d]:
            camera_position -= rotate_y(pi / 2, forwardvector * speed)

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


if __name__ == "__main__":
    # creating a pygame window
    screen = pg.display.set_mode(SIZE, pg.SCALED)
    mWIDTH, mHEIGHT = mSIZE = (min(SIZE) // 3, min(SIZE) // 3)
    mH_WIDTH, mH_HEIGHT = mH_SIZE = mWIDTH // 2, mHEIGHT // 2
    mPOS = mX, mY = WIDTH - mSIZE[0], HEIGHT - mSIZE[1]
    minimap, axissurf = pg.Surface(mSIZE), pg.Surface(mSIZE)
    minimap.set_alpha(90)
    cursor_free = False
    pg.mouse.set_visible(cursor_free)
    clock = pg.time.Clock()
    title = "$~ MIPH Paused. time: "

    # env = Environment(
    #             SpoilerTool(mass=Decimal(64000), pos=[dec(-180), dec(-50), dec(100)], rad=5, color=(255, 122, 0)),
    #             SpoilerTool(mass=Decimal(64000), pos=[dec(-20), dec(-50), dec(100)], rad=5, color=(100, 100, 255)),
    #             SpoilerTool(mass=Decimal(64000), pos=[dec(-60), dec(20), dec(100)], rad=5, color=(100, 255, 100)),
    #             SpoilerTool(mass=Decimal(64000), pos=[dec(-140), dec(0), dec(100)], rad=3, color=(255, 0, 100)),
    #                 )
    # env = Environment(SpoilerTool(mass=1000, pos=[0, 0, 0], color=(0, 255, 0)))
    # env = env3stable2

    for body in env.objects:
        body.rad = float(body.mass) / 400

    print(env)

    updtr = 0
    upd_ticks, vert_ticks, start_time, upd_time = pg.time.get_ticks(), pg.time.get_ticks(), pg.time.get_ticks(), time.perf_counter_ns()
    delta_ticks, delta_time = 1, 1
    speedup, slow_speedup, pause, enlarge_minimap, draw_traj = False, False, True, False, False

    fix_cam_dist_scale = 0.2

    mmr_scale, mmr_pos, mmr_scaled, minimappos = 1, [0, 0], False, np.asarray([0, 0])

    colors = np.asarray([1, 1, 1])
    # obj = np.asarray([[planet.pos, sputnik.pos, moon.pos]])
    tetrahedron, colors = open_model("obj/tetrahedron.mdl")
    cube, colors = open_model("obj/cube.obj")
    octahedron, colors = open_model("obj/octahedron.mdl")
    sphere, colors = open_model("obj/sphere.obj")
    axes, axes_colors = open_model("obj/OLC/axis.obj")

    cube /= 4
    tetrahedron = (tetrahedron - np.sum(tetrahedron, axis=1)[:, None] / 4) / 1.25

    for _ in range(2):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        pg.mouse.set_pos((H_WIDTH, H_HEIGHT))
        pg.mouse.set_visible(False)
        pg.display.flip()

    traj = [0] * env.n

    for i in range(env.n):
        env.objects[i].update_trajectory()
        traj[i] = env.objects[i].traj

    traj = np.asarray(traj)

    # main cycle
    while True:
        # game environment updating (with vertical synchronization)
        if (speedup or N_DELTA_TIME <= time.perf_counter_ns() - upd_time) and not pause:
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
            # checking for keyboard, window, mouse inputs or events
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
                        M_DELTA_TIME = (5, 0.25)[slow_speedup]
                        N_DELTA_TIME = M_DELTA_TIME * 1000000
                        DELTA_TIME = M_DELTA_TIME / 1000
                        # dt = Decimal(M_DELTA_TIME) / 1000

                    if event.key == pg.K_p:
                        start_time = pg.time.get_ticks()
                        pause ^= 1
                        title = "$~ MIPH Paused. time: " if pause else "$~ MIPH time: "

                    if event.key == pg.K_m:
                        enlarge_minimap ^= 1

                        mWIDTH, mHEIGHT = mSIZE = min(SIZE) // (3 - 2 * enlarge_minimap), min(SIZE) // (3 - 2 * enlarge_minimap)
                        mH_WIDTH, mH_HEIGHT = mH_SIZE = mWIDTH // 2, mHEIGHT // 2
                        mPOS = mX, mY = (WIDTH - mSIZE[0]) // (1 + enlarge_minimap), HEIGHT - mSIZE[1]
                        minimap, axissurf = pg.Surface(mSIZE), pg.Surface(mSIZE)
                        minimap.set_alpha(90)
            
                    if event.key == pg.K_l: draw_traj ^= 1

                    # if event.key == pg.K_SPACE:
                    #     play ^= 1
                    #     pause ^= 1
                    #     draw_traj ^= 1

                if event.type == pg.MOUSEWHEEL:
                    x, y = pg.mouse.get_pos()

                    if x >= mX and x <= mX + mWIDTH and y >= mY and y <= mY + mHEIGHT:
                        mmr_scale *= (100 - event.x - event.y) / 100
                        mmr_scaled = True

                    else:
                        fix_cam_dist_scale *= (100 - event.x - event.y) / 100

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

                            camera_position = rotate_y(fYaw, rotate_x(fXaw, [x, y, av_camera_pos[2] + z]))
                
                    # if right_click(event):
                    #     # do something
                    #     pass

            elapsed_ticks = pg.time.get_ticks() - vert_ticks
            vert_ticks = pg.time.get_ticks()

            if updtr >= 1:
                for i in range(env.n):
                    env.objects[i].update_trajectory()
                    traj[i] = env.objects[i].traj

                traj = np.asarray(traj)

            updtr = (updtr + 1) % 2


            def index(body):
                if body <= 3000: return sphere
                elif body <= 4500: return octahedron
                elif body <= 5750: return cube
                return tetrahedron


            # bodypos = np.asarray([body.fpos[:2] for body in env.objects])

            obj = np.concatenate([index(np.linalg.norm(camera_position - body.fpos)) * body.rad + body.fpos for body in env.objects])
            colors = np.concatenate([np.zeros(index(np.linalg.norm(camera_position - body.fpos)).shape[:2]) + body.color for body in env.objects])

            screen.fill((255, 255, 255))
            minimap.fill((0, 0, 0))
            axissurf.fill((40, 40, 40))            
            
            check_pressed()

            if pg.mouse.get_focused() and not cursor_free:
                differenceX = pg.mouse.get_pos()[0] - H_WIDTH
                differenceY = pg.mouse.get_pos()[1] - H_HEIGHT
                pg.mouse.set_pos(H_SIZE)
                fYaw -= differenceX / 32400 * W_SCALE * FOV
                fXaw -= differenceY / 32400 * W_SCALE * FOV
                fXaw = max(-pi / 2 + 0.001, min(pi / 2 - 0.001, fXaw))

            upvector = [0.0, 1.0, 0.0]
            camera_direction = rotate_y(fYaw, rotate_x(fXaw, [0.0, 0.0, 1.0]))
            # light = rotate_y(fYaw, rotate_x(fXaw, [0.57735027, 0.57735027, 0.57735027]))
            forwardvector[...] = [camera_direction[0], 0.0, camera_direction[2]]
            forwardvector /= np.linalg.norm(forwardvector)

            bodypos = matrix_multiply(np.asarray([body.fpos for body in env.objects]), quick_inverse([0, 0, 0], camera_direction, upvector))
            av_camera_pos = np.average(np.asarray([body.fpos for body in env.objects]), axis=0)
            mp_indexes = np.argsort(-bodypos[:, 2])
            bodypos = bodypos[:, :2]

            if not mmr_scaled:
                minimappos = np.average(bodypos, axis=0)
            bodypos -= minimappos + mmr_pos
            # bdm = bodypos.flat[np.abs(bodypos).argmax()]
            mScale = mH_WIDTH / (np.absolute(bodypos).max())
            
            if mmr_scale > mScale and mmr_scaled: mScale = mmr_scale
            else:
                mmr_scaled = False
                mmr_scale = mScale
                mmr_pos = [0, 0]

            bodypos *= mScale * 0.9
            bodypos = bodypos + mH_SIZE

            z = -mH_HEIGHT * fix_cam_dist_scale #* 4.5 / mmr_scale
            # camera_position = av_camera_pos + rotate_y(fYaw, rotate_x(fXaw, [0, 0, z]))

            camera_matrix = quick_inverse(camera_position, camera_direction, upvector)

            translated_vecs = obj
            normals = get_normals(translated_vecs)

            viewed = matrix_multiply(translated_vecs, camera_matrix)
            indexes = cliping(translated_vecs, normals)

            if draw_traj:
                viewed_traj = matrix_multiply(traj, camera_matrix)
                projection_traj = get_projections(viewed_traj)[:, :, :2].clip([-1, -1], SIZE)#.astype(int).tolist()

                for i in range(env.n):
                    pg.draw.lines(screen, env.objects[i].color, False, projection_traj[i], 2)

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

                        for i in indexes: pg.draw.polygon(screen, dps[i], projection_vecs[i, :, :2])
                    else:
                        dps = colors * dps[:, None]

                        for i in indexes: pg.draw.polygon(screen, dps[i], projection_vecs[i, :, :2])
                else: 
                    for polygon in projection_vecs: pg.draw.polygon(screen, "white", polygon[:, :2], 1)

            translated_vecs = rotate_x(fXaw, rotate_y(fYaw, axes)) - [0, 0, HEIGHT / (6 * (1 + 2 * enlarge_minimap))]
            normals = get_normals(translated_vecs)
            projection_vecs = get_projections(translated_vecs) - [mX / (2 - enlarge_minimap), mY / 2, 0]

            if lightning_model != "carcass":
                dps = wrap(normals)
                dps[dps > 1] = 1
                dps *= 255
                indexes = np.argsort(-projection_vecs[:, :, 2].max(axis=1))

                for i in indexes: pg.draw.polygon(axissurf, [dps[i]] * 3, projection_vecs[i, :, :2])
            else:
                for polygon in projection_vecs: pg.draw.polygon(axissurf, "white", polygon[:, :2], 1)

            for i in mp_indexes: pg.draw.circle(minimap, env.objects[i].color, bodypos[i], max(4, env.objects[i].rad * mScale))

            screen.blit(axissurf, mPOS)
            screen.blit(minimap, mPOS)

            # if play and not pause:
            #     li += 1

            # fYaw += pi / 180

            pg.display.set_caption(title + str(pg.time.get_ticks() - start_time) +\
             "~sim time: " + str(env.sim_time) + " ~fps: " + str(round(clock.get_fps(), 2)) + " ~sfps: " + str(round(1000000000 / delta_time, 2)))

            pg.display.flip()
            clock.tick()
