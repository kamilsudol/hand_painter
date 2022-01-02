from lib.gestures.gesture_paint_functions import OK_paint_event, ROCK_paint_event, ONE_paint_event, TWO_paint_event, \
    THREE_paint_event, FOUR_paint_event, FIVE_paint_event, SIX_paint_event, QUIT_paint_event, VICTORY_paint_event, \
    SATAN_paint_event, SPIDERMAN_paint_event, UNKNOWN_paint_event, THREE_V2_paint_event
from lib.gestures.hand_position_functions import get_middle_of_hand

"""
Dictionary, which contains couple of attributes assigned to each hand gesture:
    - gesture: General description of the way of mapping fingers to list:
            Index 0 - THUMB FINGER,
            Index 1 - INDEX FINGER,
            Index 2 - MIDDLE FINGER,
            Index 3 - RING FINGER,
            Index 4 - PINKY FINGER
    - callback: Callback to the proper paint function.
    - description: Gesture functionality description.
    - image_path: Path to the image, which represents proper gesture in menu.
    - icon: Path to the image, which is used in the paint area to inform user, which gesture is currently used.
    - available: boolean dict, which tells user, if following gesture functionality is currently available.
    - hand_position_function: Callback to the function, which is responsible for resolving the current hand 
    position based on its gesture.
"""


NO_HANDS_DETECTED_STRING = "No hands detected"
UNAVAILABLE_MODE_IMAGE = 'images/icon_images/unavailable.png'

GESTURE_DICT = {
    "ROCK": {'gesture': [False, False, False, False, False],
             'callback': ROCK_paint_event,
             'description': 'No action',
             'image_path': 'images/gesture_images/rock.png',
             'icon': 'images/icon_images/rock.png',
             'available': {True: '', False: ''},
             'hand_position_function': get_middle_of_hand},
    "ONE": {'gesture': [False, True, False, False, False],
            'callback': ONE_paint_event,
            'description': 'Drawing pointer',
            'image_path': 'images/gesture_images/one.png',
            'icon': 'images/icon_images/one.png',
            'available': {True: UNAVAILABLE_MODE_IMAGE, False: ''},
            'hand_position_function': get_middle_of_hand},
    # 'hand_position_function': get_one_finger_tip_position},
    "TWO": {'gesture': [True, True, False, False, False],
            'callback': TWO_paint_event,
            'description': 'Change pen color',
            'image_path': 'images/gesture_images/two.png',
            'icon': 'images/icon_images/two.png',
            'available': {True: UNAVAILABLE_MODE_IMAGE, False: ''},
            'hand_position_function': get_middle_of_hand},
    "THREE": {'gesture': [True, True, True, False, False],
              'callback': THREE_paint_event,
              'description': 'Draw rectangle',
              'image_path': 'images/gesture_images/three.png',
              'icon': 'images/icon_images/three.png',
              'available': {True: '', False: ''},
              'hand_position_function': get_middle_of_hand},
    "FOUR": {'gesture': [False, True, True, True, True],
             'callback': FOUR_paint_event,
             'description': 'Draw ellipse',
             'image_path': 'images/gesture_images/four.png',
             'icon': 'images/icon_images/four.png',
             'available': {True: '', False: ''},
             'hand_position_function': get_middle_of_hand},
    "FIVE": {'gesture': [True, True, True, True, True],
             'callback': FIVE_paint_event,
             'image_path': 'images/gesture_images/five.png',
             'icon': 'images/icon_images/five.png',
             'available': {True: '', False: UNAVAILABLE_MODE_IMAGE},
             'description': 'Continue current\ndrawing process',
             'hand_position_function': get_middle_of_hand},
    "SIX": {'gesture': [True, False, False, False, True],
            'callback': SIX_paint_event,
            'description': 'Undo',
            'image_path': 'images/gesture_images/six.png',
            'icon': 'images/icon_images/six.png',
            'available': {True: UNAVAILABLE_MODE_IMAGE, False: ''},
            'hand_position_function': get_middle_of_hand},
    "VICTORY": {'gesture': [False, True, True, False, False],
                'callback': VICTORY_paint_event,
                'description': 'Redo',
                'image_path': 'images/gesture_images/victory.png',
                'icon': 'images/icon_images/victory.png',
                'available': {True: UNAVAILABLE_MODE_IMAGE, False: ''},
                'hand_position_function': get_middle_of_hand},
    "SATAN": {'gesture': [False, True, False, False, True],
              'callback': SATAN_paint_event,
              'description': 'Magnify brush\nthickness',
              'image_path': 'images/gesture_images/satan.png',
              'icon': 'images/icon_images/satan.png',
              'available': {True: UNAVAILABLE_MODE_IMAGE, False: ''},
              'hand_position_function': get_middle_of_hand},
    "THREE_V2": {'gesture': [False, True, True, True, False],
                 'callback': THREE_V2_paint_event,
                 'description': 'Reduce brush\nthickness',
                 'image_path': 'images/gesture_images/three_v2.png',
                 'icon': 'images/icon_images/three_v2.png',
                 'available': {True: UNAVAILABLE_MODE_IMAGE, False: ''},
                 'hand_position_function': get_middle_of_hand},
    "OK": {'gesture': [True, False, False, False, False],
           'callback': OK_paint_event,
           'description': 'Save',
           'image_path': 'images/gesture_images/ok.png',
           'icon': 'images/icon_images/ok.png',
           'available': {True: UNAVAILABLE_MODE_IMAGE, False: ''},
           'hand_position_function': get_middle_of_hand},
    "SPIDERMAN": {'gesture': [True, True, False, False, True],
                  'callback': SPIDERMAN_paint_event,
                  'description': 'Clear window',
                  'image_path': 'images/gesture_images/spiderman.png',
                  'icon': 'images/icon_images/spiderman.png',
                  'available': {True: UNAVAILABLE_MODE_IMAGE, False: ''},
                  'hand_position_function': get_middle_of_hand},
    "QUIT": {'gesture': [False, False, True, True, True],
             'callback': QUIT_paint_event,
             'description': 'Quit program',
             'image_path': 'images/gesture_images/quit.png',
             'icon': 'images/icon_images/quit.png',
             'available': {True: UNAVAILABLE_MODE_IMAGE, False: ''},
             'hand_position_function': get_middle_of_hand},
    "UNKNOWN": {'gesture': None,
                'callback': UNKNOWN_paint_event,
                'description': 'Unknown gesture',
                'image_path': '',
                'icon': 'images/icon_images/unknown.png',
                'available': {True: '', False: ''},
                'hand_position_function': get_middle_of_hand}
}
