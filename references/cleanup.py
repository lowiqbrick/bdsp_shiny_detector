import os
import cv2

from utils import Point
from specific_pokemon import PokemonSearchEngine

PIXEL_CLOSE_THRESHOLD = 10
PIXEL_CLOSE_PERCENTAGE = 0.9


def pixels_close(
    pixel1: list[int],
    pixel2: list[int],
) -> bool:
    assert len(pixel1) == 3
    assert len(pixel1) == len(pixel2)
    return all(
        abs(int(p1) - int(p2)) < PIXEL_CLOSE_THRESHOLD for p1, p2 in zip(pixel1, pixel2)
    )


def pixel_coordinates_of_comparison_area() -> list[Point]:
    point_list = []
    for x in range(1100, 1650, 100):
        for y in range(400, 750, 100):
            point_list.append(Point(x, y))
    return point_list


def get_comp_pixels(
    pixel_coordinates: list[Point], image: cv2.typing.MatLike
) -> list[list[int]]:
    pixels = []
    for coordinate in pixel_coordinates:
        pixels.append(image[int(coordinate.y)][int(coordinate.x)])
    return pixels


def are_pixels_close(pixels1: list[list[int]], pixels2: list[list[int]]) -> bool:
    assert len(pixels1) == len(pixels2)

    len_pixels = len(pixels1)
    count = 0

    for pixel1, pixel2 in zip(pixels1, pixels2):
        if pixels_close(pixel1, pixel2):
            count += 1
    return (float(count) / float(len_pixels)) >= PIXEL_CLOSE_PERCENTAGE


if __name__ == "__main__":
    search_engine = PokemonSearchEngine()
    assert search_engine.giratina_menu_reference is not None
    comparison_pixel_positions = pixel_coordinates_of_comparison_area()

    # Use absolute path relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    reference_folder = script_dir + "/"

    processed_pixels = [
        get_comp_pixels(
            comparison_pixel_positions, search_engine.giratina_menu_reference
        )
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

        current_pixel = get_comp_pixels(comparison_pixel_positions, image)

        if any(are_pixels_close(pixel, current_pixel) for pixel in processed_pixels):
            os.remove(filepath)
            deleted_images += 1
        else:
            processed_pixels.append(current_pixel)

    # print(f"Deleted {deleted_images} duplicate images.")
