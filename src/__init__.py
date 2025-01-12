# __init__.py

# Importa las clases principales
from .game_of_life import GameOfLife

# Importa herramientas adicionales si existen
try:
    from .visualization import visualize_game
except ImportError:
    print("visualize_game no pudo ser importado correctamente. Verifica visualization.py.")

# Define las exportaciones públicas del módulo
__all__ = [
    "GameOfLife",
    "visualize_game"
]
