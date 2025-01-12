import numpy as np
from datetime import datetime
import platform
import cpuinfo
from visualization import visualize_game

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
        self.loop_detected = False
        self.loop_length = 0
        self.operations_count = 0

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
        self.operations_count += 1

    def finalize(self, step_count, execution_time, loop_detected=False, loop_length=0):
        """
        Finalizes the execution by recording final statistics.

        Args:
            step_count (int): Total number of steps executed.
            execution_time (float): Total execution time in seconds.
            loop_detected (bool): Whether a loop was detected.
            loop_length (int): Length of the detected loop.
        """
        self.step_count = step_count
        self.execution_time = execution_time
        self.loop_detected = loop_detected
        self.loop_length = loop_length

    def get_loop_info(self):
        """
        Returns loop detection status and its length.

        Returns:
            tuple: (loop_detected, loop_length)
        """
        return self.loop_detected, self.loop_length

    def summary(self):
        """
        Generates a user-friendly summary of the execution statistics.

        Returns:
            str: A formatted string summarizing the execution.
        """
        return f"""
        Game of Life Execution Summary
        --------------------------------
        Dimensions: {self.dimensions[0]} x {self.dimensions[1]}
        Steps Executed: {self.step_count}/{self.steps}
        Execution Time: {self.execution_time:.2f} seconds
        Max Alive Cells: {self.max_alive_cells}
        Min Alive Cells: {self.min_alive_cells}
        Operations Count: {self.operations_count}
        Loop Detected: {'Yes' if self.loop_detected else 'No'}
        Loop Length: {self.loop_length if self.loop_detected else 'N/A'}
        Timestamp: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
        Seed: {self.seed if self.seed is not None else 'Randomly Generated'}
        Processor: {self.processor_info.get('brand_raw', 'Unknown Processor')}
        System: {platform.system()} {platform.architecture()[0]}
        """

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
            "processor_name": platform.processor(),
            "loop_detected": self.loop_detected,
            "loop_length": self.loop_length,
            "operations_count": self.operations_count
        }

class GameOfLife:
    def __init__(self, dimensions=(10, 10), steps=0, initial_state=None, seed=None):
        """
        Class implementing Conway's Game of Life simulation.

        Args:
            dimensions (tuple): Dimensions of the board (rows, columns).
            steps (int): Number of steps to run the simulation.
            initial_state (numpy.ndarray, optional): Custom initial board state.
            seed (int, optional): Seed for reproducibility.
        """
        self.rows, self.cols = dimensions
        self.steps = steps
        np.random.seed(seed)
        self.seed = seed
        self.board = (
            initial_state
            if initial_state is not None
            else np.random.randint(2, size=(self.rows, self.cols))
        )
        self.execution = Execution(
            dimensions=dimensions, steps=steps, initial_state=self.board.copy(), seed=seed
        )

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

    def run(self):
        """
        Runs the simulation for the specified number of steps.
        """
        import time
        start_time = time.time()
        previous_boards = []
        loop_detected = False
        loop_length = 0

        for step in range(self.steps):
            self.step()

            # Check for loops
            board_tuple = tuple(map(tuple, self.board))
            if board_tuple in previous_boards:
                loop_detected = True
                loop_length = len(previous_boards) - previous_boards.index(board_tuple)
                break
            previous_boards.append(board_tuple)
            if len(previous_boards) > 100:  # Limit history size
                previous_boards.pop(0)

        end_time = time.time()
        self.execution.finalize(step + 1, end_time - start_time, loop_detected, loop_length)

    def get_execution_stats(self):
        """
        Retrieves the execution statistics.

        Returns:
            str: Formatted summary of the execution statistics.
        """
        return self.execution.summary()

# Centralized interface for running and visualizing the game
def run_and_visualize(dimensions, steps, seed=None):
    """
    Centralized method to run and visualize a Game of Life simulation.

    Args:
        dimensions (tuple): Dimensions of the board (rows, columns).
        steps (int): Number of steps to run the simulation.
        seed (int, optional): Seed for reproducibility.
    """
    game = GameOfLife(dimensions=dimensions, steps=steps, seed=seed)
    game.run()
    visualize_game(game)
