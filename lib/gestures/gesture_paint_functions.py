from PyQt5.QtGui import QPen, QPainter, QCloseEvent
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QApplication
from lib.utils.states_tuple import StatesTuple

STATES = StatesTuple()


def do_nothing(gui: QWidget):
    pass


def ONE_paint_func(gui: QWidget):
    """
    Paint function, that is responsible for line drawing.
    :param gui:
    :return:
    """
    global STATES
    STATES.unblock()

    previous = QPoint(gui.get_previous_hand_pos())
    current = QPoint(gui.get_current_hand_pos())

    pen_size = gui.get_pen_size()
    color = gui.get_current_color()

    def tmp_fun(painter: QPainter):
        painter.setPen(QPen(color, pen_size, Qt.SolidLine))
        painter.drawLine(previous, current)

    gui.paint_process_list_appender(tmp_fun)


def TWO_paint_func(gui: QWidget):
    """
    Paint function, that is responsible for the changing current pen color.
    :param gui:
    :return:
    """
    global STATES
    STATES.CIRCLE_OR_RECTANGLE_EVENT_MODE_AVAILABLE = True
    gui.change_color()
    STATES.COLOR_CHANGE_MODE_AVAILABLE = False


def THREE_paint_func(gui: QWidget):
    """
    Paint function, that is responsible for the drawing rectangle process.
    :param gui:
    :return:
    """
    global STATES

    if not STATES.UNCONFIRMED_FUNCTION_FLAG and STATES.CIRCLE_OR_RECTANGLE_EVENT_MODE_AVAILABLE:
        STATES.BLOCKED = True
        STATES.UNCONFIRMED_FUNCTION_FLAG = True
        STATES.INITIAL_CENTER_POSITION = QPoint(gui.get_current_hand_pos())
        STATES.CURRENT_CALLBACK_TO_PAINT_FUNCTION = lambda painter, start, end_x, end_y: painter.drawRect(start.x(),
                                                                                                          start.y(),
                                                                                                          end_x, end_y)

    if STATES.UNCONFIRMED_FUNCTION_CONTINUE_FLAG:
        pen_size = gui.get_pen_size()
        color = gui.get_current_color()
        last_callback = gui.get_unconfirmed_callback()

        def tmp_fun(painter: QPainter):
            painter.setPen(QPen(color, pen_size, Qt.SolidLine))
            last_callback(painter)

        gui.paint_process_list_appender(tmp_fun)
        gui.reset_unconfirmed_callback()
        STATES.reset()


def FOUR_paint_func(gui: QWidget):
    """
    Paint function, that is responsible for the drawing circle process.
    :param gui:
    :return:
    """
    global STATES

    if not STATES.UNCONFIRMED_FUNCTION_FLAG and STATES.CIRCLE_OR_RECTANGLE_EVENT_MODE_AVAILABLE:
        STATES.BLOCKED = True
        STATES.UNCONFIRMED_FUNCTION_FLAG = True
        STATES.INITIAL_CENTER_POSITION = QPoint(gui.get_current_hand_pos())
        STATES.CURRENT_CALLBACK_TO_PAINT_FUNCTION = lambda painter, start, end_x, end_y: painter.drawEllipse(start.x(),
                                                                                                             start.y(),
                                                                                                             end_x,
                                                                                                             end_y)

    if STATES.UNCONFIRMED_FUNCTION_CONTINUE_FLAG:
        pen_size = gui.get_pen_size()
        color = gui.get_current_color()
        last_callback = gui.get_unconfirmed_callback()

        def tmp_fun(painter: QPainter):
            painter.setPen(QPen(color, pen_size, Qt.SolidLine))
            last_callback(painter)

        gui.paint_process_list_appender(tmp_fun)
        gui.reset_unconfirmed_callback()
        STATES.reset()


def FIVE_paint_func(gui: QWidget):
    """
    Paint function, which is used in the rectangle or circle drawing mode to resolve its size.
    :param gui:
    :return:
    """
    global STATES

    if STATES.UNCONFIRMED_FUNCTION_FLAG:
        STATES.UNCONFIRMED_FUNCTION_CONTINUE_FLAG = True
        current = QPoint(gui.get_current_hand_pos())
        current_initial = QPoint(STATES.INITIAL_CENTER_POSITION)
        new_callable = STATES.CURRENT_CALLBACK_TO_PAINT_FUNCTION
        r_x = -(current_initial.x() - current.x())
        r_y = -(current_initial.y() - current.y())
        gui.set_unconfirmed_callback(lambda painter: new_callable(painter, current_initial, r_x, r_y))


def SIX_paint_func(gui: QWidget):
    """
    Paint function, that has ability to undo the previous paint command.
    :param gui:
    :return:
    """
    global STATES
    STATES.unblock()
    gui.undo()


def ROCK_paint_func(gui: QWidget):
    """
    Paint function, which is neutral and do nothing.
    :param gui:
    :return:
    """
    global STATES
    STATES.unblock()


