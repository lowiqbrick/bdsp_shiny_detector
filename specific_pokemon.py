import cv2
import numpy as np
import utils


class PokemonSearchEngine:
    def __init__(self):
        self.mewtwo_reference = cv2.imread("selected_references/mewtwo_reference.png")
        assert self.mewtwo_reference is not None

    def is_mewtwo(self, captured_image: cv2.typing.MatLike) -> bool:
        assert self.mewtwo_reference is not None
        # Compare the status bar area to see if the pokemon is present
        diff_percent = utils.get_difference_percentage(
            self.mewtwo_reference, captured_image, utils.opponent_stat_rec()
        )

        return diff_percent < 1.5

    def is_mewtwo_normal(self, captured_image: cv2.typing.MatLike) -> bool:
        assert self.mewtwo_reference is not None

        # Compare the entire pokemon sprite area
        diff_percent = utils.get_difference_percentage(
            self.mewtwo_reference, captured_image, utils.opponent_pokemon()
        )

        return diff_percent < 1.5

    def is_mewtwo_shiny(self, captured_image: cv2.typing.MatLike) -> bool:
        assert self.mewtwo_reference is not None

        # Compare the entire pokemon sprite area
        diff_percent = utils.get_difference_percentage(
            self.mewtwo_reference, captured_image, utils.opponent_pokemon()
        )

        return diff_percent >= 1.5


if __name__ == "__main__":
    search_engine = PokemonSearchEngine()
    black_image = np.zeros((1020, 1980, 3))
    print(
        "does reference of mewtwo equal a black image: "
        + str(search_engine.is_mewtwo(black_image))
    )
    for index in range(6, 1):
        print(index)
