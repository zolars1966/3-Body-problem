# 3D Graphics and N-Body Simulation Engine

This repository contains a Python-based 3D graphics and N-body simulation engine. It renders and simulates various space objects interacting with each other using an N-body simulation approach, alongside interactive 3D graphics capabilities.

## Features

- **Matrix Operations**: Efficiently handles 3D transformations using matrix multiplication.
- **Rotation Functions**: Provides functions for rotating objects around the X, Y, and Z axes.
- **Lighting Models**: Implements different lighting models such as Lambertian, Phong, Blinn-Phong, and custom reflection models.
- **Input Handling**: Includes mouse and keyboard input handling for camera movement and control settings.
- **3D Model Loading**: Supports loading and rendering of 3D models from OBJ and MDL files.
- **Interactive Visualization**: Utilizes Pygame for real-time interactive 3D rendering and visualization.
- **N-Body Simulation**: Simulates gravitational interactions between space objects, displaying their trajectories and interactions.

## Installation

Clone the repository:

```bash
git clone https://github.com/your_username/your_repo.git
cd your_repo
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Ensure that Python 3.x and Pygame are installed on your system.

## Usage

To run the simulation and visualization engine:

```bash
python main.py
```

### Controls

- **W / S**: Move forward / backward.
- **A / D**: Rotate left / right.
- **Q / E**: Move up / down.
- **Left Click**: Toggle actions based on mouse position.
- **Right Click**: Reserved for future functionality.
- **R**: Toggle speed-up mode.
- **O**: Toggle slow-speed mode.
- **P**: Pause simulation.
- **M**: Toggle minimap size.
- **L**: Toggle display of trajectories.
- **0-9**: Switch between different lighting models.

## Algorithms

The N-body problem refers to a classic problem in physics and computational science where the goal is to predict the motion of a group of celestial objects interacting with each other gravitationally or through other forces. Here are explanations of a few algorithms commonly used to solve the N-body problem:

### 1. **Direct Summation Method (Brute Force)**

The direct summation method, also known as the brute force method, calculates the force on each particle due to every other particle directly. Here's how it works:

- **Force Calculation**: For each particle \( i \), calculate the force exerted by all other particles \( j \):
  \[
  \mathbf{F}_{ij} = G \frac{m_i m_j (\mathbf{r}_j - \mathbf{r}_i)}{|\mathbf{r}_j - \mathbf{r}_i|^3}
  \]
  where \( G \) is the gravitational constant, \( m_i, m_j \) are masses of particles \( i \) and \( j \), \( \mathbf{r}_i, \mathbf{r}_j \) are their positions.

- **Integration**: Update positions and velocities of each particle based on forces calculated.

- **Complexity**: \( O(N^2) \), where \( N \) is the number of particles. It scales quadratically with the number of particles, making it inefficient for large \( N \).

### 2. **Tree Methods (Barnes-Hut Algorithm)**

Tree methods like the Barnes-Hut algorithm are more efficient than the brute force method for large \( N \). They exploit the spatial distribution of particles to reduce the number of force calculations needed.

- **Quadtree/Octree Construction**: Particles are organized into a hierarchical tree structure (quadtree for 2D, octree for 3D) based on their positions.

- **Tree Traversal**: For each particle, traverse the tree to calculate forces from distant particles efficiently.

- **Force Approximation**: Instead of calculating forces from every particle, approximate forces using center-of-mass properties of distant clusters of particles.

- **Complexity**: Typically \( O(N \log N) \) for well-separated systems, reducing to \( O(N^2) \) in dense systems. This makes it scalable for large \( N \).

### 3. **Particle Mesh Ewald (PME) Method**

PME is particularly suited for simulating periodic systems with long-range interactions, such as molecular dynamics simulations:

- **Grid-based Interpolation**: Positions and charges of particles are mapped onto a grid using interpolation methods.

- **Fast Fourier Transform (FFT)**: Fourier transforms are used to efficiently calculate long-range forces in reciprocal space.

- **Direct Space Calculation**: Short-range interactions are calculated directly.

- **Combination of Spaces**: Forces are combined from reciprocal and direct space calculations to get the total force on each particle.

- **Complexity**: \( O(N \log N) \) due to FFT operations, but also depends on grid resolution and system size.

### 4. **Verlet Integration Methods**

Verlet methods are numerical integrators used to update positions and velocities of particles in time-dependent simulations:

- **Leapfrog Integration**: Positions and velocities are updated alternately in half-steps, which ensures energy conservation in Hamiltonian systems.

- **Symplectic Integrators**: These integrators preserve phase space volume, making them ideal for long-term simulations.

- **Integration Steps**: Time integration involves updating positions and velocities using current forces and velocities respectively.

- **Complexity**: Each time step is \( O(N) \), making it efficient for simulations over long periods.

### 5. **Montgomery Sphere**
The Montgomery Sphere method is a numerical integration technique specifically designed to solve the N-body problem, particularly focusing on systems where the forces between particles are dominated by gravitational interactions. It offers several advantages over traditional integration methods like the Verlet method or direct summation, especially in terms of numerical stability and conservation properties. Here’s an explanation of how the Montgomery Sphere method works specifically for the 3-body problem:

#### Overview of Montgomery Sphere Method

The Montgomery Sphere method introduces an auxiliary sphere in a higher-dimensional space to embed the dynamics of the N-body system. This embedding helps to handle the conservation laws more effectively and mitigate issues related to close encounters between particles in the system.

#### Steps Involved in the Montgomery Sphere Method:

1. **Higher-Dimensional Embedding**:
   - Represent each particle \( i \) in an \( (N+1) \)-dimensional space, where \( N \) is the number of bodies (particles). The positions and velocities of each particle are extended to this higher-dimensional space.

2. **Sphere Construction**:
   - Define a hypersphere in this \( (N+1) \)-dimensional space that encapsulates the dynamics of the system. This sphere serves as an auxiliary construct that simplifies the interaction between particles.

3. **Hamiltonian Formulation**:
   - The dynamics of the particles are described by a Hamiltonian function in the extended phase space. The Hamiltonian typically includes kinetic and potential energy terms for each particle in the system.

4. **Integration Scheme**:
   - Apply a symplectic integrator to evolve the system over time. Symplectic integrators preserve phase space volume and exhibit long-term stability, which is crucial for accurately simulating the gravitational interactions over extended periods.

5. **Projection**:
   - Periodically project the positions and velocities of particles back onto the original physical \( N \)-dimensional space. This step ensures that the results remain interpretable in terms of the original physical problem (e.g., three-dimensional space for the 3-body problem).

#### Advantages of Montgomery Sphere Method:

- **Conservation Laws**: The method effectively preserves conservation laws (such as conservation of energy and angular momentum) due to its symplectic nature.
  
- **Long-Term Stability**: Unlike some traditional methods, Montgomery Sphere maintains numerical stability over long integration times, crucial for simulating celestial mechanics accurately.

- **Handling Close Encounters**: By embedding particles in a higher-dimensional sphere, the method mitigates issues related to close encounters and gravitational singularities, which can cause numerical instability in traditional methods.

#### Implementation Considerations:

- **Choice of Parameters**: Parameters such as the radius of the sphere and the symplectic integrator used can impact the accuracy and efficiency of the method.
  
- **Accuracy vs. Efficiency Trade-off**: Adjustments may be necessary to balance computational efficiency with the desired level of accuracy, particularly for large \( N \).

### Application to the 3-Body Problem:

For the specific case of the 3-body problem, the Montgomery Sphere method offers a robust framework to simulate the gravitational interactions between three particles (e.g., stars, planets) over time. It ensures that the system evolves according to the laws of celestial mechanics while maintaining numerical stability and conservation properties inherent in the method.

In summary, the Montgomery Sphere method extends the traditional phase space of an N-body system into a higher-dimensional sphere, leveraging symplectic integration techniques to accurately model gravitational interactions. This approach is particularly effective for the 3-body problem, ensuring both stability and accuracy in long-term simulations of celestial dynamics.

### Conclusion

Each algorithm has its strengths depending on the specific characteristics of the N-body system being simulated. The choice of algorithm often balances between accuracy, computational efficiency, and scalability with increasing number of particles \( N \). Advanced simulations often employ a combination of these techniques to handle different aspects of the N-body problem effectively.

## Code Explanation

### Import Statements and Class Definitions

```python
import random as rand
from body import *
from globals import *
```

**Class `Environment`**

```python
class Environment:
    def __init__(self, *objects, dt=Decimal("0.005")):
        self.objects = objects
        self.objects_count = self.n = self.number = self.num = len(self.objects)
        self.sim_time = 0
        self.dt = dt

        for body in self.objects:
            body.dt = self.dt
