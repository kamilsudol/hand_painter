from PyQt5.QtGui import QPen, QPainter
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget
from typing import Callable

TEMPORARY_POINT: QPoint
TEMPORARY_PAINT_FUNCTION: Callable


def mouse_pencil(gui: QWidget, new_point: QPoint):
    """
    Mouse paint function, that is responsible for point drawing.
    :param gui:
    :param new_point:
    :return:
    """
    size = gui.current_pen_size
    color = gui.current_pen_color

    def tmp(painter):
        painter.setPen(QPen(color, size, Qt.SolidLine))
        painter.drawPoint(new_point)

    gui.paint_process_list_appender(tmp)


def mouse_rectangle_click(gui: QWidget, new_point: QPoint):
    """
    Mouse paint function, that is responsible for the rectangle drawing at the on click event.
    :param gui:
    :param new_point:
    :return:
    """
    global TEMPORARY_POINT
    global TEMPORARY_PAINT_FUNCTION
    TEMPORARY_POINT = new_point
    TEMPORARY_PAINT_FUNCTION = lambda painter, start, end_x, end_y: painter.drawRect(start.x(),
                                                                                     start.y(),
                                                                                     end_x, end_y)


def mouse_circle_click(gui: QWidget, new_point: QPoint):
    """
    Mouse paint function, that is responsible for the circle drawing at the on click event.
    :param gui:
    :param new_point:
    :return:
    """
    global TEMPORARY_POINT
    global TEMPORARY_PAINT_FUNCTION
    TEMPORARY_POINT = new_point
    TEMPORARY_PAINT_FUNCTION = lambda painter, start, end_x, end_y: painter.drawEllipse(start.x(),
                                                                                        start.y(),
                                                                                        end_x,
                                                                                        end_y)


def mouse_rectangle_or_circle_move(gui: QWidget, new_point: QPoint):
    """
    Mouse paint function, that is responsible for the rectangle or circle drawing at the on move event.
    :param gui:
    :param new_point:
    :return:
    """
    global TEMPORARY_POINT
    global TEMPORARY_PAINT_FUNCTION
    current = new_point
    current_initial = QPoint(TEMPORARY_POINT)
    new_callable = TEMPORARY_PAINT_FUNCTION
    r_x = -(current_initial.x() - current.x())
    r_y = -(current_initial.y() - current.y())
    gui.set_unconfirmed_callback(lambda painter: new_callable(painter, current_initial, r_x, r_y))


def mouse_rectangle_or_mouse_release(gui: QWidget, new_point: QPoint):
    """
    Mouse paint function, that is responsible for the rectangle or circle drawing at the on release event.
    :param gui:
    :param new_point:
    :return:
    """
    pen_size = gui.get_pen_size()
    color = gui.get_current_color()
    last_callback = gui.get_unconfirmed_callback()

    def tmp_fun(painter: QPainter):
        painter.setPen(QPen(color, pen_size, Qt.SolidLine))
        last_callback(painter)

    gui.paint_process_list_appender(tmp_fun)
    gui.reset_unconfirmed_callback()


# Mouse paint function mapping
MOUSE_PAINT_DICT = {
    True: None,
    False: {
        "pencil": {
            "on_click": mouse_pencil,
            "on_move": mouse_pencil,
            "on_release": mouse_pencil
        },
        "rectangle": {
            "on_click": mouse_rectangle_click,
            "on_move": mouse_rectangle_or_circle_move,
            "on_release": mouse_rectangle_or_mouse_release
        },
        "circle": {
            "on_click": mouse_circle_click,
            "on_move": mouse_rectangle_or_circle_move,
            "on_release": mouse_rectangle_or_mouse_release
        },
    }
}
