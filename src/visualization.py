import pygame
import numpy as np
import random
from PIL import Image

def generate_color_pair():
    """
    Genera un par de colores predefinidos de una biblioteca estilística.

    Returns:
        tuple: (alive_color, dead_color) en formato RGB.
    """
    color_palettes = [
        ((0, 255, 0), (0, 0, 0)),  # Verde vivo sobre negro
        ((0, 0, 255), (10, 10, 30)),  # Azul vivo sobre azul oscuro
        ((255, 165, 0), (30, 15, 5)),  # Naranja sobre marrón oscuro
        ((255, 0, 0), (50, 0, 0)),  # Rojo sobre rojo oscuro
        ((255, 255, 255), (0, 0, 0)),  # Blanco sobre negro
        ((255, 223, 186), (34, 34, 59))  # Tono pastel sobre azul profundo
    ]
    return random.choice(color_palettes)

def invert_colors(alive_color, dead_color):
    """
    Invierte los colores vivos y muertos.

    Args:
        alive_color (tuple): Color actual de las celdas vivas.
        dead_color (tuple): Color actual de las celdas muertas.

    Returns:
        tuple: Nuevos colores invertidos (alive_color, dead_color).
    """
    return dead_color, alive_color

def hex_to_rgb(hex_color):
    """
    Convierte un color hexadecimal a un formato RGB.

    Args:
        hex_color (str): Color en formato hexadecimal (e.g., "#FFFFFF").

    Returns:
        tuple: Color en formato RGB (R, G, B).
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def capture_frame(surface):
    """
    Captura el contenido de la ventana de pygame como una imagen de PIL.

    Args:
        surface (pygame.Surface): Superficie de la ventana de pygame.

    Returns:
        PIL.Image: Imagen capturada de la ventana.
    """
    data = pygame.image.tostring(surface, "RGB")
    width, height = surface.get_size()
    return Image.frombytes("RGB", (width, height), data)

def visualize_game(
    game_of_life,
    cell_size=None,
    save_as_gif=False,
    gif_path="game_of_life.gif",
    disable_display=False,
    color_alive="#000000",
    color_dead="#FFFFFF",
    randomize_colors=False,
    grid_color=(50, 50, 50),
    fps=None,
    show_stats=False,
    verbose=False
):
    """
    Visualiza la simulación del Game of Life usando pygame, con captura de cuadros y exportación a GIF.

    Args:
        game_of_life (GameOfLife): Instancia del juego.
        cell_size (int, optional): Tamaño de cada celda en píxeles. Aleatorio si None.
        save_as_gif (bool): Si True, guarda la simulación como un archivo GIF.
        gif_path (str): Ruta para guardar el GIF.
        disable_display (bool): Si True, evita que Pygame abra una ventana.
        color_alive (str): Color hexadecimal para células vivas.
        color_dead (str): Color hexadecimal para células muertas.
        randomize_colors (bool): Si True, genera colores aleatorios para células vivas y muertas.
        grid_color (tuple): Color de las líneas de la cuadrícula (RGB).
        fps (int, optional): Cuadros por segundo para la animación. Aleatorio si None.
        show_stats (bool): Si True, muestra estadísticas minimalistas.
        verbose (bool): Si True, imprime detalles de los parámetros utilizados.
    """
    pygame.init()

    # Asignar valores por defecto o aleatorios
    cell_size = cell_size or random.choice(range(5, 21))
    fps = fps or random.choice(range(5, 31))

    if randomize_colors:
        alive_color, dead_color = generate_color_pair()
    else:
        alive_color = hex_to_rgb(color_alive)
        dead_color = hex_to_rgb(color_dead)

    parameters = {
        "Cell Size": cell_size,
        "Alive Color": alive_color,
        "Dead Color": dead_color,
        "Randomize Colors": randomize_colors,
        "Grid Color": grid_color,
        "FPS": fps,
        "Save as GIF": save_as_gif,
        "GIF Path": gif_path,
        "Disable Display": disable_display
    }

    if verbose:
        print("\n--- Simulation Parameters ---")
        for key, value in parameters.items():
            print(f"{key}: {value}")

    # Crear la superficie de renderizado
    width, height = game_of_life.cols * cell_size, game_of_life.rows * cell_size
    if disable_display:
        screen = pygame.Surface((width, height))  # Superficie sin ventana
    else:
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Game of Life")

    # Fuente para estadísticas (si están habilitadas)
    font = pygame.font.SysFont("consolas", 20)

    # Reloj para controlar el framerate
    clock = pygame.time.Clock()

    running = True
    paused = False
    generation = 0
    previous_boards = []
    loop_counter = 0
    max_loops = 60  # Límite de iteraciones en caso de estancamiento

    frames = []  # Almacenar cuadros para crear el GIF

    while running:
        if not disable_display:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Pausar/Reanudar
                        paused = not paused
                    elif event.key == pygame.K_r:  # Reiniciar
                        game_of_life.board = np.random.randint(2, size=(game_of_life.rows, game_of_life.cols))
                        generation = 0
                        previous_boards = []
                        loop_counter = 0

        if not paused:
            # Avanzar un paso en la simulación
            game_of_life.step()
            generation += 1

            # Verificar ciclos o estancamiento
            board_tuple = tuple(map(tuple, game_of_life.board))
            if len(previous_boards) > 0 and board_tuple == previous_boards[-1]:
                # Si el tablero actual es igual al anterior, incrementar contador
                loop_counter += 1
            elif len(previous_boards) > 1 and board_tuple == previous_boards[-2]:
                # Si el tablero alterna con el anterior al último
                loop_counter += 1
            else:
                # Reiniciar contador si no hay ciclo
                loop_counter = 0

            if loop_counter >= max_loops:
                alive_color, dead_color = invert_colors(alive_color, dead_color)
                show_stats = True  # Forzar mostrar estadísticas
                running = False  # Terminar ejecución después del countdown

            previous_boards.append(board_tuple)
            if len(previous_boards) > 10:  # Mantener un historial limitado
                previous_boards.pop(0)

        # Dibujar el estado actual del tablero
        screen.fill(grid_color)  # Fondo con color de cuadrícula
        for row in range(game_of_life.rows):
            for col in range(game_of_life.cols):
                color = alive_color if game_of_life.board[row, col] == 1 else dead_color
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(
                        col * cell_size, row * cell_size, cell_size, cell_size
                    )
                )

        # Capturar cuadro si se va a guardar como GIF
        if save_as_gif:
            frames.append(capture_frame(screen))

        # Mostrar estadísticas si está habilitado
        if show_stats and not disable_display:
            alive_cells = np.sum(game_of_life.board)
            stats_text = f"Gen: {generation} | Alive: {alive_cells}"
            stats_surface = font.render(stats_text, True, (255, 255, 255))
            screen.blit(stats_surface, (10, 10))

        if not disable_display:
            pygame.display.flip()
            clock.tick(fps)

    pygame.quit()

    # Guardar el GIF si es necesario
    if save_as_gif and frames:
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=1000 // fps,
            loop=0
        )
        if verbose:
            print(f"GIF guardado en {gif_path}")