```

**Explanation:**

The `Environment` class manages multiple instances of celestial bodies (defined in `body.py`) and their interactions in a simulated environment.

### String Representation and Utility Methods

```python
    def __str__(self):
        s = "Environment(\n"

        for obj in self.objects:
            s = s + str(obj) + ",\n"

        return s + ")\n"

    @staticmethod
    def length(x, y, z):
        return Decimal.sqrt(x * x + y * y + z * z)
```

**Explanation:**

- **`__str__` Method**: Provides a string representation of the `Environment` class instance, listing all objects within it.
- **`length` Static Method**: Calculates the Euclidean length of a vector (x, y, z) using the `Decimal` module for precision.

### Object Management Methods

```python
    def add(self, object):
        self.objects.append(object)
        self.objects_count += 1

    def update(self):
        self.sim_time += self.dt

        for i in range(self.objects_count):
            for j in range(i + 1, self.objects_count):
                d1, d2, d3 = (self.objects[i].posx - self.objects[j].posx), \
                             (self.objects[i].posy - self.objects[j].posy), \
                             (self.objects[i].posz - self.objects[j].posz)

                l = self.length(d1, d2, d3) ** 3

                d1 /= l
                d2 /= l
                d3 /= l

                # acceleration
                self.objects[i].a1 -= self.objects[j].mass * d1
                self.objects[i].a2 -= self.objects[j].mass * d2
                self.objects[i].a3 -= self.objects[j].mass * d3

                self.objects[j].a1 += self.objects[i].mass * d1
                self.objects[j].a2 += self.objects[i].mass * d2
                self.objects[j].a3 += self.objects[i].mass * d3

            self.objects[i].update()
