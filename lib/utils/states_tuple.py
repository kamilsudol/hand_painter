from typing import Callable
from PyQt5.QtCore import QPoint


class StatesTuple:
    """
    Simple class, which represents couple of boolean state variables,
    which are essential to proper work of the drawing module.
    """
    UNCONFIRMED_FUNCTION_FLAG: bool = False
    UNCONFIRMED_FUNCTION_CONTINUE_FLAG: bool = False
    BLOCKED: bool = False
    CIRCLE_OR_RECTANGLE_EVENT_MODE_AVAILABLE: bool = True
    INITIAL_CENTER_POSITION: QPoint = None
    CURRENT_CALLBACK_TO_PAINT_FUNCTION: Callable = None
    COLOR_CHANGE_MODE_AVAILABLE: bool = True

    def reset(self):
        """
        Reset method, which sets proper variables to its initial states.
        """
        self.UNCONFIRMED_FUNCTION_FLAG = False
        self.UNCONFIRMED_FUNCTION_CONTINUE_FLAG = False
        self.INITIAL_CENTER_POSITION = None
        self.CURRENT_CALLBACK_TO_PAINT_FUNCTION = None
        self.CIRCLE_OR_RECTANGLE_EVENT_MODE_AVAILABLE = False
        self.BLOCKED = False

    def unblock(self):
        """
        Method, which is resetting two most important boolean flags, which are
        responsible for current drawing availability.
        """
        self.CIRCLE_OR_RECTANGLE_EVENT_MODE_AVAILABLE = True
        self.COLOR_CHANGE_MODE_AVAILABLE = True
