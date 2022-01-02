from PyQt5.QtCore import Qt, QEvent, QPoint
from PyQt5.QtGui import QMouseEvent
from typing import Callable

from lib.gestures.gesture_paint_function_resolver import gesture_paint_function_resolver


class HandOnChangeEvent(QMouseEvent):
    """
    HandOnChangeEvent class, which is inheriting over QMouseEvent class.
    It is responsible for creating an event with proper attributes of detected hand, which is meant to be emitted.
    """
    def __init__(self, x: float, y: float, window_width: int, window_height: int, resolved_gesture: str,
                 drawing_flag: bool):
        super().__init__(QEvent.MouseButtonPress, QPoint(0, 0),
                         Qt.LeftButton, Qt.LeftButton, Qt.KeyboardModifier())
        self.hand_x = int(window_width * x)
        self.hand_y = int(window_height * y)
        self.resolved_gesture: str = resolved_gesture
        self.callback_to_gesture_function: Callable = gesture_paint_function_resolver(resolved_gesture)
        self.drawing_flag: bool = drawing_flag

    def get_drawing_flag(self) -> bool:
        """
        Simple method, which is returning boolean drawing flag.
        :return: drawing_flag.
        """
        return self.drawing_flag
