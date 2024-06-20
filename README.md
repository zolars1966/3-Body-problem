# 3-Body-problem
A simple N-body system simulation, now including both 2D and 3D visualization options. Space objects are randomly generated and interact with each other according to the rules of classical mechanics.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Controls](#controls)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Images](#images)

## Features

- **2D and 3D Modes:** Both modes are available to visualize the simulation.
- **Interactive Controls:** Allow for dynamic camera positioning and different lighting models.
- **Multifile Project:** Structured in multiple Python files for better organization and maintainability.
- **Random Space Objects:** Objects are randomly generated each time the simulation starts.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/zolars1966/3-Body-problem.git
    cd 3-Body-problem
    ```

2. Install required packages:
    ```bash
    pip install pygame numpy
    ```

## Usage

Run the main script:
```bash
python main.py
```

The application will open a Pygame window displaying the simulation. You can switch between 2D and 3D modes and control various aspects of the simulation using the keyboard.

## Controls

### Mouse Controls:

- **Left Click:** Camera teleportation in the minimap.
- **Mouse Wheel:** Toggles minimap scale.

### Keyboard Controls:

- **Movement:**
  - `W`: Move camera forward
  - `S`: Move camera backward
  - `A`: Move camera left
  - `D`: Move camera right
  - `Q`: Move camera up
  - `E`: Move camera down

- **Speed Adjustments:**
  - `Shift`: Increase speed
  - `Ctrl`: Decrease speed

- **Lighting Models:**
  - `0`: Carcass
  - `1`: Diffuse Light
  - `2`: Lambert
  - `3`: Wrap
  - `4`: Phong
  - `5`: Blinn
  - `6`: Highlight
  - `7`: Blinn Highlight
  - `8`: Metal
  - `9`: Light Reflect

- **Other Controls:**
  - `ESC`: Toggle mouse cursor visibility
  - `R`: Toggle simulation speed
  - `O`: Toggle slow speedup mode
  - `P`: Toggle pause
  - `M`: Toggle minimap size
  - `L`: Toggle drawing trajectory

## Project Structure

```
3-Body-problem/
├── environment.py
├── globals.py
├── main.py
├── README.md
└── sengine.py
```

- `environment.py`: Handles the environment and object initialization.
- `globals.py`: Global variables and configurations.
- `main.py`: Main script, initializes the Pygame window and starts the simulation.
- `sengine.py`: Simulation engine, handles the physics and object interactions.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/NewFeature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/NewFeature`).
5. Create a new Pull Request.

## License

© 2019-2024 Zolars

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

Created by Arseny Zolotarev on July 18, 2023.


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
