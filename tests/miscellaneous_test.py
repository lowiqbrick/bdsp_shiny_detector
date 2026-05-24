import cv2
import utils


def test_period_to_string_length():
    assert len(utils.period_to_str(12.12)) == 5
    assert len(utils.period_to_str(12.1)) == 5
    assert len(utils.period_to_str(12)) == 5


def test_cv2_color_channels():
    """
    test image generated via:

    import cv2
    import numpy as np

    color_channel_test = np.zeros((1080, 1920, 3)) + 128

    for height_index in range(0, 1080):
        for width_index in range(0, 1920):
            if height_index <= 510 and width_index <= 990:
                color_channel_test[height_index][width_index][0] = 255
            if height_index > 510 and width_index < 990:
                color_channel_test[height_index][width_index][1] = 255
            if height_index < 510 and width_index > 990:
                color_channel_test[height_index][width_index][2] = 255
    cv2.imwrite("selected_references/color_channel_reference.png", color_channel_test)
    """

    test_image = cv2.imread("selected_references/color_channel_reference.png")
    assert test_image is not None

    # image dimensions (height, width, color dims) (1020, 1980, 3)
    # top left blue
    assert test_image[0][0][0] == 255
    # bottom left green
    assert test_image[1000][0][1] == 255
    # top right red
    assert test_image[0][1100][2] == 255
