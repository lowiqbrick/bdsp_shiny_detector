from references.cleanup import pixels_close, PIXEL_CLOSE_THRESHOLD


def test_pixels_close():
    pixel1 = [100, 90, 80]
    pixel2 = [102, 87, 76]
    assert pixels_close(pixel1, pixel2)


def test_pixels_close_false():
    pixel1 = [100, 90, 80]
    pixel2 = [102, 87, 80 + PIXEL_CLOSE_THRESHOLD]
    assert not pixels_close(pixel1, pixel2)
