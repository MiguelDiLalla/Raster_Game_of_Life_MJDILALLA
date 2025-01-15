# __init__.py

# Importa las clases principales
from .Filtering_function import apply_filter
from .gif_generator import GifGenerator

# Define las exportaciones públicas del módulo
__all__ = [
    "apply_filter",
    "GifGenerator"
]