```

**Explanation:**

- **`add` Method**: Adds a new object to `self.objects` and increments `self.objects_count`.
- **`update` Method**: Advances the simulation time by `self.dt` and computes gravitational interactions between objects using Newton's law.

### Class `Object` and `SpoilerTool`

```python
from decimal import Decimal

class Object:
    def __init__(self, pos=[0, 0, 0], vel=[1, 0, 0], mass=1., rad=1, color=(255, 255, 255), dt=Decimal("0.005"), acl=[0, 0, 0], fps=60):
        self.posx, self.posy, self.posz = list(map(Decimal, pos))
        self.fpos = list(map(float, pos))
        self.velx, self.vely, self.velz = list(map(Decimal, vel))
        self.mass = Decimal(mass)
        self.a1, self.a2, self.a3 = Decimal(0), Decimal(0), Decimal(0)
        self.rad = rad
        self.color = color
        self.traj = [list(map(float, pos))] * 500
        self.dt = dt

    def __str__(self):
        return "Object(pos=" + str((self.posx, self.posy, self.posz)) + ", vel=" + str((self.velx, self.vely, self.velz)) + ", mass=" + str(self.mass) + ", rad=" + str(self.rad) + ", color=" + str(self.color) + ", acl=" + str((self.a1, self.a2, self.a3)) + ")"

    def update(self):
        self.velx += self.a1 * self.dt
        self.vely += self.a2 * self.dt
        self.velz += self.a3 * self.dt

        self.posx += self.velx * self.dt
        self.posy += self.vely * self.dt
        self.posz += self.velz * self.dt

        self.a1, self.a2, self.a3 = Decimal(0), Decimal(0), Decimal(0)

        self.fpos = float(self.posx), float(self.posy), float(self.posz)

    def update_trajectory(self):
        self.traj = self.traj[1:] + [self.fpos]


class SpoilerTool(Object):
    def update(self):
        self.a1, self.a2, self.a3 = Decimal(0), Decimal(0), Decimal(0)
        self.fpos = float(self.posx), float(self.posy), float(self.posz)

    # def update_trajectory(self):
    #     pass
```

**Explanation:**

- **`Object` Class**: Represents a celestial body with attributes such as position (`posx, posy, posz`), velocity (`velx, vely, velz`), mass (`mass`), radius (`rad`), color (`color`), acceleration (`a1, a2, a3`), and time step (`dt`). It includes methods for updating the object's position and velocity (`update`) and maintaining a trajectory history (`update_trajectory`).
  
- **`SpoilerTool` Class**: Inherits from `Object` and overrides the `update` method to reset acceleration (`a1, a2, a3`) and update the floating-point position (`fpos`) without updating the trajectory.

### Conclusion

The repository combines advanced 3D graphics rendering with an N-body simulation engine to simulate gravitational interactions among celestial bodies. It provides a flexible framework for exploring various scenarios in celestial mechanics and dynamics.

Sure, let's split the code into several logical blocks and explain each one:

### Initialization and Setup

```python
import pygame as pg
import sys
import time
from environment import *
from sengine import *
from globals import *

