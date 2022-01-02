from sys import exit, argv
from os import path
from typing import Callable, List, Dict

from PyQt5.QtWidgets import QWidget, QMainWindow, QFileDialog, QApplication, QMenuBar, QAction, QMenu, \
    QPushButton, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QPaintEvent, QImage, QResizeEvent, QColor, QMouseEvent, QCloseEvent
from PyQt5.QtCore import Qt, QPoint, QRectF

from lib.camera.video_capture import camera_capture, update_window_size
from lib.gestures.hand_on_change_event import HandOnChangeEvent
from lib.gestures.hand_position_resolver import HandPosition
from lib.utils.mouse_paint_functions import MOUSE_PAINT_DICT
from lib.gestures.gesture_paint_functions import UNKNOWN_paint_event, STATES
from lib.gestures.gesture_dict import GESTURE_DICT, NO_HANDS_DETECTED_STRING

WIDTH = 1280
HEIGHT = 720


class MainGUI(QWidget):

    def __init__(self):
        super().__init__(flags=Qt.Window)
        self.custom_gray: QColor = QColor(230, 231, 233)
        self.image: QImage = QImage(WIDTH, HEIGHT, QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.copy_image: QImage = self.image
        self.image_to_save: QImage = self.image
        self.hand_position: HandPosition = HandPosition(0, 0, False)
        self.current_callback: Callable = UNKNOWN_paint_event
        self.previous_pos: QPoint = None
        self.current_pos: QPoint = None
        self.current_width: int = WIDTH
        self.current_height: int = HEIGHT
        self.stamp: float = 0
        self.image_size: float = 0

        self.resolved_width: float = 0
        self.resolved_height: float = 0

        self.unconfirmed_func_callback: Callable = None

        self.command_list: List[Callable] = []
        self.command_list_backup: List[Callable] = []
        self.current_gesture_description: str = NO_HANDS_DETECTED_STRING
        self.current_gesture: str = "UNKNOWN"

        self.COLOR_LIST: List[QColor] = [Qt.black, Qt.red, Qt.blue, Qt.green, Qt.gray, Qt.magenta, Qt.yellow]
        self.COLOR_LIST_COPY = self.COLOR_LIST[:]
        self.current_pen_color: QColor = Qt.black
        self.current_pen_size: int = 10

        self.cursor_size: int = 50
        self.cursor_size_half: float = self.cursor_size / 2
        self.current_menu_rect: QRectF
        self.current_text_x_pos_start: int = 0
        self.current_text_stamp: float = 0

        self.font_size: int = 0
        self.display_process_stamp_1: int = 0
        self.display_process_stamp_2: int = 0
        self.display_process_stamp_3: int = 0

        self.display_process_color_x: int = 0
        self.display_process_color_y: int = 0

        self.menu_bar: QMenuBar = QMenuBar(self)
        self.file_menu: QMenu = self.menu_bar.addMenu("File")
        self.edit_menu: QMenu = self.menu_bar.addMenu("Edit")
        self.options_menu: QMenu = self.menu_bar.addMenu("Options")

        self.SWITCH_MODE_FLAG: bool = True

        self.SWITCH_MODE = {
            "display_menu": {
                True: self.display_hand_menu,
                False: self.display_mouse_menu
            },
            "update": {
                True: self.update_hand_menu,
                False: self.update_mouse_menu
            },
            "cursor": {
                True: self.display_cursor,
                False: lambda nothing: None
            },
            "option": {
                True: 'Switch to the manual mode',
                False: 'Switch to the hand mode'
            },
            "event_handler": {
                True: self.hand_event_handler,
                False: self.mouse_press_event_handler
            }
        }

        self.setMinimumSize(WIDTH, HEIGHT)
        QMainWindow.setWindowTitle(self, "Hand Painter")
        QMainWindow.resize(self, WIDTH, HEIGHT)

        self.switch_action: QAction = QAction(self.SWITCH_MODE["option"][self.SWITCH_MODE_FLAG], self)
        self.render_toolbar_menu()

        self.buttons: Dict[str, QPushButton] = {
            "pencil_button": QPushButton("Pencil", self),
            "change_color_button": QPushButton("Change color", self),
            "rectangle_button": QPushButton("Draw rectangle", self),
            "circle_button": QPushButton("Draw circle", self),
            "undo_pen_button": QPushButton("Undo", self),
            "redo_pen_button": QPushButton("Redo", self),
            "enlarge_pen_button": QPushButton("Magnify pen size", self),
            "reduce_pen_button": QPushButton("Reduce pen size", self),
            "clear_window_button": QPushButton("Clear window", self),
            "save_button": QPushButton("Save", self),
            "quit_button": QPushButton("Quit", self)
        }

        self.button_width: int = 0
        self.current_mouse_paint_function: str = "pencil"

        self.render_buttons()

        self.show()

    def render_toolbar_menu(self):
        """
        Method that is responsible for the toolbar menu initialization.
        :return:
        """

        # File menu
        new_action = QAction('New', self)
        new_action.triggered.connect(self.new_scene)
        new_action.setShortcut(Qt.CTRL + Qt.Key_N)
        self.file_menu.addAction(new_action)

        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_file_dialog)
        save_action.setShortcut(Qt.CTRL + Qt.Key_S)
        self.file_menu.addAction(save_action)

        quit_action = QAction('Quit program', self)
        quit_action.triggered.connect(self.emit_quit)
        quit_action.setShortcut(Qt.CTRL + Qt.Key_Q)
        self.file_menu.addAction(quit_action)

        # Edit menu
        undo_action = QAction('Undo', self)
        undo_action.triggered.connect(self.undo)
        undo_action.setShortcut(Qt.CTRL + Qt.Key_Z)
        self.edit_menu.addAction(undo_action)

        redo_action = QAction('Redo', self)
        redo_action.triggered.connect(self.redo)
        redo_action.setShortcut(Qt.CTRL + Qt.ALT + Qt.Key_Z)
        self.edit_menu.addAction(redo_action)

        clear_action = QAction('Clear entire window', self)
        clear_action.triggered.connect(self.clear_window)
        clear_action.setShortcut(Qt.CTRL + Qt.Key_W)
        self.edit_menu.addAction(clear_action)

        # Options menu

        self.switch_action.triggered.connect(self.switch_mode)
        self.options_menu.addAction(self.switch_action)

        enlarge_action = QAction('Enlarge pen size', self)
        enlarge_action.triggered.connect(self.enlarge_pen_size)
        enlarge_action.setShortcut(Qt.Key_Plus)
        self.options_menu.addAction(enlarge_action)

        reduce_action = QAction('Reduce pen size', self)
        reduce_action.triggered.connect(self.reduce_pen_size)
        reduce_action.setShortcut(Qt.Key_Minus)
        self.options_menu.addAction(reduce_action)

        color_action = QAction('Change pen color', self)
        color_action.triggered.connect(self.change_color)
        color_action.setShortcut(Qt.CTRL + Qt.Key_T)
        self.options_menu.addAction(color_action)

    def set_current_mouse_paint_function(self, function: str):
        """
        Method that is setting current mouse paint function.
        :param function: Callback to the paint function given as a string.
        :return:
        """
        self.current_mouse_paint_function = function

    def render_buttons(self):
        """
        Method that is responsible for mouse menu buttons preparing.
        :return:
        """
        for button in self.buttons:
            self.buttons[button].resize(100, 32)

        self.buttons["pencil_button"].clicked.connect(lambda x: self.set_current_mouse_paint_function("pencil"))
        self.buttons["change_color_button"].clicked.connect(self.change_color)
        self.buttons["rectangle_button"].clicked.connect(lambda x: self.set_current_mouse_paint_function("rectangle"))
        self.buttons["circle_button"].clicked.connect(lambda x: self.set_current_mouse_paint_function("circle"))
        self.buttons["enlarge_pen_button"].clicked.connect(self.enlarge_pen_size)
        self.buttons["reduce_pen_button"].clicked.connect(self.reduce_pen_size)
        self.buttons["undo_pen_button"].clicked.connect(self.undo)
        self.buttons["redo_pen_button"].clicked.connect(self.redo)
        self.buttons["clear_window_button"].clicked.connect(self.clear_window)
        self.buttons["save_button"].clicked.connect(self.save_file_dialog)
        self.buttons["quit_button"].clicked.connect(self.emit_quit)

    def display_cursor(self, painter: QPainter):
        """
        Method responsible for cursor displaying.
        :param painter:
        """
        painter.setPen(Qt.green)
        painter.setBrush(Qt.green)
        if self.hand_position.visible:
            position = QPoint(self.hand_position.x - self.cursor_size_half,
                              self.hand_position.y - self.cursor_size_half)
            painter.drawImage(position,
                              QImage(GESTURE_DICT[self.current_gesture]['icon']).scaled(self.cursor_size,
                                                                                        self.cursor_size))
            painter.drawImage(position,
                              QImage(GESTURE_DICT[self.current_gesture]['available'][STATES.BLOCKED]).scaled(
                                  self.cursor_size_half, self.cursor_size_half))

    def display_current_process(self, painter: QPainter, painting_mode: bool):
        """
        Method responsible for displaying following information about:
            - current process,
            - rectangle/circle drawing mode,
            - current color,
            - current pen size.
        :param painting_mode:
        :param painter:
        """
        painter.setPen(Qt.black)
        font = painter.font()
        font.setPointSize(self.font_size)
        painter.setFont(font)
        process_string = f"{self.current_gesture_description}, circle/rectangle mode: {STATES.BLOCKED}" if painting_mode else "Manual mode."
        painter.drawText(QPoint(10, self.display_process_stamp_1), process_string)
        painter.drawText(QPoint(10, self.display_process_stamp_2), "Current color:")
        painter.drawText(QPoint(10, self.display_process_stamp_3), f"Current pen size: {self.current_pen_size}")
        painter.setBrush(self.current_pen_color)
        painter.drawEllipse(QPoint(self.display_process_color_x, self.display_process_color_y), 5, 5)

    def display_hand_menu(self, painter: QPainter):
        """
        Method, which is responsible for displaying hand GUI menu.
        :param painter:
        """
        self.resolved_height = 0

        # Gray panel
        painter.setPen(self.custom_gray)
        painter.setBrush(self.custom_gray)
        painter.drawRect(self.current_menu_rect)

        painter.setPen(Qt.black)
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        for gesture in GESTURE_DICT:
            if path.exists(GESTURE_DICT[gesture]['image_path']):
                painter.drawImage(QPoint(self.resolved_width, self.resolved_height),
                                  QImage(GESTURE_DICT[gesture]['image_path']).scaled(self.image_size, self.image_size))

                painter.drawText(QRectF(self.current_text_x_pos_start, self.resolved_height + self.current_text_stamp,
                                        self.current_width, self.current_height),
                                 GESTURE_DICT[gesture]['description'])
                self.resolved_height += self.stamp

    def display_mouse_menu(self, painter: QPainter):
        """
        Method, which is responsible for displaying mouse GUI menu.
        :param painter:
        """
        # Gray panel
        painter.setPen(self.custom_gray)
        painter.setBrush(self.custom_gray)
        painter.drawRect(self.current_menu_rect)
        current_height = self.stamp / 2
        for button in self.buttons:
            self.buttons[button].move(self.resolved_width, current_height)
            self.buttons[button].resize(self.button_width, 32)
            self.buttons[button].show()
            current_height += self.stamp

    def disable_buttons(self):
        """
        Simple method that is responsible for disabling mouse menu buttons after switching
        application to hand mode.
        """
        for button in self.buttons:
            self.buttons[button].hide()

    def switch_mode(self):
        """
        Method that is responsible for switching application paint mode.
        """
        if self.SWITCH_MODE_FLAG and self.unconfirmed_func_callback is not None:
            GESTURE_DICT["THREE"]["callback"](self)  # TO PREVENT BUGS CAUSED BY SWITCHING BETWEEN PAINTING MODES
        print(f"Current mode: {self.SWITCH_MODE['option'][self.SWITCH_MODE_FLAG]}")
        self.SWITCH_MODE_FLAG = not self.SWITCH_MODE_FLAG
        self.switch_action.setText(self.SWITCH_MODE["option"][self.SWITCH_MODE_FLAG])
        self.SWITCH_MODE["update"][self.SWITCH_MODE_FLAG]()

    def paintEvent(self, event: QPaintEvent):
        """
        Paint event method, which is responsible for entire paint process.
        :param event:
        """
        self.copy_image = QImage(self.image)

        painter_image = QPainter()
        painter_image.begin(self.copy_image)
        painter_image.setRenderHint(QPainter.Antialiasing)
        painter_image.setPen(QPen(Qt.black, self.current_pen_size, Qt.SolidLine))

        for process in self.command_list:
            try:
                process(painter_image)
            except:
                pass

        self.image_to_save = QImage(self.copy_image)

        if self.unconfirmed_func_callback is not None:
            self.unconfirmed_func_callback(painter_image)

        self.current_pen_color = painter_image.pen().color()
        self.SWITCH_MODE["cursor"][self.SWITCH_MODE_FLAG](painter_image)
        self.display_current_process(painter_image, self.SWITCH_MODE_FLAG)
        self.SWITCH_MODE["display_menu"][self.SWITCH_MODE_FLAG](painter_image)
        painter_image.end()

        painter_window = QPainter()
        painter_window.begin(self)
        painter_window.drawImage(0, 0, self.copy_image, 0, 0, self.current_width, self.current_height)
        painter_window.end()

    def update_hand_menu(self):
        """
        Method that is responsible for updating hand menu parameters.
        """
        self.disable_buttons()
        self.stamp = self.current_height / (len(GESTURE_DICT) - 1)
        self.image_size = self.stamp * 0.85

        self.resolved_width = self.current_width - 1.2 * self.stamp

        self.current_menu_rect = QRectF(self.current_width - self.stamp * 1.6, 0, self.current_width,
                                        self.current_height)
        self.current_text_x_pos_start = self.current_width - self.stamp * 1.5
        self.current_text_stamp = 0.75 * self.stamp

        self.process_position_update(self.stamp)

    def update_mouse_menu(self):
        """
        Method that is responsible for updating mouse menu parameters.
        """
        self.stamp = self.current_height / (len(self.buttons) + 1)
        self.button_width = 1.5 * self.stamp

        self.resolved_width = self.current_width - self.button_width

        self.current_menu_rect = QRectF(self.resolved_width, 0, self.current_width, self.current_height)

        stamp_tmp = self.stamp * 0.75
        self.process_position_update(stamp_tmp)

    def process_position_update(self, stamp: float):
        """
        Method that is responsible for computing current position of process information.
        :param stamp:
        :return:
        """
        self.font_size = stamp / 4
        self.display_process_stamp_1 = stamp / 3
        self.display_process_stamp_2 = self.display_process_stamp_1 * 2
        self.display_process_stamp_3 = self.display_process_stamp_1 * 3
        self.display_process_color_x = self.display_process_stamp_1 * 8.3
        self.display_process_color_y = self.display_process_stamp_1 * 1.65

        move = 15
        self.display_process_stamp_1 += move
        self.display_process_stamp_2 += move
        self.display_process_stamp_3 += move
        self.display_process_color_y += move

    def resizeEvent(self, event: QResizeEvent):
        """
        Resize event method, which is responsible for updating proper attributes of main GUI.
        :param event:
        """
        self.image = QImage(self.size().width(), self.size().height(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        update_window_size(self)
        self.current_width = self.width()
        self.current_height = self.height()

        self.SWITCH_MODE["update"][self.SWITCH_MODE_FLAG]()

    def hand_event_handler(self, event: HandOnChangeEvent):
        """
        Method that is responsible for handling hand event.
        :param event:
        """
        self.hand_position = HandPosition(event.hand_x, event.hand_y, event.get_drawing_flag())
        if event.drawing_flag:
            self.previous_pos = self.current_pos
            self.current_pos = QPoint(event.hand_x, event.hand_y)
            self.current_gesture = event.resolved_gesture
            self.current_gesture_description = GESTURE_DICT[event.resolved_gesture]['description']
            self.current_callback = event.callback_to_gesture_function
            self.current_callback(self)
        else:
            self.current_gesture_description = NO_HANDS_DETECTED_STRING

    def mouse_press_event_handler(self, event: QMouseEvent):
        """
        Method that is responsible for handling mouse press event.
        :param event:
        """
        if type(event) is not HandOnChangeEvent:
            try:
                MOUSE_PAINT_DICT[self.SWITCH_MODE_FLAG][self.current_mouse_paint_function]["on_click"](self,
                                                                                                       QPoint(event.x(),
                                                                                                              event.y()))
            except:
                pass

    def mousePressEvent(self, event: QMouseEvent):
        """
        Mouse Press Event - handler for HandOnChangeEvent or QMouseEvent signals,
        which contain all the needed information about current position, etc.
        :param event:
        """
        try:
            self.SWITCH_MODE["event_handler"][self.SWITCH_MODE_FLAG](event)
        except Exception:
            pass
        self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        """
        Mouse Move Event - handler for QMouseEvent signal.
        :param event:
        """
        try:
            MOUSE_PAINT_DICT[self.SWITCH_MODE_FLAG][self.current_mouse_paint_function]["on_move"](self,
                                                                                                  QPoint(event.x(),
                                                                                                         event.y()))
        except:
            pass

        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """
        Mouse Release Event - handler for QMouseEvent signal.
        :param event:
        """
        try:
            MOUSE_PAINT_DICT[self.SWITCH_MODE_FLAG][self.current_mouse_paint_function]["on_release"](self,
                                                                                                     QPoint(event.x(),
                                                                                                            event.y()))
        except:
            pass

        self.update()

    def get_previous_hand_pos(self) -> QPoint:
        """
        Simple method that returns previous hand position.
        :return: QPoint.
        """
        return self.previous_pos

    def get_current_hand_pos(self) -> QPoint:
        """
        Simple method that returns current hand position.
        :return: QPoint.
        """
        return self.current_pos

    def paint_process_list_appender(self, process: Callable):
        """
        Simple method that is adding new painting process to the process list.
        :param process:
        """
        self.command_list.append(process)
        self.command_list_backup = self.command_list[:]

    def new_scene(self):
        """
        Method that is resetting values to its initial states.
        """
        self.clear_window()
        self.command_list_backup = []
        self.COLOR_LIST_COPY = self.COLOR_LIST[:]
        self.current_pen_size = 10
        self.current_pen_color = Qt.black
        self.image_to_save = self.image
        self.copy_image = self.image

    def clear_window(self):
        """
        Simple method that is wiping current command list to simulate clearing window process.
        """
        self.command_list = []

    def undo(self):
        """
        Method that is deleting last process from the process list.
        """
        try:
            self.command_list.pop()
        except IndexError:
            pass

    def redo(self):
        """
        Method that brings back last deleted process from process list.
        """
        try:
            self.command_list.append(self.command_list_backup[len(self.command_list)])
        except IndexError:
            pass

    def save_file_dialog(self):
        """
        Method that gives the user the ability to save the current paint image to the file.
        """
        print("Saving file!")
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save file", "Untitled",
                                                   "JPG Files (*.jpg);;PNG Files (*.png)", options=options)
        if file_name:
            self.image_to_save.save(file_name)

    def set_unconfirmed_callback(self, callback: Callable):
        """
        Simple method that sets unconfirmed paint function variable to the given callback.
        :param callback:
        """
        self.unconfirmed_func_callback = callback

    def get_unconfirmed_callback(self) -> Callable:
        """
        Simple method that returns current unconfirmed paint function to the given callback.
        :return:
        """
        return self.unconfirmed_func_callback

    def reset_unconfirmed_callback(self):
        """
        Simple method that sets unconfirmed paint function variable to the None.
        :return:
        """
        self.unconfirmed_func_callback = None

    def enlarge_pen_size(self):
        """
        Simple method that enlarges pen size.
        """
        self.current_pen_size += 1

    def reduce_pen_size(self):
        """
        Simple method that reduces pen size.
        """
        if self.current_pen_size > 1:
            self.current_pen_size -= 1

    def get_pen_size(self) -> int:
        """
        Simple method that returns current pen size.
        :return: int
        """
        return self.current_pen_size

    def get_current_color(self) -> QColor:
        """
        Simple method that returns current pen color.
        :return: QColor
        """
        return self.current_pen_color

    def change_color(self):
        """
        Method that is changing current pen color.
        """
        previous_color = self.COLOR_LIST_COPY.pop(0)
        pen_color = self.COLOR_LIST_COPY[0]
        self.COLOR_LIST_COPY.append(previous_color)
        pen_size = self.get_pen_size()
        self.paint_process_list_appender(lambda painter: painter.setPen(QPen(pen_color, pen_size, Qt.SolidLine)))

    def hand_capture_start(self):
        """
        Method that is responsible for enabling camera capture for detecting hands.
        """
        camera_capture(self)

    def closeEvent(self, event: QCloseEvent):
        exit_dialog = QMessageBox.question(self, "Quit program", "Are you sure to exit the program?", QMessageBox.Yes | QMessageBox.Cancel)
        if exit_dialog == QMessageBox.Yes:
            exit(0)
        else:
            event.ignore()

    def emit_quit(self):
        QApplication.sendEvent(self, QCloseEvent())


def run_GUI():
    app = QApplication(argv)
    gui = MainGUI()
    gui.show()
    gui.hand_capture_start()

    try:
        exit(app.exec_())
    except SystemExit:
        pass
