import streamlit as st
import numpy as np
from src.Filtering_function import apply_filter
from src.gif_generator import GifGenerator

# Page Configuration
st.set_page_config(
    # page_title="Game of Life GIF Generator",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Title
st.title("DITHERING !!! & run")

# Create two columns
left_col, right_col = st.columns(2)

# Left Column: File Uploader
with left_col:
    st.header("Game of Life GIF Generator")
    # st.write("Upload an image to define the initial state of the Game of Life.")

    uploaded_file = st.file_uploader(
        " ",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=False
    )

    if uploaded_file is not None:
        # st.write("File uploaded successfully! Processing the image.")

        # Apply filtering
        try:
            filter_result = apply_filter(uploaded_file, max_area=256*256, dithering_algorithm='floyd_steinberg')
            processed_image = filter_result.processed_image

            st.image(processed_image, caption="Processed Image", use_container_width=True)

            # Store the processed image in the session state
            st.session_state["processed_image"] = processed_image

            # Automatically generate the GIF
            image_array = np.array(processed_image.convert("1"))
            initial_board = (image_array > 0).astype(int)

            gif_path = "game_of_life_simulation.gif"
            generator = GifGenerator(initial_board=initial_board, steps=10, verbose=True)
            generator.simulate()
            generator.generate_gif(save=True, filename=gif_path)

            # Store the generated GIF path in the session state
            st.session_state["gif_path"] = gif_path

        except Exception as e:
            st.error(f"Error processing the image: {e}")

# Right Column: GIF Output
with right_col:
    st.header("Generated Simulation")

    if "gif_path" in st.session_state:
        st.image(st.session_state["gif_path"], caption="Simulation Output", use_container_width=True)
