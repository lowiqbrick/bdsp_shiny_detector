import cv2
import os
import sms
import utils
import specific_pokemon
import time
import datetime
import subprocess
import numpy as np


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, top_left: Point, bottom_right: Point):
        assert top_left.x < bottom_right.x
        assert top_left.y < bottom_right.y
        self.top_left = top_left
        self.bottom_right = bottom_right

    def is_point_in_rectangle(self, point: Point) -> bool:
        if (
            self.top_left.x <= point.x
            and self.top_left.y <= point.y
            and self.bottom_right.x > point.x
            and self.bottom_right.y > point.y
        ):
            return True
        return False

    def is_point_outside_rectangle(self, point: Point) -> bool:
        return not self.is_point_in_rectangle(point)


def opponent_stat_rec():
    # returns rectangle with the opponents status
    return Rectangle(Point(300, 130), Point(840, 260))


def opponent_pokemon():
    # returns rectangle with the opponents pokemon sprite
    return Rectangle(Point(1150, 80), Point(1550, 450))


def is_image_part_equal(
    reference_image: cv2.typing.MatLike,
    captured_image: cv2.typing.MatLike,
    comparison_area: Rectangle,
    threshold: int = 5,
    min_match_ratio: float = 0.95,
) -> bool:
    "compares part of two images specified in the comparison area on a pixel basis"

    x1, x2 = (int(comparison_area.top_left.x), int(comparison_area.bottom_right.x))
    y1, y2 = (int(comparison_area.top_left.y), int(comparison_area.bottom_right.y))

    reference_pixels = reference_image[y1:y2:2, x1:x2:2].astype(np.int16)
    captured_pixels = captured_image[y1:y2:2, x1:x2:2].astype(np.int16)

    differences = np.abs(reference_pixels - captured_pixels)
    # Calculate what percentage of color elements are within the threshold
    matches = np.sum(differences <= threshold)
    match_ratio = matches / differences.size
    return bool(match_ratio >= min_match_ratio)


def get_difference_percentage(
    reference_image: cv2.typing.MatLike,
    captured_image: cv2.typing.MatLike,
    comparison_area: Rectangle,
    threshold: int = 5,
) -> float:
    """Calculates what percentage of pixels in a region differ significantly."""
    x1, x2 = (int(comparison_area.top_left.x), int(comparison_area.bottom_right.x))
    y1, y2 = (int(comparison_area.top_left.y), int(comparison_area.bottom_right.y))

    ref_part = reference_image[y1:y2:2, x1:x2:2].astype(np.int16)
    cap_part = captured_image[y1:y2:2, x1:x2:2].astype(np.int16)

    # Find pixels where the difference is greater than the threshold
    diff = np.abs(ref_part - cap_part)
    # Check if ANY of the 3 color channels (BGR) differ
    mask = np.any(diff > threshold, axis=2)
    return float((np.sum(mask) / mask.size) * 100)


def is_status_menu_equal(
    reference_image: cv2.typing.MatLike,
    captured_image: cv2.typing.MatLike,
) -> bool:
    return is_image_part_equal(reference_image, captured_image, opponent_stat_rec())


def is_pokemon_equal(
    reference_image: cv2.typing.MatLike,
    captured_image: cv2.typing.MatLike,
) -> bool:
    return is_image_part_equal(reference_image, captured_image, opponent_pokemon())


def save_shiny(image: cv2.typing.MatLike):
    if "PYTEST_CURRENT_TEST" not in os.environ:
        date_time = datetime.datetime.now()
        cv2.imwrite(
            "references/suspected_shiny_"
            + str(date_time.year)
            + "_"
            + str(date_time.month)
            + "_"
            + str(date_time.day)
            + "_"
            + str(date_time.hour)
            + "_"
            + str(date_time.minute)
            + "_"
            + str(date_time.second)
            + ".png",
            image,
        )


class FPSAverager:
    def __init__(self, size_limit: int):
        self.__max_size = size_limit
        self.__current_index = 0
        self.frame_list = []
        for _ in range(0, size_limit):
            self.frame_list.append(0)

    def insert_new_value(self, value: float):
        self.frame_list[self.__current_index] = value
        self.__current_index = (self.__current_index + 1) % self.__max_size

    def get_fps(self) -> float:
        assert len(self.frame_list) == self.__max_size
        return round(sum(self.frame_list) / len(self.frame_list), 1)


