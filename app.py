import streamlit as st
from src.game_of_life import GameOfLife
from src.visualization import visualize_game

# Inicializar session_state para almacenar metadata y último GIF generado
if 'last_simulation' not in st.session_state:
    st.session_state['last_simulation'] = {
        'gif_path': None,
        'metadata': {}
    }

# Función para la barra lateral izquierda: Video streaming
def sidebar_video_stream():
    st.sidebar.header("Video Stream")
    st.sidebar.video("https://www.example.com/video.mp4", format="mp4", start_time=0)
    audio_button = st.sidebar.button("Audio")
    if audio_button:
        st.sidebar.info("Audio activado/desactivado (esto es solo un ejemplo).")

# Función para el segundo bloque: Game of Life
def game_of_life_block():
    st.markdown("<div style='text-align: left;'>", unsafe_allow_html=True)
    st.header("Game of Life: Simulación Basada en GIF")

    # Contenedor principal para la visualización
    visualization_container = st.container()

    # Parámetros del tablero con entradas de texto
    rows = st.number_input("Filas", min_value=10, max_value=2000, value=14, step=1, key="rows_input")
    cols = st.number_input("Columnas", min_value=10, max_value=2000, value=100, step=1, key="cols_input")
    steps = st.number_input("Pasos", min_value=1, max_value=500, value=100, step=1, key="steps_input")

    # Selección de colores
    color_alive = st.color_picker("Color para células vivas", value="#000000")
    color_dead = st.color_picker("Color para células muertas", value="#FFFFFF")

    # Booleano para randomizar colores
    randomize_colors = st.checkbox("Randomizar colores", value=False)

    # Menú desplegable para tamaño de archivo límite
    file_size_limit = st.selectbox("Tamaño límite del archivo (MB)", options=[1, 5, 10, 20, 50], index=2)

    # Botón para renderizar
    if st.button("Renderizar Simulación"):
        # Crear simulación inicial
        default_game = GameOfLife(dimensions=(rows, cols), steps=steps, verbose=True)
        default_game.run()
        gif_path = "default_game_of_life.gif"
        metadata = {
            'rows': rows,
            'cols': cols,
            'steps': steps,
            'color_alive': color_alive,
            'color_dead': color_dead,
            'randomize_colors': randomize_colors,
            'file_size_limit': file_size_limit,
            'generations': default_game.execution.step_count,
            'max_alive_cells': default_game.execution.max_alive_cells,
            'min_alive_cells': default_game.execution.min_alive_cells,
            'execution_time': default_game.execution.execution_time
        }
        visualize_game(
            game_of_life=default_game,
            cell_size=10,  # Valor fijo de ejemplo para el tamaño de celda
            save_as_gif=True,
            gif_path=gif_path,
            disable_display=True,
            color_alive=color_alive,
            color_dead=color_dead,
            randomize_colors=randomize_colors
        )

        # Almacenar resultados en session_state
        st.session_state['last_simulation'] = {
            'gif_path': gif_path,
            'metadata': metadata
        }

        with visualization_container:
            st.image(
                gif_path,
                caption="Simulación Generada (GIF)",
                use_container_width=True
            )

    # Botón para guardar el GIF
    if st.session_state['last_simulation']['gif_path']:
        with open(st.session_state['last_simulation']['gif_path'], "rb") as file:
            st.download_button(
                label="Guardar GIF",
                data=file,
                file_name="game_of_life_simulation.gif",
                mime="image/gif"
            )

    # Mostrar metadata de la última simulación
    if st.session_state['last_simulation']['metadata']:
        st.subheader("Última Simulación")
        st.json(st.session_state['last_simulation']['metadata'])

    st.text("Ajusta los parámetros y haz clic en 'Renderizar Simulación' para generar un nuevo GIF.")
    st.markdown("</div>", unsafe_allow_html=True)

# Función para la barra lateral derecha: Historia del proyecto
def right_sidebar_project_story():
    st.markdown("<div style='text-align: right; text-justify: inter-word;'>", unsafe_allow_html=True)
    st.header("Historia del Proyecto")
    st.markdown(
        """
        Aquí puedes incluir una descripción detallada del proyecto, sus objetivos, y cualquier información histórica relevante.
        Este espacio puede usarse como un archivo permanente de datos relacionados con el desarrollo.
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Llamada a la barra lateral izquierda
sidebar_video_stream()

# Detectar formato móvil o escritorio (simulado para esta implementación)
is_mobile = st.checkbox("Simular formato móvil", value=False)

if is_mobile:
    # Disposición vertical (tres bloques uno debajo de otro)
    game_of_life_block()
    right_sidebar_project_story()
else:
    # Disposición horizontal con proporciones específicas
    col1, col2, col3 = st.columns([1, 2, 1])  # Proporción: Video (1), Game (2), Texto (1)
    with col1:
        st.sidebar.empty()  # La barra lateral se mueve a la izquierda
    with col2:
        game_of_life_block()
    with col3:
        right_sidebar_project_story()
