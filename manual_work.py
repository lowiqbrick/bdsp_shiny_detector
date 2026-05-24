import cv2
import utils
import numpy as np


def black_image_part(
    image: cv2.typing.MatLike, visible_area: utils.Rectangle
) -> cv2.typing.MatLike:
    """
    this function is for finding out,
    what rectangle values correspond to what area in the captured images
    and isn't used for anything more than debugging

    pokemon: approx. Rectangle(Point(1150, 80), Point(1550, 450))

    opponent status bar: approx. Rectangle(Point(300, 130), Point(840, 260))

    fight menu: approx. Rectangle(Point(975, 760), Point(1920, 1080))
    """
    height, width, _ = image.shape

    for height_index in range(0, height):
        for width_index in range(0, width):
            if visible_area.is_point_outside_rectangle(
                utils.Point(width_index, height_index)
            ):
                image[height_index][width_index][0] = 0
                image[height_index][width_index][1] = 0
                image[height_index][width_index][2] = 0

    return image


def show_pixel_in_image(
    image: cv2.typing.MatLike, pixel: utils.Point, *args: int
) -> cv2.typing.MatLike:
    grid = 0
    for arg in args:
        grid = arg

    height, width = image.shape[:2]

    # get pixel
    assert pixel.x <= width
    assert pixel.y <= height
    channel1, channel2, channel3 = (
        image[int(pixel.y)][pixel.x][0],
        image[int(pixel.y)][pixel.x][1],
        image[int(pixel.y)][pixel.x][2],
    )

    for height_index in range(0, height):
        for width_index in range(0, width):
            if height_index == pixel.y or width_index == pixel.x:
                image[height_index][width_index][0] = 255
                image[height_index][width_index][1] = 255
                image[height_index][width_index][2] = 255
            elif (
                # grid enabled
                grid != 0
                # not at the left or top of the image
                and (height_index != 0 and width_index != 0)
                # condition for the grid
                and ((height_index % grid) == 0 or (width_index % grid) == 0)
            ):
                image[height_index][width_index][0] = 122
                image[height_index][width_index][1] = 122
                image[height_index][width_index][2] = 122
            else:
                image[height_index][width_index][0] = (
                    image[height_index][width_index][0] / 2 + channel1 / 2
                )
                image[height_index][width_index][1] = (
                    image[height_index][width_index][1] / 2 + channel2 / 2
                )
                image[height_index][width_index][2] = (
                    image[height_index][width_index][2] / 2 + channel3 / 2
                )

    print(
        f"channel 1 (blue): {channel1}; channel 2 (green): {channel2}; channel 3 (red): {channel3}"
    )

    return image


def gray_comparison_image(
    img1: cv2.typing.MatLike, img2: cv2.typing.MatLike
) -> cv2.typing.MatLike:
    """
    images must be imported as gray scale images:
    cv2.imread("image_name.png", cv2.IMREAD_GRAYSCALE)
    """
    # Convert to signed type to avoid uint8 wraparound
    a = img1.astype(np.int16)
    b = img2.astype(np.int16)

    # Signed difference centered at gray (128)
    diff = b - a + 128

    # Clamp to valid image range
    diff = np.clip(diff, 0, 255).astype(np.uint8)

    return diff


if __name__ == "__main__":
    mewtwo_reference = cv2.imread(
        "selected_references/mewtwo_reference.png", cv2.IMREAD_GRAYSCALE
    )
    color_channel_reference = cv2.imread(
        "selected_references/color_channel_reference.png", cv2.IMREAD_GRAYSCALE
    )
    assert mewtwo_reference is not None
    assert color_channel_reference is not None

    cv2.imshow(
        "pixel example",
        gray_comparison_image(mewtwo_reference, color_channel_reference),
    )
    cv2.waitKey(1)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nprogram ended")

    cv2.destroyAllWindows()