class LoopReporter:
    def __init__(self):
        self.__reset()

    def add_printout(self, text: str):
        self.__printout += text

    def print(self) -> str:
        terminal_columns = os.get_terminal_size().columns
        if len(self.__printout) > terminal_columns:
            self.__printout = self.__printout[:terminal_columns]
        elif len(self.__printout) < terminal_columns:
            self.__printout = self.__printout + " " * (
                terminal_columns - len(self.__printout)
            )
        printout = self.__printout + "\r"
        self.__reset()
        return printout

    def __reset(self):
        self.__printout = ""


def period_to_str(period: float) -> str:
    period_string = str(round(period, 2))
    if len(period_string) < 5:
        period_string = period_string + ((5 - len(period_string)) * " ")
    return period_string


class PeriodImager:
    def __init__(self):
        self.__image_taken = False

    def save_encounter(self, image: cv2.typing.MatLike):
        if "PYTEST_CURRENT_TEST" not in os.environ:
            date_time = datetime.datetime.now()
            cv2.imwrite(
                "references/encounter_"
                + str(date_time.year)
                + "_"
                + str(date_time.month)
                + "_"
                + str(date_time.day)
                + "_"
                + str(date_time.hour)
                + "_"
                + str(date_time.minute)
                + "_"
                + str(date_time.second)
                + "_"
                + str(date_time.microsecond)
                + ".png",
                image,
            )

    def take_image(
        self,
        time_since_last_period: float,
        frame: cv2.typing.MatLike,
        time_for_shiny: float,
    ):
        if (time_since_last_period) >= time_for_shiny and not self.__image_taken:
            self.save_encounter(frame)
            self.__image_taken = True

    def reset(self, reset_counter: int):
        if (
            not self.__image_taken
            and reset_counter > 2
            and ("PYTEST_CURRENT_TEST" not in os.environ)
        ):
            print("\nmewtwo image not taken in cycle " + str(datetime.datetime.now()))
        self.__image_taken = False
        if (reset_counter % 5) == 0:
            # Run cleanup as a background process to avoid blocking the main detection loop
            # This prevents "hiccups" in the timing method
            subprocess.Popen(["python3", "references/cleanup.py"])


class PeriodTime:
    def __init__(self) -> None:
        self.period_time = time.time() + 300

    def get_passed_time(self) -> float:
        return time.time() - self.period_time

    def preemptive_check(self, is_detected: bool, is_last_detected: bool):
        if not is_detected and is_last_detected:
            self.reset()

    def is_pokemon_present(self, time_for_shiny: float) -> bool:
        return self.get_passed_time() >= time_for_shiny

    def reset(self):
        self.period_time = time.time()


class MacroDuration:
    def __init__(self):
        self._old_weight = 0.9
        self._new_weight = 1 - self._old_weight
        self._duration = None
        self._time_for_shiny_offset = 0.75

    def update(self, new_duration: float):
        if new_duration <= 0:
            return

        if self._duration is None:
            self._duration = new_duration
        else:
            self._duration = (self._duration * self._old_weight) + (
                new_duration * self._new_weight
            )

    def time_for_shiny(self) -> float:
        # return high value to prevent false alarms
        if self._duration is None or self._duration <= self._time_for_shiny_offset:
            return 300
        return self._duration - self._time_for_shiny_offset

    def should_shiny_be_present(self) -> bool:
        if self._duration is None:
            return False
        return self._duration >= self.time_for_shiny()

    def get_duration_str(self) -> str:
        if self._duration is None:
            return "None"
        else:
            return str(round(self._duration, 2)) + "s"


class LoopStructs:
    def __init__(self):
        # load all reference images
        self.search_engine = specific_pokemon.PokemonSearchEngine()
        # averaging pfs values
        self.fps_averager = utils.FPSAverager(60)
        # status printer
        self.logger = utils.LoopReporter()
        # sms notification (not mandatory)
        self.sender = sms.SMSSender()
        # keep time of the current period
        self.period_timer = utils.PeriodTime()
        # take an image every period
        self.period_imager = utils.PeriodImager()
        # adjust the macro duration dynamically
        self.macro_duration = utils.MacroDuration()


class LoopVariables:
    def __init__(self):
        self.is_last_detected: bool = False
        self.last_image: cv2.typing.MatLike | None = None
        self.reset_counter: int = 0
        self.period_length_last_loop: float = -300.0


class NoNewMewtwoException(Exception):
    def __init__(self):
        self.message = "the loop didn't detect a normal mewtwo after the timeout passed"
        super().__init__(self.message)


if __name__ == "__main__":
    pass
