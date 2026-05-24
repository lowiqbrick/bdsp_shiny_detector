import cv2
import copy
import time
import numpy as np

import utils
import specific_pokemon


def test_image_part_equal():
    mewtwo_reference = cv2.imread("selected_references/mewtwo_reference.png")
    assert mewtwo_reference is not None
    comp_area = utils.Rectangle(utils.Point(50, 50), utils.Point(400, 400))
    assert utils.is_image_part_equal(mewtwo_reference, mewtwo_reference, comp_area)


def test_image_part_equal_false():
    mewtwo_reference = cv2.imread("selected_references/mewtwo_reference.png")
    assert mewtwo_reference is not None
    mewtwo_reference_changed = copy.deepcopy(mewtwo_reference)
    # over write large chunk
    for index_y in range(50, 301):
        for index_x in range(50, 301):
            mewtwo_reference_changed[index_x][index_y][0] = 255
            mewtwo_reference_changed[index_x][index_y][1] = 255
            mewtwo_reference_changed[index_x][index_y][2] = 255
    comp_area = utils.Rectangle(utils.Point(50, 50), utils.Point(400, 400))
    assert not utils.is_image_part_equal(
        mewtwo_reference, mewtwo_reference_changed, comp_area
    )


def test_is_mewtwo():
    search_engine = specific_pokemon.PokemonSearchEngine()
    mewtwo_reference = cv2.imread("selected_references/mewtwo_reference.png")
    assert mewtwo_reference is not None
    assert search_engine.is_mewtwo(mewtwo_reference)


def test_is_mewtwo_false():
    search_engine = specific_pokemon.PokemonSearchEngine()
    black_image = np.zeros((1080, 1920, 3))
    assert not search_engine.is_mewtwo(black_image)


def test_is_mewtwo_during_send_out():
    search_engine = specific_pokemon.PokemonSearchEngine()
    send_out_reference = cv2.imread("selected_references/send_out.png")
    assert send_out_reference is not None
    assert search_engine.is_mewtwo(send_out_reference)
    assert search_engine.is_mewtwo_shiny(send_out_reference)


def test_is_mewtwo_normal():
    search_engine = specific_pokemon.PokemonSearchEngine()
    mewtwo_reference = cv2.imread("selected_references/mewtwo_reference.png")
    assert mewtwo_reference is not None
    assert search_engine.is_mewtwo_normal(mewtwo_reference)


def test_is_mewtwo_normal_false():
    search_engine = specific_pokemon.PokemonSearchEngine()
    black_image = np.zeros((1080, 1920, 3))
    assert not search_engine.is_mewtwo_normal(black_image)


def test_is_mewtwo_shiny():
    search_engine = specific_pokemon.PokemonSearchEngine()
    mewtwo_reference = cv2.imread("selected_references/mewtwo_reference.png")
    assert mewtwo_reference is not None
    # over write large chunk
    for index_y in range(1150, 1500):
        for index_x in range(80, 400):
            mewtwo_reference[index_x][index_y][0] = 255
            mewtwo_reference[index_x][index_y][1] = 255
            mewtwo_reference[index_x][index_y][2] = 255
    assert search_engine.is_mewtwo_shiny(mewtwo_reference)


def test_is_mewtwo_shiny_false():  # 1400 350
    search_engine = specific_pokemon.PokemonSearchEngine()
    mewtwo_reference = cv2.imread("selected_references/mewtwo_reference.png")
    assert mewtwo_reference is not None
    assert not search_engine.is_mewtwo_shiny(mewtwo_reference)


def test_is_pokemon_present():
    time_for_shiny = 0.25
    period_timer = utils.PeriodTime()
    period_timer.reset()
    assert period_timer.get_passed_time() < 0.01
    time.sleep(time_for_shiny - 0.125)
    assert not period_timer.is_pokemon_present(time_for_shiny)
    time.sleep(0.5)
    assert period_timer.is_pokemon_present(time_for_shiny)
