import cv2
import time
import datetime
import os
from gpiozero import LED

import utils


def main():
    # start controller pin
    controller = LED(21)

    # get video source (0: switch 2; 1: pc webcam)
    cap = cv2.VideoCapture(0)

    # set limits for capture of switch 2
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    loop_structs = utils.LoopStructs()
    loop_variables = utils.LoopVariables()

    print("started at " + str(datetime.datetime.now()))

    # display captured images
    while True:
        is_detected = False
        start_time = time.time()
        # capture frame
        success, frame = cap.read()

        if (not success) or (frame is None):
            loop_structs.logger.add_printout("no frame")
            cv2.destroyAllWindows()
        else:
            is_detected = image_processing(
                frame=frame,
                controller=controller,
                loop_structs=loop_structs,
                loop_variables=loop_variables,
            )

        loop_update(
            is_detected=is_detected,
            start_time=start_time,
            frame=frame,
            loop_structs=loop_structs,
            loop_variables=loop_variables,
        )


def image_processing(
    frame: cv2.typing.MatLike,
    controller: LED,
    loop_structs: utils.LoopStructs,
    loop_variables: utils.LoopVariables,
) -> bool:

    loop_structs.logger.add_printout("got frame;")
    # display frame
    if "PYTEST_CURRENT_TEST" not in os.environ:
        cv2.imshow("HDMI Video Capture", cv2.resize(src=frame, dsize=(1000, 500)))
        cv2.waitKey(1)

    loop_structs.logger.add_printout(
        " " + str(loop_variables.reset_counter) + " resets;"
    )
    loop_structs.logger.add_printout(
        " "
        + utils.period_to_str(round(loop_structs.period_timer.get_passed_time(), 2))
        + f"s period (av {loop_structs.macro_duration.get_duration_str()});"
    )
    loop_structs.logger.add_printout(f" state {loop_structs.search_engine.state.name};")

    is_detected = loop_structs.search_engine.is_menu_present(frame)

    if loop_structs.search_engine.is_menu_late(frame):
        handle_shiny_found(frame, controller, loop_structs)

    return is_detected


def handle_shiny_found(frame, controller, loop_structs):
    utils.save_shiny(frame)
    controller.on()
    loop_structs.logger.add_printout("shiny found omg !!!!11111eleven")
    if "PYTEST_CURRENT_TEST" not in os.environ:
        print(loop_structs.logger.print(), end="")

    date_time = str(datetime.datetime.now())
    try:
        loop_structs.sender.send("shiny suspected at " + str(date_time))
    except ConnectionError:
        print("\nfailed to send message")
    finally:
        raise utils.MenuTimeout()


def loop_update(
    is_detected: bool,
    start_time: float,
    frame: cv2.typing.MatLike,
    loop_structs: utils.LoopStructs,
    loop_variables: utils.LoopVariables,
):
    # fps calculation
    delta_time = time.time() - start_time
    if delta_time:
        loop_structs.fps_averager.insert_new_value(1 / delta_time)
        loop_structs.logger.add_printout(
            " fps: " + str(loop_structs.fps_averager.get_fps()) + ";"
        )
    if "PYTEST_CURRENT_TEST" not in os.environ:
        print(loop_structs.logger.print(), end="")
    loop_variables.period_length_last_loop = loop_structs.period_timer.get_passed_time()

    # take sample images
    loop_structs.period_imager.take_image(
        loop_structs.period_timer.get_passed_time(),
        frame,
        loop_structs.macro_duration.time_for_shiny(),
    )

    # update for next period
    if not is_detected and loop_variables.is_last_detected:
        loop_structs.macro_duration.update(loop_variables.period_length_last_loop)
        loop_variables.reset_counter += 1
        loop_structs.period_timer.reset()
        loop_structs.period_imager.reset(loop_variables.reset_counter)
        if loop_variables.last_image is not None:
            loop_structs.period_imager.save_encounter(loop_variables.last_image)

    loop_variables.is_last_detected = is_detected
    if frame is not None:
        loop_variables.last_image = frame


if __name__ == "__main__":
    try:
        main()
    except utils.MenuTimeout as e:
        print(f"\n{e.message}")
    except KeyboardInterrupt:
        print("\nmanual intervention")
    finally:
        print("\nprogram ended at " + str(datetime.datetime.now()))
