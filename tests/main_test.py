import main
import utils
import specific_pokemon
import pytest
import cv2
from gpiozero import LED, Device
from gpiozero.pins.mock import MockFactory
import time
import numpy as np

Device.pin_factory = MockFactory()


def main_iteration(
    image: cv2.typing.MatLike,
    controller: LED,
    loop_structs: utils.LoopStructs,
    loop_variables: utils.LoopVariables,
):
    start_time = time.time()
    is_detected = main.image_processing(image, controller, loop_structs, loop_variables)
    main.loop_update(is_detected, start_time, image, loop_structs, loop_variables)


def main_cycle(
    list_timings: list[float],
    black_image: cv2.typing.MatLike,
    appear_image: cv2.typing.MatLike,
    menu_image: cv2.typing.MatLike,
    controller: LED,
    loop_structs: utils.LoopStructs,
    loop_variables: utils.LoopVariables,
):
    assert len(list_timings) == 4

    # load game; nothing to detect
    main_iteration(black_image, controller, loop_structs, loop_variables)
    time.sleep(list_timings[0])
    # pokemon appears
    main_iteration(appear_image, controller, loop_structs, loop_variables)
    time.sleep(list_timings[1])
    assert (
        loop_structs.search_engine.state == specific_pokemon.SearchEngineState.APPEARING
    )
    # time between appearance and menu
    main_iteration(black_image, controller, loop_structs, loop_variables)
    time.sleep(list_timings[2])
    assert (
        loop_structs.search_engine.state
        == specific_pokemon.SearchEngineState.POKEMON_SEND_OUT
    )
    # menu shows up
    main_iteration(menu_image, controller, loop_structs, loop_variables)
    time.sleep(list_timings[3])
    assert loop_structs.search_engine.state == specific_pokemon.SearchEngineState.MENU


def test_regular():
    appear_image = cv2.imread("selected_references/palkia_appears.png")
    menu_image = cv2.imread("selected_references/menu_present.png")
    assert appear_image is not None
    assert menu_image is not None
    black_image = np.zeros((1080, 1920, 3))
    loop_structs = utils.LoopStructs()
    loop_variables = utils.LoopVariables()
    controller = LED(21)
    regular_timing = [0.5, 0.5, 0.5, 0.5]

    # get through startup process
    main_cycle(
        regular_timing,
        black_image,
        appear_image,
        menu_image,
        controller,
        loop_structs,
        loop_variables,
    )

    for _ in range(0, 3):
        main_cycle(
            regular_timing,
            black_image,
            appear_image,
            menu_image,
            controller,
            loop_structs,
            loop_variables,
        )

    # do one more black image to count the last for-loop iteration
    start_time = time.time()
    is_detected = main.image_processing(
        black_image, controller, loop_structs, loop_variables
    )
    main.loop_update(is_detected, start_time, black_image, loop_structs, loop_variables)

    assert loop_variables.period_length_last_loop == pytest.approx(expected=2, rel=0.1)
    assert loop_variables.reset_counter == 4


def test_fail_on_no_menu():
    # expect an exception to be raised
    with pytest.raises(utils.MenuTimeout):
        appear_image = cv2.imread("selected_references/palkia_appears.png")
        menu_image = cv2.imread("selected_references/menu_present.png")
        assert appear_image is not None
        assert menu_image is not None
        black_image = np.zeros((1080, 1920, 3))
        loop_structs = utils.LoopStructs()
        loop_variables = utils.LoopVariables()
        controller = LED(21)
        regular_timing = [0.5, 0.5, 0.5, 0.5]
        shiny_timing = [0.5, 0.5, loop_structs.search_engine.MENU_TIMEOUT + 0.6, 0.5]

        # get through startup process
        main_cycle(
            regular_timing,
            black_image,
            appear_image,
            menu_image,
            controller,
            loop_structs,
            loop_variables,
        )

        # one regular cycle
        main_cycle(
            regular_timing,
            black_image,
            appear_image,
            menu_image,
            controller,
            loop_structs,
            loop_variables,
        )

        # give black image in timeout to simulate shiny
        main_cycle(
            shiny_timing,
            black_image,
            appear_image,
            black_image,
            controller,
            loop_structs,
            loop_variables,
        )


def test_fail_on_too_long_cycle():
    # expect an exception to be raised
    with pytest.raises(utils.NoMenuAppeared):
        appear_image = cv2.imread("selected_references/palkia_appears.png")
        menu_image = cv2.imread("selected_references/menu_present.png")
        assert appear_image is not None
        assert menu_image is not None
        black_image = np.zeros((1080, 1920, 3))
        loop_structs = utils.LoopStructs()
        loop_variables = utils.LoopVariables()
        controller = LED(21)
        regular_timing = [0.5, 0.5, 0.5, 0.5]

        # get through startup process
        main_cycle(
            regular_timing,
            black_image,
            appear_image,
            menu_image,
            controller,
            loop_structs,
            loop_variables,
        )

        for _ in range(0, 3):
            main_cycle(
                regular_timing,
                black_image,
                appear_image,
                menu_image,
                controller,
                loop_structs,
                loop_variables,
            )

        macro_duration = loop_structs.macro_duration.get_duration()
        assert macro_duration is not None
        time.sleep(10)
        macro_duration = loop_structs.macro_duration.get_duration()
        assert macro_duration is not None
        menu_timeout_timing = [
            0.5,
            macro_duration * loop_structs.period_timer.get_timeout_factor(),
            0.5,
            0.5,
        ]

        # menu should come in too late
        main_cycle(
            menu_timeout_timing,
            black_image,
            appear_image,
            menu_image,
            controller,
            loop_structs,
            loop_variables,
        )


if __name__ == "__main__":
    pass
