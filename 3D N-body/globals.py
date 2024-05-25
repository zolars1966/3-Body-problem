from math import *
from sengine import *
from decimal import Decimal
from pygame import time as pgtime
import numpy as np
import sys


# global references
lightning_model = phong
W_SCALE = 1
try:
    SIZE = WIDTH, HEIGHT = int(sys.argv[1]), int(sys.argv[2])
except IndexError:
    SIZE = WIDTH, HEIGHT = 1920 // W_SCALE, 1080 // W_SCALE
H_SIZE = H_WIDTH, H_HEIGHT = WIDTH / 2, HEIGHT / 2
l_press, r_press = False, False
l_press_el, r_press_el = pgtime.get_ticks(), pgtime.get_ticks()
shift_x, shift_y = 0, 0
M_DELTA_TIME = 5
N_DELTA_TIME = M_DELTA_TIME * 1000000
DELTA_TIME = M_DELTA_TIME / 1000
FPS = 60
FPS_DT = 1000 / FPS
coeff = 0.05
g = 9.81
dt = Decimal(M_DELTA_TIME) / 1000

FOV = 90

perspective_matrix = np.array([
        [(1.0 / tan(FOV / 720 * pi)), 0.0, 0.0],
        [0.0, (WIDTH / HEIGHT) * (1.0 / tan(FOV / 720 * pi)), 0.0],
        [0.0, 0.0, 1.0]
    ])
