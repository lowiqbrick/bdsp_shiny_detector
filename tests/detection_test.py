import cv2
import copy
import time
import pytest
import numpy as np

import utils
import specific_pokemon


def test_image_part_equal():
    mewtwo_reference = cv2.imread("selected_references/palkia_appears.png")
    assert mewtwo_reference is not None
    comp_area = utils.Rectangle(utils.Point(50, 50), utils.Point(400, 400))
    assert utils.is_image_part_equal(mewtwo_reference, mewtwo_reference, comp_area)


def test_image_part_equal_false():
    mewtwo_reference = cv2.imread("selected_references/palkia_appears.png")
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


def test_palkia_appearing():
    search_engine = specific_pokemon.PokemonSearchEngine()
    palkia_appearance = cv2.imread("selected_references/palkia_appears.png")
    assert palkia_appearance is not None
    assert search_engine.is_palkia_appearing(palkia_appearance)


def test_palkia_appearing_false():
    search_engine = specific_pokemon.PokemonSearchEngine()
    black_image = np.zeros((1080, 1920, 3))
    assert not search_engine.is_palkia_appearing(black_image)


def test_is_menu_present():
    search_engine = specific_pokemon.PokemonSearchEngine()
    fight_menu_reference = cv2.imread("selected_references/menu_present.png")
    assert fight_menu_reference is not None
    assert search_engine.is_menu_present(fight_menu_reference)


def test_is_menu_present_false():
    search_engine = specific_pokemon.PokemonSearchEngine()
    black_image = np.zeros((1080, 1920, 3))
    assert not search_engine.is_menu_present(black_image)


def search_engine():
    search_engine = specific_pokemon.PokemonSearchEngine()
    palkia_appearance = cv2.imread("selected_references/palkia_appears.png")
    menu_present = cv2.imread("selected_references/menu_present.png")
    black_image = np.zeros((1080, 1920, 3))
    assert palkia_appearance is not None
    assert menu_present is not None

    for _ in range(0, 4):
        assert not search_engine.is_menu_late(black_image)
        time.sleep(0.5)
        assert not search_engine.is_menu_late(palkia_appearance)
        time.sleep(0.5)
        assert not search_engine.is_menu_late(black_image)
        time.sleep(0.5)
        assert not search_engine.is_menu_late(menu_present)
        time.sleep(0.5)

    assert search_engine.duration_appear_to_menu == pytest.approx(0.5, abs=0.01)


def search_engine_irregular():
    search_engine = specific_pokemon.PokemonSearchEngine()
    palkia_appearance = cv2.imread("selected_references/palkia_appears.png")
    menu_present = cv2.imread("selected_references/menu_present.png")
    black_image = np.zeros((1080, 1920, 3))
    assert palkia_appearance is not None
    assert menu_present is not None

    for _ in range(0, 4):
        assert not search_engine.is_menu_late(black_image)
        time.sleep(0.5)
        assert not search_engine.is_menu_late(palkia_appearance)
        time.sleep(0.5)
        assert not search_engine.is_menu_late(black_image)
        time.sleep(0.5)
        assert not search_engine.is_menu_late(menu_present)
        time.sleep(0.5)

    assert not search_engine.is_menu_late(black_image)
    time.sleep(0.5)
    assert not search_engine.is_menu_late(palkia_appearance)
    time.sleep(0.5)
    assert not search_engine.is_menu_late(black_image)
    time.sleep(search_engine.MENU_TIMEOUT + 0.5)
    assert search_engine.is_menu_late(menu_present)
