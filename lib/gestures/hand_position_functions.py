from typing import Tuple
from mediapipe.framework.formats import landmark_pb2
from mediapipe.python.solutions.hands import HandLandmark


def get_middle_of_hand(hand_landmarks: landmark_pb2.NormalizedLandmarkList) -> Tuple[float, float]:
    """
    Function, which is returning coordinates of a point, which is located in the middle of the detected hand.
    :param hand_landmarks: Hand gesture structure.
    :return: Tuple of x and y coordinates.
    """
    x = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_MCP].x
    y = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_MCP].y
    return x, y


def get_one_finger_tip_position(hand_landmarks: landmark_pb2.NormalizedLandmarkList) -> Tuple[float, float]:
    """
    Function that returns the coordinates of a point that is at the tip of the index finger of the detected hand.
    :param hand_landmarks: Hand gesture structure.
    :return: Tuple of x and y coordinates.
    """
    x = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_TIP].x
    y = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_TIP].y
    return x, y