# Define some utility functions
def get_projections(translated_vec):
    # Function details omitted for brevity
    pass

def get_projection_x(translated_vec):
    # Function details omitted for brevity
    pass

def cliping(translated_vecs, normals):
    # Function details omitted for brevity
    pass

def left_click(event):
    # Function details omitted for brevity
    pass

def right_click(event):
    # Function details omitted for brevity
    pass

def check_pressed():
    # Function details omitted for brevity
    pass

if __name__ == "__main__":
    # Initialize Pygame window
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
```

**Explanation:**
- Imports necessary libraries and modules.
- Defines utility functions related to graphics and input handling.
- Initializes Pygame and sets up the game window (`screen`) with specific dimensions.
- Initializes surfaces (`minimap`, `axissurf`) and other graphical elements.
- Sets initial configurations for mouse visibility, clock, and window title.

### Environment Setup and Object Initialization

```python
# Object initialization (environment setup)
env = Environment(
    SpoilerTool(mass=Decimal(64000), pos=[dec(-180), dec(-50), dec(100)], rad=5, color=(255, 122, 0)),
    SpoilerTool(mass=Decimal(64000), pos=[dec(-20), dec(-50), dec(100)], rad=5, color=(100, 100, 255)),
    SpoilerTool(mass=Decimal(64000), pos=[dec(-60), dec(20), dec(100)], rad=5, color=(100, 255, 100)),
    SpoilerTool(mass=Decimal(64000), pos=[dec(-140), dec(0), dec(100)], rad=3, color=(255, 0, 100)),
)

# Optional: Modify object properties if needed
for body in env.objects:
    body.rad = float(body.mass) / 400

print(env)

# Other initializations
updtr = 0
upd_ticks, vert_ticks, start_time, upd_time = pg.time.get_ticks(), pg.time.get_ticks(), pg.time.get_ticks(), time.perf_counter_ns()
delta_ticks, delta_time = 1, 1
speedup, slow_speedup, pause, enlarge_minimap, draw_traj = False, False, True, False, False
fix_cam_dist_scale = 0.2
mmr_scale, mmr_pos, mmr_scaled, minimappos = 1, [0, 0], False, np.asarray([0, 0])
colors = np.asarray([1, 1, 1])
tetrahedron, colors = open_model("/Users/zolars/Documents/Projects/miph/obj/samples/platons/tetrahedron.mdl")
cube, colors = open_model("/Users/zolars/Documents/Projects/miph/obj/cube.obj")
octahedron, colors = open_model("/Users/zolars/Documents/Projects/miph/obj/samples/platons/octahedron.mdl")
sphere, colors = open_model("/Users/zolars/Documents/Projects/miph/obj/sphere.obj")
axes, axes_colors = open_model("/Users/zolars/Documents/Projects/miph/obj/OLC/axis.obj")

# Optional: Modify loaded models or data
cube /= 4
tetrahedron = (tetrahedron - np.sum(tetrahedron, axis=1)[:, None] / 4) / 1.25
```

**Explanation:**
- Sets up the initial simulation environment (`env`) with specific objects (`SpoilerTool` instances).
- Modifies properties of each object (e.g., radius) based on its mass.
- Initializes various flags (`speedup`, `slow_speedup`, etc.) and variables (`fix_cam_dist_scale`, `mmr_scale`, etc.) for control and configuration.
- Loads and optionally modifies various models (`tetrahedron`, `cube`, etc.) from file paths.

### Main Game Loop

```python
# Main game loop
while True:
    if (speedup or N_DELTA_TIME <= time.perf_counter_ns() - upd_time) and not pause:
        # Update game environment
        # Details omitted for brevity
        env.update()

    if FPS_DT <= pg.time.get_ticks() - vert_ticks:
        # Handle input events (keyboard, mouse, etc.)
        # Details omitted for brevity

        # Update camera and other dynamic elements
        # Details omitted for brevity

        # Draw objects and UI elements
        # Details omitted for brevity

        # Update screen and handle FPS
        # Details omitted for brevity
