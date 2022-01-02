from typing import NamedTuple, Tuple
from mediapipe.framework.formats import landmark_pb2
from lib.gestures.gesture_dict import GESTURE_DICT


class HandPosition(NamedTuple):
    """
    Simple tuple class, which represents hand position and its displaying possibility.
    """
    x: int
    y: int
    visible: bool = True


def get_hand_position(gesture: str, hand_landmarks: landmark_pb2.NormalizedLandmarkList) -> Tuple[float, float]:
    """
    Function, which is returning the tuple, which contains current position of the detected hand.
    :param gesture: Detected hand gesture.
    :param hand_landmarks: Hand gesture structure.
    :return: Tuple of a hand position coordinates.
    """
    return GESTURE_DICT[gesture]['hand_position_function'](hand_landmarks)
