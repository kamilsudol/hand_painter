from mediapipe.python.solutions.hands import Hands, HAND_CONNECTIONS
from mediapipe.python.solutions.drawing_utils import draw_landmarks
from lib.gestures.gesture_resolver import gesture_resolver
from PyQt5.QtWidgets import QApplication, QWidget
from lib.gestures.hand_on_change_event import HandOnChangeEvent
from lib.gestures.hand_position_resolver import get_hand_position
from cv2 import VideoCapture, imshow, flip, cvtColor, waitKey, destroyWindow, circle, COLOR_BGR2RGB, COLOR_RGB2BGR, \
    FILLED

window_width = 0
window_height = 0


def update_window_size(window: QWidget):
    """
    Function, which is necessary to valid work of camera_capture function.
    :param window - Main GUI
    """
    global window_width
    window_width = window.size().width()
    global window_height
    window_height = window.size().height()


def camera_capture(window: QWidget):
    """
    Function, which is responsible for detecting hand gestures on user's camera
    and if so, then it emits proper event signal to the main GUI.
    :param window - Main GUI
    """
    captured_image = VideoCapture(0)  # Zero means default camera usage.
    captured_image.set(3, 1280)
    captured_image.set(4, 720)
    x = 0.
    y = 0.
    with Hands(min_detection_confidence=0.5) as hands:
        while captured_image.isOpened():
            success, image = captured_image.read()
            if not success:
                continue

            image = cvtColor(image, COLOR_BGR2RGB)
            # image = flip(image, 3)
            image.flags.writeable = False
            hand_processing_results = hands.process(image)
            image = cvtColor(image, COLOR_RGB2BGR)

            if hand_processing_results.multi_hand_landmarks:
                for hand_landmarks in hand_processing_results.multi_hand_landmarks:
                    current_gesture = gesture_resolver(hand_landmarks)
                    x, y = get_hand_position(current_gesture, hand_landmarks)
                    event = HandOnChangeEvent(x, y, window_width, window_height, current_gesture, True)
                    circle(image, (int(captured_image.get(3) * x), int(captured_image.get(4) * y)), 15, (0, 255, 0), FILLED)
                    draw_landmarks(image, hand_landmarks, HAND_CONNECTIONS)
            else:
                event = HandOnChangeEvent(x, y, window_width, window_height, "UNKNOWN", False)
            QApplication.sendEvent(window, event)
            # imshow('Hands Capturing', image)
            if waitKey(5) & 0xFF == 27:
                destroyWindow('Hands Capturing')
                break
    captured_image.release()