```

**Explanation:**
- **Game Environment Update:** Updates the simulation environment (`env`) based on the game's logic and timing (`speedup`, `pause`).
- **Input Event Handling:** Monitors and reacts to user inputs such as keyboard presses and mouse movements.
- **Camera and Dynamic Element Updates:** Adjusts the camera position and updates other dynamic elements based on user interaction.
- **Drawing and UI Elements:** Renders objects (`obj`, `axes`) and UI elements (`minimap`, `axissurf`) on the screen using Pygame's drawing functions.
- **Screen Update and FPS Control:** Updates the Pygame display (`screen`) and manages the frame rate (`clock.tick()`).

### Conclusion

Each block of the code serves a specific purpose:
- **Initialization:** Sets up necessary libraries, environment, and objects.
- **Main Loop:** Handles game logic, user input, updates, and rendering.

Sure, let's split and explain the provided Python code into logical blocks:

### Imports and Matrix Operations

```python
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
```

**Explanation:**
- **Imports**: Imports the `math` module for trigonometric functions and `numpy` for numerical operations.
- **Functions**:
  - `matrix_multiply(inp_tri, matrix)`: Performs matrix multiplication where `inp_tri` is a set of input vectors and `matrix` is a transformation matrix.
  - `rotate_x(fTheta, triangle)`: Rotates the triangle around the x-axis by `fTheta` radians.
  - `rotate_z(fTheta, triangle)`: Rotates the triangle around the z-axis by `fTheta` radians.
  - `rotate_y(fTheta, triangle)`: Rotates the triangle around the y-axis by `fTheta` radians.

### Normal Vectors and Inverse Matrix Calculation

```python
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
```

**Explanation:**
- **Functions**:
  - `get_normals(translated_vec)`: Computes normalized normal vectors for a set of translated vectors.
  - `quick_inverse(pos, direction, up)`: Calculates a quick inverse matrix based on position (`pos`), viewing direction (`direction`), and up vector (`up`). This is used for camera transformations.

### Lighting Models and Camera Setup

```python
light = [0.57735027, 0.57735027, 0.57735027]
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
```

**Explanation:**
- **Global Variables**:
  - `light`: Direction vector for the light source.
  - `camera_position`, `camera_direction`, `upvector`, `forwardvector`, `fYaw`, `fXaw`: Variables related to camera position and orientation.
- **Lighting Functions**:
  - Various lighting models (`light_diff`, `light_reflect`, `highlight`, `blinn_highlight`, `lambert`, `wrap`, `phong`, `blinn`, `metal`) compute illumination effects based on surface normals and light sources.

### Model Loading and Processing

```python
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
```

**Explanation:**
- **Function `open_model(file)`**:
  - Reads and processes a 3D model file (`obj` or `mdl`).
  - Parses vertices (`vertex`), faces (`faces`), and colors (`colors`).
  - Constructs the model (`obj`) from vertices and faces.
  - Assigns colors to model components based on file format.
  - Returns the constructed 3D model (`obj`) and associated colors (`color`).


## Images

* N-body 3D
![Minimap](https://github.com/zolars1966/3-Body-problem/assets/70763346/d976ee8d-3f11-4d18-a5eb-ca8bf0d73f2d)
![Minimap](https://github.com/zolars1966/3-Body-problem/assets/70763346/53e1fe72-3d6d-4d06-88c4-1cf019eb2cdf)
![N-body](https://github.com/zolars1966/3-Body-problem/assets/70763346/b53e3277-1c9f-430c-b9de-449e49da49af)
![N-body](https://github.com/zolars1966/3-Body-problem/assets/70763346/4e39476d-e45f-4db9-9892-0071fa2e99d8)

* 3-body 2d (unsolvable)
![3-body](https://github.com/zolars1966/3-Body-problem/assets/70763346/b22bee4e-0870-47ff-bd47-aef828e18fb6)

* Ball trajectories (with diffirent delta-time parameter)
![Parabolic ball (python)](https://github.com/zolars1966/3-Body-problem/assets/70763346/f34ab4b2-8e15-46e9-8adb-96087a3dc3dd)
![Parabolic ball (c++)](https://github.com/zolars1966/3-Body-problem/assets/70763346/a179780a-d583-4dde-8f23-bc51fede9e17)

* Sputnik trajectories
![Earth mass equals 729](https://github.com/zolars1966/3-Body-problem/assets/70763346/a1994fed-5746-4b94-bb31-a60abaadf8e6)
![Earth mass equals 243](https://github.com/zolars1966/3-Body-problem/assets/70763346/eb0ab3d6-051b-45e9-9d9d-8663c644d9e0)

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

© 2019-2024 Zolars. This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Developed by Arseny Zolotarev
Initial development date: Tuesday, 18th of July, 2023
