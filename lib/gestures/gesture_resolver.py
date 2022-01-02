from mediapipe.python.solutions.hands import HandLandmark
from mediapipe.framework.formats import landmark_pb2
from lib.gestures.gesture_dict import GESTURE_DICT

acceptable_surrounding = 0.

GESTURES_DICT_KEYS_LIST = list(GESTURE_DICT.keys())
GESTURES_DICT_VALUES_LIST = [element['gesture'] for element in list(GESTURE_DICT.values())]


def resolve_scale(hand_structure: landmark_pb2.NormalizedLandmarkList) -> float:
    """
    Function, which is resolving current distance between WRIST and MIDDLE_FINGER_MCP hand points.
    :param hand_structure: Hand gesture structure.
    :return: Distance between WRIST and MIDDLE_FINGER_MCP hand points.
    """
    return (((hand_structure.landmark[HandLandmark.WRIST].x - hand_structure.landmark[
        HandLandmark.MIDDLE_FINGER_MCP].x) ** 2 + (
                     hand_structure.landmark[HandLandmark.WRIST].y - hand_structure.landmark[
                        HandLandmark.MIDDLE_FINGER_MCP].y) ** 2) ** 0.5)


def gesture_resolver(hand_structure: landmark_pb2.NormalizedLandmarkList) -> str:
    """
    Function, which is resolving hand gesture from the hand_gesture parameter.
    :param hand_structure: Hand gesture structure.
    :return: Hand gesture as a string.
    """
    global acceptable_surrounding
    acceptable_surrounding = resolve_scale(hand_structure)
    resolved_gesture = [
        check_if_finger_is_open(hand_structure.landmark, HandLandmark.RING_FINGER_MCP, HandLandmark.THUMB_TIP,
                                sigma_resizer=.8),
        check_if_finger_is_open(hand_structure.landmark, HandLandmark.INDEX_FINGER_MCP, HandLandmark.INDEX_FINGER_TIP),
        check_if_finger_is_open(hand_structure.landmark, HandLandmark.MIDDLE_FINGER_MCP,
                                HandLandmark.MIDDLE_FINGER_TIP),
        check_if_finger_is_open(hand_structure.landmark, HandLandmark.RING_FINGER_MCP, HandLandmark.RING_FINGER_TIP),
        check_if_finger_is_open(hand_structure.landmark, HandLandmark.PINKY_MCP, HandLandmark.PINKY_TIP)
    ]

    try:
        return GESTURES_DICT_KEYS_LIST[GESTURES_DICT_VALUES_LIST.index(resolved_gesture)]
    except ValueError:
        return "UNKNOWN"


def check_if_finger_is_open(hand_landmarks: landmark_pb2.NormalizedLandmarkList, finger_point_start: HandLandmark,
                            finger_point_end: HandLandmark, sigma_resizer: float = 0.5) -> bool:
    """
    Function, which checks, if given finger is open.
    :param hand_landmarks: Hand gesture structure.
    :param finger_point_start: Start point of the given finger.
    :param finger_point_end: End point of the given finger.
    :param sigma_resizer: Variable that has the ability to change the criteria
    by which a finger is determined to be open (DEFAULT 0.5).
    :return: boolean
    """
    pos_x = (hand_landmarks[finger_point_start].x - hand_landmarks[finger_point_end].x) ** 2
    pos_y = (hand_landmarks[finger_point_start].y - hand_landmarks[finger_point_end].y) ** 2
    # print("{} and  {}".format((pos_x + pos_y) ** 0.5, acceptable_surrounding * sigma_resizer))
    return ((pos_x + pos_y) ** 0.5) > (acceptable_surrounding * sigma_resizer)
