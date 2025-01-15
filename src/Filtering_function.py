import numpy as np
from PIL import Image, ImageOps
from skimage import exposure
import hashlib

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


def apply_floyd_steinberg_dithering(image_array):
    """
    Aplica el algoritmo de dithering de Floyd–Steinberg a una imagen en escala de grises.

    Args:
        image_array (numpy.ndarray): Array de la imagen en escala de grises.

    Returns:
        numpy.ndarray: Imagen con dithering aplicado.
    """
    height, width = image_array.shape
    for y in range(height):
        for x in range(width):
            old_pixel = image_array[y, x]
            new_pixel = 255 if old_pixel > 127 else 0
            image_array[y, x] = new_pixel
            error = old_pixel - new_pixel

            if x + 1 < width:
                image_array[y, x + 1] += error * 7 / 16
            if y + 1 < height:
                if x > 0:
                    image_array[y + 1, x - 1] += error * 3 / 16
                image_array[y + 1, x] += error * 5 / 16
                if x + 1 < width:
                    image_array[y + 1, x + 1] += error * 1 / 16

    return np.clip(image_array, 0, 255)


def apply_filter(image_path, max_area=256*256, light_correction_range=(20, 235), dithering_algorithm=None):
    """
    Aplica un filtro que incluye:
    1. Escala de grises con corrección de niveles ligeros.
    2. Creación de bandas de grises (banding).
    3. Aplicación de dithering opcional.

    Args:
        image_path (str): Ruta del archivo de la imagen a procesar.
        max_area (int): Área máxima permitida para la imagen redimensionada.
        light_correction_range (tuple): Rango para la corrección de niveles de luz.
        dithering_algorithm (str, optional): Algoritmo de dithering a aplicar ('floyd_steinberg' o None).

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
        grayscale_array = np.array(grayscale_image, dtype=np.float32)
        grayscale_corrected = exposure.rescale_intensity(grayscale_array, in_range="image", out_range=light_correction_range)
        # grayscale_corrected = np.clip(grayscale_array, light_correction_range[0], light_correction_range[1])

        # Aplicar dithering si se especifica
        if dithering_algorithm == 'floyd_steinberg':
            # # invert before dithering
            # grayscale_corrected = 255 - grayscale_corrected

            dithered_array = apply_floyd_steinberg_dithering(grayscale_corrected.copy())
            processed_image = Image.fromarray(dithered_array.astype(np.uint8))
        else:
            banded_image = ((grayscale_corrected // 32) * 32).astype(np.uint8)
            processed_image = Image.fromarray(banded_image)

        params = {
            "max_area": max_area,
            "light_correction_range": light_correction_range,
            "dithering_algorithm": dithering_algorithm
        }

        hash_value = generate_hash(processed_image, params)

        metadata = {
            "original_size": (original_width, original_height),
            "resized_size": (new_width, new_height),
            "original_pixel_count": original_width * original_height,
            "resized_pixel_count": new_width * new_height,
            "filter_steps": ["grayscale", "level correction", "banding"],
            "dithering_algorithm": dithering_algorithm,
            "hash": hash_value
        }

        if dithering_algorithm:
            metadata["filter_steps"].append(dithering_algorithm)

        return FilterResult(original_image, processed_image.convert("RGB"), metadata)

    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        raise ValueError(f"No se pudo procesar la imagen: {e}")
