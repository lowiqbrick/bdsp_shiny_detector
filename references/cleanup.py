import os
import cv2
from specific_pokemon import PokemonSearchEngine

PIXEL_CLOSE_THRESHOLD = 5


def pixels_close(
    pixel1: list[int],
    pixel2: list[int],
) -> bool:
    assert len(pixel1) == 3
    assert len(pixel1) == len(pixel2)
    return all(abs(p1 - p2) < PIXEL_CLOSE_THRESHOLD for p1, p2 in zip(pixel1, pixel2))


if __name__ == "__main__":
    search_engine = PokemonSearchEngine()
    assert search_engine.giratina_menu_reference is not None

    # Use absolute path relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    reference_folder = script_dir + "/"

    processed_pixels = [
        search_engine.get_giratina_ref_pixel(search_engine.giratina_menu_reference)
    ]
    deleted_images = 0

    for filename in os.listdir(reference_folder):
        if (
            filename == "cleanup.py"
            or filename.startswith(".")
            or filename.endswith(".py")
        ):
            continue

        filepath = reference_folder + filename

        if not os.path.isfile(filepath):
            continue

        image = cv2.imread(filepath)

        # Handle non-image files or corrupted captures gracefully
        if image is None:
            continue

        current_pixel = search_engine.get_giratina_ref_pixel(image)

        if any(pixels_close(pixel, current_pixel) for pixel in processed_pixels):
            os.remove(filepath)
            deleted_images += 1
        else:
            processed_pixels.append(search_engine.get_giratina_ref_pixel(image))

    # print(f"Deleted {deleted_images} duplicate images.")
