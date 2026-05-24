import cv2
import time
from gpiozero import LED

SAVED_FRAMES_PER_SECOND = 4

if __name__ == "__main__":
    # start controller pin
    controller = LED(21)

    # get video source (0: switch 2; 1: pc webcam)
    cap = cv2.VideoCapture(0)

    # set limits for capture of switch 2
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    save_folder = "references/"
    frame_counter = 0

    # display captured images
    while True:
        # capture frame
        success, frame = cap.read()

        if not success:
            print("video could not be read")
            cap.release()
            cv2.destroyAllWindows()
            break
        else:
            # save frame
            cv2.imwrite(save_folder + "reference_" + str(frame_counter) + ".png", frame)
            cv2.waitKey(1)
            frame_counter += 1
            time.sleep(1 / SAVED_FRAMES_PER_SECOND)
