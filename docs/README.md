# Project Documentation: Game of Life

## Overview
This project is a comprehensive implementation of Conway's "Game of Life," emphasizing modularity, scalability, and interactivity. It leverages Python libraries such as NumPy, Pygame, and Streamlit to provide a dynamic and educational platform for exploring cellular automata. The project includes enhanced visualization features, statistical tracking, and an interactive web interface.

## Key Features

### Core Engine (`game_of_life.py`)
- **Efficient Simulation**: Uses convolution with SciPy to compute neighbors, optimizing performance for large grids.
- **Execution Metadata**: Tracks key metrics such as alive cells, loop detection, and execution time.
- **Verbose Mode**: Provides real-time feedback during the simulation.

#### Example Usage:
```python
from game_of_life import GameOfLife

game = GameOfLife(dimensions=(50, 50), steps=100, verbose=True)
game.run()
print(game.get_execution_stats())
```

### Visualization Module (`visualization.py`)
- **Color Customization**: Supports custom or random color palettes for alive and dead cells.
- **GIF Export**: Captures and saves simulations as animated GIFs.
- **Grid Control**: Adjustable cell sizes and grid colors for better visuals.

#### Example Usage:
```python
from visualization import visualize_game

visualize_game(
    game_of_life=game,
    save_as_gif=True,
    gif_path="simulation.gif",
    color_alive="#00FF00",
    color_dead="#000000",
    fps=15
)
```

### Streamlit Interface (`app.py`)
- **Interactive Simulation**: Configure grid dimensions, steps, and colors directly in the web interface.
- **Real-Time Feedback**: View progress, statistics, and rendered GIFs in a user-friendly layout.
- **Session Management**: Tracks the last simulation metadata and GIF for easy download.

#### Example Interface Workflow:
1. Set grid dimensions, number of steps, and cell colors.
2. Click **Render Simulation** to generate and display a GIF.
3. Download the generated GIF or explore the metadata.

### Testing Module (`test_game_of_life.py`)
- **Preset Patterns**: Includes classic configurations like "block," "blinker," and "glider."
- **Randomized Tests**: Generates random boards for exploratory simulations.
- **Visualization Integration**: Optional live visualization during test runs.

#### Example Test:
```python
from test_game_of_life import test_simulation

test_result = test_simulation(rows=20, cols=20, steps=50, preset="glider", visualize=True)
print(test_result)
```

## Getting Started

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/game-of-life
   cd game-of-life
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Streamlit App
Launch the interactive interface:
```bash
streamlit run app.py
```

### Running a Standalone Simulation
```python
from game_of_life import GameOfLife

game = GameOfLife(dimensions=(30, 30), steps=50)
game.run()
```

## Roadmap

1. **Core Engine Improvements**
   - Implement additional boundary conditions.
   - Add custom rule configurations.
2. **Visualization Enhancements**
   - Support for 3D cellular automata visualizations.
   - Interactive real-time editing of grid states.
3. **Performance Optimization**
   - Introduce GPU acceleration for larger simulations.
   - Explore multi-threading for faster computations.

## Contributing
We welcome contributions to improve this project! Please adhere to the [contribution guidelines](CONTRIBUTING.md).

## License
This project is licensed under the GNU General Public License, Version 3 (GPLv3).

---

This documentation reflects the current state of the project and will evolve as new features are added. Stay tuned for updates!

