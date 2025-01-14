from PIL import Image, ImageOps
from PIL.ImageQt import ImageQt
from skimage import exposure
import numpy as np
import hashlib
from PySide6.QtGui import QImage  # Importar QImage para la compatibilidad

class FilterResult:
    def __init__(self, original_image, processed_image, metadata):
        """
        Clase para encapsular el resultado del filtrado de una imagen.

        Args:
            original_image (PIL.Image.Image): Imagen original.
            processed_image (PIL.Image.Image): Imagen procesada.
            metadata (dict): Información adicional sobre el filtrado.
        """
        self.original_image = original_image
        self.processed_image = processed_image
        self.metadata = metadata

    def save(self, output_path):
        """Guarda la imagen procesada en el path especificado."""
        self.processed_image.save(output_path)


def calculate_new_dimensions(original_width, original_height, max_area):
    """
    Calcula las nuevas dimensiones para que el área total sea igual a max_area,
    respetando el ratio de aspecto de la imagen original.

    Args:
        original_width (int): Ancho original de la imagen.
        original_height (int): Altura original de la imagen.
        max_area (int): Área máxima permitida para la imagen redimensionada.

    Returns:
        tuple: Nuevas dimensiones (ancho, alto).
    """
    aspect_ratio = original_width / original_height
    new_height = int((max_area / aspect_ratio) ** 0.5)
    new_width = int(max_area / new_height)
    return new_width, new_height


def generate_hash(processed_image, params):
    """
    Genera un hash único basado en la imagen procesada y los parámetros usados.

    Args:
        processed_image (PIL.Image.Image): Imagen procesada.
        params (dict): Parámetros utilizados en el procesamiento.

    Returns:
        str: Hash único en formato hexadecimal.
    """
    hasher = hashlib.sha256()

    # Añadir bytes de la imagen procesada
    image_bytes = processed_image.tobytes()
    hasher.update(image_bytes)

    # Añadir los parámetros al hash
    for key, value in sorted(params.items()):
        hasher.update(f"{key}:{value}".encode('utf-8'))

    return hasher.hexdigest()


def apply_filter(image_path, max_area=256*256, light_correction_range=(20, 235)):
    """
    Aplica un filtro que incluye:
    1. Escala de grises con corrección de niveles ligeros.
    2. Creación de bandas de grises (banding).
    3. Aplicación de dithering binario.

    Args:
        image_path (str): Ruta del archivo de la imagen a procesar.
        max_area (int): Área máxima permitida para la imagen redimensionada.
        light_correction_range (tuple): Rango para la corrección de niveles de luz.

    Returns:
        FilterResult: Resultado del filtrado que incluye la imagen original, la procesada y metadata.
    """
    try:
        # Cargar la imagen
        original_image = Image.open(image_path)
        original_width, original_height = original_image.size

        # Redimensionar respetando el ratio de aspecto
        new_width, new_height = calculate_new_dimensions(original_width, original_height, max_area)
        resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Convertir a escala de grises
        grayscale_image = ImageOps.grayscale(resized_image)

        # Corrección de niveles ligeros
        grayscale_array = np.array(grayscale_image)
        grayscale_corrected = exposure.rescale_intensity(grayscale_array, in_range="image", out_range=light_correction_range)

        # Crear bandas de grises
        banded_image = ((grayscale_corrected // 32) * 32).astype(np.uint8)  # Crear 8 bandas de grises (0-255 dividido entre 8)

        # Aplicar dithering binario
        binary_image = Image.fromarray(banded_image).convert("1")
        binary_image_rgb = binary_image.convert("RGB")

        params = {
            "max_area": max_area,
            "light_correction_range": light_correction_range
        }

        hash_value = generate_hash(binary_image_rgb, params)

        metadata = {
            "original_size": (original_width, original_height),
            "resized_size": (new_width, new_height),
            "original_pixel_count": original_width * original_height,
            "resized_pixel_count": new_width * new_height,
            "filter_steps": ["grayscale", "level correction", "banding", "dithering"],
            "hash": hash_value
        }

        return FilterResult(original_image, binary_image_rgb, metadata)

    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        raise ValueError(f"No se pudo procesar la imagen: {e}")
