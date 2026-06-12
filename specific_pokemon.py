import cv2
import time
import utils
from enum import Enum


class SearchEngineState(Enum):
    UNINITIALIZED = 1
    RELOAD_GAME = 2
    APPEARING = 3
    POKEMON_SEND_OUT = 1
    MENU = 5


class PokemonSearchEngine:
    MENU_TIMEOUT = 1.0

    def __init__(self):
        self.palkia_appears_reference = cv2.imread(
            "selected_references/palkia_appears.png"
        )
        self.giratina_appearing_reference = cv2.imread(
            "selected_references/giratina_appears.png"
        )
        self.giratina_menu_reference = cv2.imread(
            "selected_references/giratina_menu.png"
        )
        self.is_menu_present_reference = cv2.imread(
            "selected_references/menu_present.png"
        )
        self.state = SearchEngineState.UNINITIALIZED
        self.current_duration_start = None
        self.duration_appear_to_menu = None
        assert self.palkia_appears_reference is not None
        assert self.giratina_appearing_reference is not None
        assert self.giratina_menu_reference is not None
        assert self.is_menu_present_reference is not None

    def is_palkia_appearing(self, captured_image: cv2.typing.MatLike) -> bool:
        assert self.palkia_appears_reference is not None
        # Compare the status bar area to see if the pokemon is present
        diff_percent = utils.get_difference_percentage(
            self.palkia_appears_reference, captured_image, utils.appearing_textbox()
        )

        return diff_percent < 1.5

    def is_giratina_appearing(self, captured_image: cv2.typing.MatLike) -> bool:
        assert self.giratina_appearing_reference is not None
        # Compare the status bar area to see if the pokemon is present
        diff_percent = utils.get_difference_percentage(
            self.giratina_appearing_reference, captured_image, utils.appearing_textbox()
        )

        return diff_percent < 1.5

    def get_giratina_ref_pixel(self, captured_image: cv2.typing.MatLike) -> list[int]:
        reference_pixel_coordinate = utils.Point(x=1330, y=400)
        return captured_image[int(reference_pixel_coordinate.y)][
            int(reference_pixel_coordinate.x)
        ]

    def is_menu_present(self, captured_image: cv2.typing.MatLike) -> bool:
        assert self.is_menu_present_reference is not None

        # Compare the entire pokemon sprite area
        diff_percent = utils.get_difference_percentage(
            self.is_menu_present_reference, captured_image, utils.fight_menu()
        )

        return diff_percent < 1.5

    def update_state(self, frame: cv2.typing.MatLike):
        is_appearing = self.is_giratina_appearing(frame) or self.is_palkia_appearing(
            frame
        )
        is_menu_present = self.is_menu_present(frame)
        if is_appearing:
            self.state = SearchEngineState.APPEARING
        elif is_menu_present:
            self.state = SearchEngineState.MENU
        # only change to nothing detected after certain detection
        # to prevent startup problems
        elif self.state != SearchEngineState.UNINITIALIZED:
            if (
                self.state == SearchEngineState.APPEARING
                and not is_appearing
                and not is_menu_present
            ):
                self.state = SearchEngineState.POKEMON_SEND_OUT
            elif (
                self.state == SearchEngineState.MENU
                and not is_appearing
                and not is_menu_present
            ):
                self.state = SearchEngineState.RELOAD_GAME

    def update_current_duration_timer(self, last_state: SearchEngineState):
        # reset/start duration timer
        # on disappearing textbox
        if (
            last_state == SearchEngineState.APPEARING
            and self.state == SearchEngineState.POKEMON_SEND_OUT
        ):
            self.current_duration_start = time.time()

    def is_menu_present_late(self, current_duration: float) -> bool:
        if self.duration_appear_to_menu is None:
            return False

        return self.duration_appear_to_menu + self.MENU_TIMEOUT < current_duration

    def ran_in_menu_timeout(self, last_state: SearchEngineState) -> bool:
        if self.current_duration_start is None:
            return False

        # save/compare timer on menu detection
        # on previous cycle
        current_duration = time.time() - self.current_duration_start

        # initialise the duration until menu
        if (
            self.duration_appear_to_menu is None
            and self.state == SearchEngineState.MENU
        ):
            self.duration_appear_to_menu = current_duration

        if (
            self.state == SearchEngineState.POKEMON_SEND_OUT
            and self.duration_appear_to_menu is not None
        ):
            if self.current_duration_start is not None:
                # reference time saved
                if self.is_menu_present_late(current_duration):
                    return True
        return False

    def is_menu_late(self, frame: cv2.typing.MatLike) -> bool:
        """
        This function processes a frame to calculate the time between
        the message that the pokemon appears and the fight menu presence.

        If a shiny pokemon appeared a small visual effect occurs that delays
        the appearance. If the current duration is significantly longer
        than the last a shiny is assumed to be present.

        Returns:
            bool: True if current duration is significantly longer than the last
        """
        last_state = self.state
        self.update_state(frame)

        self.update_current_duration_timer(last_state)

        if self.current_duration_start is None:
            return False

        if self.ran_in_menu_timeout(last_state):
            return True
        else:
            return False


if __name__ == "__main__":
    pass
