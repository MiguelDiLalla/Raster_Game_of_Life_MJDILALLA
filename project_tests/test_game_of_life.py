import os
import sys
import numpy as np
from src.game_of_life import GameOfLife
from src.visualization import visualize_game
import random

# Asegurar que /src esté en el sys.path para los imports
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
if src_path not in sys.path:
    sys.path.append(src_path)

def generate_random_board(rows, cols, seed=None):
    """
    Genera un tablero aleatorio de dimensiones especificadas.

    Args:
        rows (int): Número de filas del tablero.
        cols (int): Número de columnas del tablero.
        seed (int, optional): Semilla para reproducibilidad.

    Returns:
        numpy.ndarray: Tablero inicial aleatorio.
    """
    np.random.seed(seed)
    print(f"Generando un tablero aleatorio de {rows}x{cols} con semilla {seed}.")
    return np.random.randint(2, size=(rows, cols))

def generate_preset_board(preset=None, rows=5, cols=5):
    """
    Genera tableros predefinidos basados en patrones clásicos o selecciona uno aleatoriamente.

    Args:
        preset (str, optional): Nombre del patrón ("block", "blinker", "glider", "random"), o None para seleccionar "random".
        rows (int, optional): Número de filas para el tablero aleatorio.
        cols (int, optional): Número de columnas para el tablero aleatorio.

    Returns:
        numpy.ndarray: Tablero inicial con el patrón seleccionado.
    """
    patterns = {
        "block": np.array([
            [1, 1],
            [1, 1]
        ]),
        "blinker": np.array([
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0]
        ]),
        "glider": np.array([
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1]
        ]),
        "random": lambda: generate_random_board(rows, cols)  # Generar tablero aleatorio con dimensiones especificadas
    }

    if preset is None:
        preset = "random"
        print(f"Preset no especificado. Seleccionando: {preset}.")

    print(f"Seleccionando un patrón predefinido: {preset}.")

    if preset not in patterns:
        raise ValueError(f"Preset '{preset}' no está definido.")

    if preset == "random":
        return patterns[preset]()  # Genera dinámicamente un tablero aleatorio con las dimensiones dadas

    # Ajustar el patrón predefinido al tamaño especificado (centrado en el tablero)
    pattern = patterns[preset]
    board = np.zeros((rows, cols), dtype=int)
    start_row = (rows - pattern.shape[0]) // 2
    start_col = (cols - pattern.shape[1]) // 2
    board[start_row:start_row + pattern.shape[0], start_col:start_col + pattern.shape[1]] = pattern
    return board

def run_simulation(initial_state, steps=10):
    """
    Ejecuta una simulación del Game of Life.

    Args:
        initial_state (numpy.ndarray): Tablero inicial.
        steps (int): Número de pasos a ejecutar.

    Returns:
        GameOfLife: Objeto del juego tras la simulación.
    """
    print(f"Ejecutando simulación con {steps} pasos.")
    game = GameOfLife(initial_state=initial_state, steps=steps)
    game.run()
    return game

def test_simulation(rows=None, cols=None, steps=None, preset=None, seed=None, visualize=False):
    """
    Ejecuta una simulación unitaria con parámetros ajustables o aleatorizados y reporta resultados.

    Args:
        rows (int, optional): Número de filas del tablero.
        cols (int, optional): Número de columnas del tablero.
        steps (int, optional): Número de pasos a ejecutar.
        preset (str, optional): Patrón predefinido ("block", "blinker", "glider", "random") o None para seleccionar "random".
        seed (int, optional): Semilla para reproducibilidad.
        visualize (bool, optional): Si True, genera una visualización.

    Returns:
        dict: Resumen de la simulación.
    """
    # Aleatorizar parámetros si no se proporcionan
    rows = rows or random.choice(range(10, 101))
    cols = cols or random.choice(range(10, 101))
    steps = steps or random.choice(range(1, 501))

    if preset is None:
        preset = "random"
        print(f"Preset no especificado. Seleccionando: {preset}")
        initial_state = generate_preset_board(preset, rows, cols)
    elif preset == "random":
        seed = seed or random.randint(0, 1000000)  # Generar semilla aleatoria si no se proporciona
        initial_state = generate_random_board(rows, cols, seed)
    else:
        initial_state = generate_preset_board(preset, rows, cols)

    game = run_simulation(initial_state, steps)

    if visualize:
        print("Iniciando visualización...")
        visualize_game(game_of_life=game)

    summary = {
        "Dimensions": f"{rows} x {cols}",
        "Steps Executed": f"{game.execution.step_count}/{steps}",
        "Execution Time": f"{game.execution.execution_time:.2f} seconds",
        "Max Alive Cells": game.execution.max_alive_cells,
        "Min Alive Cells": game.execution.min_alive_cells,
        "Loop Detected": "Yes" if game.execution.loop_detected else "No",
        "Loop Length": game.execution.loop_length if game.execution.loop_detected else "N/A",
        "Seed": seed,
    }

    return summary

# # Ejemplo de ejecución directa
# if __name__ == "__main__":
#     report = test_simulation(visualize=True)
#     print("\n--- Resumen de la Simulación ---")
#     for key, value in report.items():
#         print(f"{key}: {value}")
