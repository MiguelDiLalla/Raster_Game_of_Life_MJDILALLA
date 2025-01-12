import numpy as np
from datetime import datetime
import platform
import cpuinfo

class Execution:
    def __init__(self, dimensions, steps, initial_state, seed=None):
        """
        Class to store and manage metadata and statistics for a Game of Life execution.

        Args:
            dimensions (tuple): Dimensions of the board (rows, columns).
            steps (int): Maximum number of steps to execute.
            initial_state (numpy.ndarray): Initial state of the board.
            seed (int, optional): Seed used for reproducibility.
        """
        self.dimensions = dimensions
        self.steps = steps
        self.initial_state = initial_state
        self.seed = seed if seed is not None else np.random.randint(0, 1000000)
        self.timestamp = datetime.now()  # Timestamp for the start of the execution
        self.step_count = 0
        self.alive_cells_stats = []  # Percentage of alive cells per step
        self.max_alive_cells = 0
        self.min_alive_cells = np.prod(dimensions)
        self.execution_time = 0
        self.processor_info = cpuinfo.get_cpu_info()

    def update_stats(self, board):
        """
        Updates the statistics of the execution for each step.

        Args:
            board (numpy.ndarray): Current board state after a step.
        """
        alive_cells = np.sum(board)
        total_cells = self.dimensions[0] * self.dimensions[1]
        alive_percentage = alive_cells / total_cells * 100
        self.alive_cells_stats.append(alive_percentage)
        self.max_alive_cells = max(self.max_alive_cells, alive_cells)
        self.min_alive_cells = min(self.min_alive_cells, alive_cells)

    def finalize(self, step_count, execution_time):
        """
        Finalizes the execution by recording final statistics.

        Args:
            step_count (int): Total number of steps executed.
            execution_time (float): Total execution time in seconds.
        """
        self.step_count = step_count
        self.execution_time = execution_time

    def to_dict(self):
        """
        Converts the metadata into a dictionary for export.

        Returns:
            dict: A dictionary containing metadata and statistics.
        """
        return {
            "dimensions": self.dimensions,
            "steps": self.steps,
            "step_count": self.step_count,
            "execution_time": self.execution_time,
            "max_alive_cells": self.max_alive_cells,
            "min_alive_cells": self.min_alive_cells,
            "alive_cells_stats": self.alive_cells_stats,
            "seed": self.seed,
            "timestamp": self.timestamp.isoformat(),
            "processor": self.processor_info.get('brand_raw', 'Unknown Processor'),
            "architecture": platform.architecture()[0],
            "system": platform.system(),
            "processor_name": platform.processor()
        }


class GameOfLife:
    def __init__(self, dimensions=(10, 10), steps=0, initial_state=None, seed=None, verbose=False):
        """
        Class implementing Conway's Game of Life simulation.

        Args:
            dimensions (tuple): Dimensions of the board (rows, columns).
            steps (int): Number of steps to run the simulation.
            initial_state (numpy.ndarray, optional): Custom initial board state.
            seed (int, optional): Seed for reproducibility.
            verbose (bool): If True, prints detailed information during simulation.
        """
        self.rows, self.cols = dimensions
        self.steps = steps
        np.random.seed(seed)
        self.seed = seed if seed is not None else np.random.randint(0, 1000000)
        self.verbose = verbose
        self.board = (
            initial_state
            if initial_state is not None
            else np.random.randint(2, size=(self.rows, self.cols))
        )
        self.execution = Execution(
            dimensions=dimensions, steps=steps, initial_state=self.board.copy(), seed=self.seed
        )

        if self.verbose:
            print("--- Game of Life Initialization ---")
            print(f"Dimensions: {dimensions}")
            print(f"Steps: {steps} (default)" if steps == 0 else f"Steps: {steps} (user-defined)")
            print(f"Seed: {self.seed} (random)" if seed is None else f"Seed: {self.seed} (user-defined)")
            print(f"Initial State: {'default-random' if initial_state is None else 'user-defined'}")

    def count_neighbors(self, board):
        """
        Counts the number of alive neighbors for each cell.

        Args:
            board (numpy.ndarray): Current state of the board.

        Returns:
            numpy.ndarray: Array with neighbor counts for each cell.
        """
        neighbors = (
            np.roll(np.roll(board, 1, axis=0), 1, axis=1) +
            np.roll(np.roll(board, 1, axis=0), -1, axis=1) +
            np.roll(np.roll(board, -1, axis=0), 1, axis=1) +
            np.roll(np.roll(board, -1, axis=0), -1, axis=1) +
            np.roll(board, 1, axis=0) +
            np.roll(board, -1, axis=0) +
            np.roll(board, 1, axis=1) +
            np.roll(board, -1, axis=1)
        )
        return neighbors

    def step(self):
        """
        Executes a single step of the simulation, updating the board state.
        """
        neighbors = self.count_neighbors(self.board)
        self.board = (
            (self.board & (neighbors == 2)) | (neighbors == 3)
        ).astype(int)
        self.execution.update_stats(self.board)

        if self.verbose:
            print(f"Step {self.execution.step_count + 1}: Alive Cells = {np.sum(self.board)}")

    def run(self):
        """
        Runs the simulation for the specified number of steps.
        """
        import time
        start_time = time.time()

        if self.verbose:
            print("--- Simulation Started ---")

        for step in range(self.steps):
            self.step()

        end_time = time.time()
        self.execution.finalize(step + 1, end_time - start_time)

        if self.verbose:
            print("--- Simulation Ended ---")
            print(f"Total Steps Executed: {self.execution.step_count}")
            print(f"Execution Time: {self.execution.execution_time:.2f} seconds")

    def get_execution_stats(self):
        """
        Retrieves the execution statistics.

        Returns:
            str: Formatted summary of the execution statistics.
        """
        return self.execution.to_dict()

# Example usage:
if __name__ == "__main__":
    game = GameOfLife(dimensions=(10, 10), steps=5, verbose=True)
    game.run()
    print(game.get_execution_stats())
