from typing import Callable
from lib.gestures.gesture_dict import GESTURE_DICT


def gesture_paint_function_resolver(gesture: str) -> Callable:
    """
    Function, which is retrieving callback to the proper paint function from a given hand gesture.
    :param gesture: hand gesture.
    :return: callback to paint function.
    """
    return GESTURE_DICT[gesture]['callback']
