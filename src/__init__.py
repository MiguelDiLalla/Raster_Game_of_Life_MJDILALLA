# __init__.py

# Importa las clases principales
from .game_of_life import GameOfLife, Execution

# Importa herramientas adicionales (si existen)
# from .dithering import apply_dithering
# from .image_processing import process_image
from .visualization import visualize_game

# Define las exportaciones públicas del módulo
__all__ = [
    "GameOfLife",
    "visualize_game"
]
