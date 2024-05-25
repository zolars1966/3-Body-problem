from math import *
import numpy as np


def matrix_multiply(inp_tri, matrix):    
    return inp_tri @ matrix[:3] + matrix[3]


def rotate_x(fTheta, triangle):
    rotate_x_matrix = np.array([
        [1.0, 0.0, 0.0],
        [0.0, cos(fTheta), sin(fTheta)],
        [0.0, -sin(fTheta), cos(fTheta)],
        [0.0, 0.0, 0.0]
    ])

    return matrix_multiply(triangle, rotate_x_matrix)


def rotate_z(fTheta, triangle):
    rotate_z_matrix = np.array([
        [cos(fTheta), sin(fTheta), 0.0],
        [-sin(fTheta), cos(fTheta), 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0]
    ])
    
    return matrix_multiply(triangle, rotate_z_matrix)


def rotate_y(fTheta, triangle):
    rotate_y_matrix = np.array([
        [cos(fTheta), 0.0, sin(fTheta)],
        [0.0, 1.0, 0.0],
        [-sin(fTheta), 0.0, cos(fTheta)],
        [0.0, 0.0, 0.0]
    ])

    return matrix_multiply(triangle, rotate_y_matrix)


def get_normals(translated_vec):
    point = translated_vec[:, 0]
    normal = np.cross(translated_vec[:, 1] - point, translated_vec[:, 2] - point)
    return normal / np.linalg.norm(normal, axis=1)[:, np.newaxis]


def quick_inverse(pos, direction, up):
    newUp = up - direction * np.sum(up @ direction)
    newUp /= np.linalg.norm(newUp)

    m = np.asarray([np.cross(newUp, direction), newUp, direction])

    qim = np.zeros([4, 3])
    qim[:3] = np.flipud(np.rot90(m))

    qim[3] = np.sum(-m * pos, axis=1)

    return qim


light = [0.57735027, 0.57735027, 0.57735027]
# camera_position = np.array([4.875, 0.0, 60.0])
camera_position = np.array([0., 0, -100.0])
camera_direction = np.asarray([-1.0, 1.0, 1.0])
camera_direction /= np.linalg.norm(camera_direction)
upvector = [0.0, 1.0, 0.0]
forwardvector = np.asarray(camera_direction)
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
