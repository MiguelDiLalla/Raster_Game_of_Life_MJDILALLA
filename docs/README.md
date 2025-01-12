# Project Documentation: Game of Life

## Overview
This project provides a modular and optimized implementation of Conway's "Game of Life," enabling efficient simulation, detailed analysis, and visualization. The design emphasizes flexibility, scalability, and reproducibility, making it suitable for educational, research, and aesthetic purposes.

## Features and Modules

### Core Engine (`game_of_life.py`)
The core of the project includes:
- **GameOfLife Class:** Implements Conway's rules and simulates state transitions efficiently.
- **Execution Class:** Tracks metadata, statistics, and execution details such as:
  - Percentage of alive cells over time.
  - Loop detection to identify repeating states.
  - Execution time, seed, and environment details.

#### Example Usage
```python
from game_of_life import GameOfLife

# Initialize and run the simulation
game = GameOfLife(dimensions=(30, 30), steps=50, seed=1234)
game.run()

# Retrieve execution statistics
print(game.get_execution_stats())
```

### Visualization Module (`visualization.py`)
Facilitates dynamic visualization of the simulation using **Pygame**, with features including:
- **Color Pair Selection:** Generates random or predefined color schemes for alive and dead cells.
- **Interactive Controls:** Pause, reset, or adjust the simulation in real time.
- **GIF Export:** Optionally saves the simulation as an animated GIF.

#### Example Usage
```python
from game_of_life import GameOfLife
from visualization import visualize_game

# Run and visualize the simulation
game = GameOfLife(dimensions=(20, 20), steps=100)
visualize_game(game, save_as_gif=True, gif_path="output.gif")
```

### Testing Module (`test_game_of_life.py`)
Provides tools to verify the behavior and correctness of the simulation:
- Generates random or preset initial states (e.g., "glider," "block").
- Configures simulation parameters dynamically.
- Includes visualization during testing for interactive debugging.

#### Example Test
```python
from test_game_of_life import test_simulation

# Run a test with a preset pattern
report = test_simulation(preset="glider", steps=50, visualize=True)

# Print the simulation summary
for key, value in report.items():
    print(f"{key}: {value}")
```

### Initialization (`__init__.py`)
Centralizes imports for the module, exposing key components like `GameOfLife`, `Execution`, and utility functions.

### Planned Features
1. **Advanced Visualization:**
   - Streamlit-based web interface for remote simulation.
   - Enhanced customization of visual aesthetics.
2. **Rule Extensions:**
   - Support for non-standard cellular automata rules.
3. **Performance Enhancements:**
   - GPU acceleration for large-scale simulations.
   - Multi-threaded execution for better performance.

## Getting Started

### Installation
Clone the repository and install required dependencies:
```bash
git clone https://github.com/your-repo/game-of-life
cd game-of-life
pip install -r requirements.txt
```

### Running the Simulation
```python
from game_of_life import GameOfLife

# Define dimensions and steps
game = GameOfLife(dimensions=(50, 50), steps=200)
game.run()
```

### Custom Initial State
```python
import numpy as np
from game_of_life import GameOfLife

initial_state = np.array([
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
])
game = GameOfLife(dimensions=(3, 3), steps=10, initial_state=initial_state)
game.run()
```

## Roadmap

1. **Core Engine Refinement**
   - Extend boundary conditions.
   - Optimize neighbor computation for larger grids.
2. **Visualization Enhancements**
   - Real-time visual feedback during parameter tuning.
   - Animated export improvements.
3. **Interactivity Features**
   - Add user-driven pattern creation tools.
4. **Testing and Validation**
   - Automated test suite integration for CI/CD pipelines.

## Contributing
Contributions are welcome to enhance this project! Follow the [contribution guidelines](CONTRIBUTING.md) in the repository.

## License
This project is licensed under the GNU General Public License, Version 3 (GPLv3).

---

This documentation will evolve as features are added and the project grows. Stay tuned for updates!