def OK_paint_func(gui: QWidget):
    """
    Paint function that allows user to save the current painting to the file.
    :param gui:
    :return:
    """
    global STATES
    STATES.unblock()
    gui.save_file_dialog()


def VICTORY_paint_func(gui: QWidget):
    """
    Paint function that has ability to redo the previous paint command.
    :param gui:
    :return:
    """
    global STATES
    STATES.unblock()
    gui.redo()


def SPIDERMAN_paint_func(gui: QWidget):
    """
    Paint function that has ability to clear the entire painting screen.
    :param gui:
    :return:
    """
    global STATES
    STATES.unblock()
    gui.clear_window()


def SATAN_paint_func(gui: QWidget):
    """
    Paint function that has ability to enlarge the pen size.
    :param gui:
    :return:
    """
    global STATES
    STATES.unblock()
    gui.enlarge_pen_size()


def THREE_V2_paint_func(gui: QWidget):
    """
    Paint function that has ability to reduce the pen size.
    :param gui:
    :return:
    """
    global STATES
    STATES.unblock()

    gui.reduce_pen_size()


def QUIT_paint_func(gui: QWidget):
    """
    Paint function that allows user to quit the program.
    :param gui:
    :return:
    """
    QApplication.sendEvent(gui, QCloseEvent())


def UNKNOWN_paint_func(gui: QWidget):
    pass


"""
State dicts, which are mapping proper paint functions depending on the current STATE flags.
"""

ONE_PAINT_MAP = {
    True: do_nothing,
    False: ONE_paint_func
}

TWO_PAINT_MAP = {
    True: TWO_paint_func,
    False: do_nothing
}

THREE_PAINT_MAP = {
    True: THREE_paint_func,
    False: THREE_paint_func
}

FOUR_PAINT_MAP = {
    True: FOUR_paint_func,
    False: FOUR_paint_func
}

FIVE_PAINT_MAP = {
    True: FIVE_paint_func,
    False: do_nothing
}

SIX_PAINT_MAP = {
    True: do_nothing,
    False: SIX_paint_func
}

SATAN_PAINT_MAP = {
    True: do_nothing,
    False: SATAN_paint_func
}

THREE_V2_PAINT_MAP = {
    True: do_nothing,
    False: THREE_V2_paint_func
}

SPIDERMAN_PAINT_MAP = {
    True: do_nothing,
    False: SPIDERMAN_paint_func
}

ROCK_PAINT_MAP = {
    True: do_nothing,
    False: ROCK_paint_func
}

OK_PAINT_MAP = {
    True: do_nothing,
    False: OK_paint_func
}

VICTORY_PAINT_MAP = {
    True: do_nothing,
    False: VICTORY_paint_func
}

QUIT_PAINT_MAP = {
    True: do_nothing,
    False: QUIT_paint_func
}

UNKNOWN_PAINT_MAP = {
    True: do_nothing,
    False: UNKNOWN_paint_func
}

"""
Segment of code, where the proper paint functions are called from the state dicts.
"""


def ONE_paint_event(gui: QWidget):
    global STATES
    ONE_PAINT_MAP[STATES.BLOCKED](gui)


def TWO_paint_event(gui: QWidget):
    global STATES
    TWO_PAINT_MAP[STATES.COLOR_CHANGE_MODE_AVAILABLE](gui)


def FOUR_paint_event(gui: QWidget):
    global STATES
    FOUR_PAINT_MAP[STATES.BLOCKED](gui)


def THREE_paint_event(gui: QWidget):
    global STATES
    THREE_PAINT_MAP[STATES.BLOCKED](gui)


def FIVE_paint_event(gui: QWidget):
    global STATES
    FIVE_PAINT_MAP[STATES.BLOCKED](gui)


def SIX_paint_event(gui: QWidget):
    global STATES
    SIX_PAINT_MAP[STATES.BLOCKED](gui)


def ROCK_paint_event(gui: QWidget):
    global STATES
    ROCK_PAINT_MAP[STATES.BLOCKED](gui)


def OK_paint_event(gui: QWidget):
    global STATES
    OK_PAINT_MAP[STATES.BLOCKED](gui)


def VICTORY_paint_event(gui: QWidget):
    global STATES
    VICTORY_PAINT_MAP[STATES.BLOCKED](gui)


def SPIDERMAN_paint_event(gui: QWidget):
    global STATES
    SPIDERMAN_PAINT_MAP[STATES.BLOCKED](gui)


def SATAN_paint_event(gui: QWidget):
    global STATES
    SATAN_PAINT_MAP[STATES.BLOCKED](gui)


def THREE_V2_paint_event(gui: QWidget):
    global STATES
    THREE_V2_PAINT_MAP[STATES.BLOCKED](gui)


def QUIT_paint_event(gui: QWidget):
    global STATES
    QUIT_PAINT_MAP[STATES.BLOCKED](gui)


def UNKNOWN_paint_event(gui: QWidget):
    global STATES
    UNKNOWN_PAINT_MAP[STATES.BLOCKED](gui)
