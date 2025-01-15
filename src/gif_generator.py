import numpy as np
from scipy.signal import convolve2d
from PIL import Image, ImageDraw
import os
import time
import random
from matplotlib.colors import to_rgb, to_hex

class GifGenerator:
    def __init__(self, initial_board=None, steps=50, verbose=False):
        """
        Inicializa el generador del GIF del Game of Life.

        Args:
            initial_board (numpy.ndarray, optional): Tablero inicial. Si no se especifica, se genera aleatoriamente.
            steps (int): Número de pasos a simular (default: 50, máximo: 500).
            verbose (bool): Si es True, imprime los parámetros y resultados en consola.
        """
        self.steps = min(steps, 500)  # Limitar el número de pasos a 500
        self.verbose = verbose
        self.metadata = {}
        
        # Validar y configurar el tablero inicial
        if initial_board is None:
            rows, cols = np.random.randint(10, 51, size=2)
            self.board = np.random.randint(2, size=(rows, cols))
        else:
            if not np.all(np.isin(initial_board, [0, 1])):
                raise ValueError("El tablero inicial solo debe contener 0s y 1s.")
            self.board = initial_board

        # self.metadata['initial_board'] = self.board.tolist()
        self.metadata['steps'] = self.steps
        self.metadata['hash'] = self._hash_board(self.board)

        if self.verbose:
            print("Parámetros iniciales:", self.metadata)

    def _hash_board(self, board):
        """Genera un hash único para el estado del tablero."""
        return hash(board.tobytes())


    def _count_neighbors(self, board):
        """Cuenta los vecinos vivos para cada celda usando convolución."""
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])
        return convolve2d(board, kernel, mode='same', boundary='wrap')
    
    def _update_board(self):
        """Actualiza el tablero según las reglas del Game of Life."""
        neighbors = self._count_neighbors(self.board)
        new_board = np.zeros_like(self.board)
        # Rule 1 and Rule 3: Any live cell with fewer than two or more than three live neighbors dies.
        new_board[(self.board == 1) & ((neighbors == 2) | (neighbors == 3))] = 1
        # Rule 4: Any dead cell with exactly three live neighbors becomes a live cell.
        new_board[(self.board == 0) & (neighbors == 3)] = 1
        self.board = new_board
        
    def simulate(self):
        """Ejecuta la simulación del Game of Life."""
        self.frames = []
        seen_states = set()
        start_time = time.time()

        for step in range(self.steps):
            board_hash = self._hash_board(self.board)
            if board_hash in seen_states:
                if self.verbose:
                    print(f"Ciclo detectado en el paso {step + 1}.")
                break

            seen_states.add(board_hash)
            self.frames.append(self.board.copy())
            self._update_board()

        self.metadata['simulated_steps'] = len(self.frames)
        self.metadata['execution_time'] = time.time() - start_time

        if self.verbose:
            print("Simulación completada:", self.metadata)

    def _generate_complementary_colors(self):
        """Genera un par de colores complementarios en formato HEX."""
        base_color = [random.random() for _ in range(3)]  # Color base aleatorio en RGB
        complementary_color = [1 - c for c in base_color]  # Color complementario
        # Convertir a formato HEX
        light_color = to_hex(base_color)
        dark_color = to_hex(complementary_color)
        return light_color, dark_color

    def generate_gif(self, show=False, save=False, filename="game_of_life.gif", color_alive=None, color_dead=None):
        """Genera un GIF de la simulación con colores personalizados.

        Args:
            show (bool): Si True, muestra el GIF al finalizar.
            save (bool): Si True, guarda el GIF en el archivo especificado.
            filename (str): Nombre del archivo para guardar el GIF.
            color_alive (str, optional): Color HEX para las células vivas.
            color_dead (str, optional): Color HEX para las células muertas.
        """
        if not hasattr(self, 'frames') or len(self.frames) == 0:
            raise RuntimeError("La simulación no se ha ejecutado. Llame a simulate() primero.")

        if color_alive is None or color_dead is None:
            color_alive, color_dead = self._generate_complementary_colors()

        if self.verbose:
            print(f"Colores utilizados: Vivas = {color_alive}, Muertas = {color_dead}")

        images = []
        for frame in self.frames:
            img = Image.new('RGB', (frame.shape[1], frame.shape[0]), color_dead)
            draw = ImageDraw.Draw(img)
            for y in range(frame.shape[0]):
                for x in range(frame.shape[1]):
                    if frame[y, x] == 1:
                        draw.rectangle([x, y, x + 1, y + 1], fill=color_alive)
            resize_factor = 1
            images.append(img.resize((frame.shape[1] * resize_factor, frame.shape[0] * resize_factor), Image.NEAREST))

        if save:
            images[0].save(
                filename, save_all=True, append_images=images[1:], duration=200, loop=0
            )
            if self.verbose:
                print(f"GIF guardado como {filename}")

        if show:
            # show gif FROM file if dsave is true
            os.system(f"start {filename}") # respect this

