# here are usefull utilities for app main loop code shortening

import time
from PIL import Image, ImageDraw, ImageFont
from face import FaceAnalyzer

# SImple timer class for time measuring
class Timer:
    def __init__(self, units = 's', precision = 0):
        self.start_point = 0
        self.end_point = 0
        self.total_time = 0
        self.elapsed_time = 0
        self.check_point = 0
        self.ticking = False
        self.units = units
        self.precision = precision
    
    def start(self):
        if self.ticking == False:
            self.start_point = time.time()
            self.ticking = True
    
    def stop(self) -> float:
        if self.ticking:
            self.end_point = time.time()
            self.total_time = self.end_point - self.start_point
            self.ticking = False
        if self.units == 's':
            return round(self.total_time, self.precision)
        elif self.units == 'ms':
            return round(self.total_time * 1000, self.precision)
    
    def check(self) -> float:
        if self.ticking:
            self.check_point = time.time()
            self.elapsed_time = self.check_point - self.start_point
        if self.units == 's':
            return round(self.elapsed_time, self.precision)
        elif self.units == 'ms':
            return round(self.elapsed_time * 1000, self.precision)


# Buttons draw on the keyboard
class Button:
    def __init__(self, xy, size, color, position, bg_img):
        self.xy = xy
        self.size = size
        self.color = color
        self.position = position
        self.bg_img = bg_img
    
    def draw_button(self, text_):
        draw = ImageDraw.Draw(self.bg_img)
        draw.rectangle((self.xy[0], self.xy[1], self.xy[0]+self.size[0], self.xy[1]+self.size[1]), fill=self.color)
        draw_font = ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf', 40)
        draw.text((self.xy[0]+7, self.xy[1]+5, self.xy[0]+self.size[0], self.xy[1]+self.size[1]), text=text_, font=draw_font, fill=(0,0,0))


# Draw the full keyboard
def draw_board(img, items_list, delta, size):        
    for i in range(size[0]):
        for j in range(size[1]):
            new_button = Button((10+delta*j, 50+delta*i), (70, 70), (255,255,255), 0, img)
            new_button.draw_button(items_list[i][j])

# find element in multidimensional list
def find(list_, element):
    for row, i in enumerate(list_):
        try:
            column = i.index(element)
        except ValueError:
            continue
        return row, column
    return -1

# find dimmension of 2D list
def dimension(x):
    if type(x) == list and len(x) != 0:
        if type(x[0]) == list:
            return (len(x), len(x[0]))
        else:
            return len(x)
    elif type(x) == list and len(x) == 0:
        return 0
    else:
        return None

# face analyzing function
my_face = FaceAnalyzer()
def analyze(img):
    l, r, m = None, None, None
    l_e, r_e, l_i, r_i, l_b, r_b, lips = my_face.face_features(img, True, False, False, True)
    if l_e != None and r_e != None:
        l, r = my_face.eyes_status(l_e, r_e)
    if lips != None:
        m = my_face.lips_status(lips)
    return l, r, m

# keyboard definition
key_list = [['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
           ['A', 'Ą', 'B', 'C', 'Ć', 'D', 'E', 'Ę', 'F', 'G'],
           ['H', 'I', 'J', 'K', 'L', 'Ł', 'M', 'N', 'Ń', 'O'],
           ['Ó', 'P', 'R', 'S', 'Ś', 'T', 'U', 'V', 'W', 'X'],
           ['Y', 'Z', 'Ź', 'Ż', ' ', 'BS', '+', '-', '*', '=']]

