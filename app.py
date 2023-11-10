import tkinter as Tk
from PIL import Image
from PIL import ImageTk
import pyttsx3
import cv2
from utilities import Timer, find, draw_board, Button, key_list, analyze

# Constants definition
SHORT_BLINK = 0.4 # measured in seconds
LONG_BLINK = 1.0
LONG_BLINK_APPROVE = 2.0
DELTA = 90 # buttons shift on keyboard

CAMERA = 0 # or 1, 2, 3 according to connected webcams/cameras
CAMERA_RESOLUTION = (640, 480)
CAMERA_BRIGHTNESS = 100

# Main window parameters
WINDOW_DIM = '900x650'

# Speach synthesis activation
synthesis = pyttsx3.init()
voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PL-PL_PAULINA_11.0'
#voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0" 
synthesis.setProperty('voice', voice_id)
synthesis.setProperty('rate', 125)

# camera
camera = cv2.VideoCapture(CAMERA + cv2.CAP_DSHOW)
#set brightness
camera.set(cv2.CAP_PROP_BRIGHTNESS, CAMERA_BRIGHTNESS) 
# set width
camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_RESOLUTION[0]) 
# set height
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_RESOLUTION[1])

# Main window definition
root = Tk.Tk()
root.geometry(WINDOW_DIM)
root.resizable(width=False, height=False)
root.wm_title('BlinkBoard')

# String for message keeping
message = ''
# Array for active button possition monitoring
position = [[0 for x in range(10)] for y in range(5)]
position[0][0] = 1

# Background definition and keyboard
bcg = Image.new(mode='RGB', size=(900, 600), color=(0, 0, 0))
draw_board(bcg, key_list, DELTA, (5, 10))
new_button = Button((10, 50), (70, 70), (255,0,0), 0, bcg)
new_button.draw_button(key_list[0][0])

# Eyes and mouth status 0 - left eye, 1 - right eye, 2 - mouth
face_status = [None, None, None]

# Timer for eyes and mouth states open/closed
# l_t - left eye timer, r_t - right eye timer, c_t - mouth timer
l_t = Timer(units='s', precision=2)
r_t = Timer(units='s', precision=2)
c_t = Timer(units='s', precision=2)

def main():
    global message, face_status, SHORT_BLINK, LONG_BLINK, LONG_BLINK_APPROVE
    left = 0
    right = 0
    c = 0
    _, img = camera.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Face analysis, in result gives status of eyes and mouth open/closed
    face_status[0], face_status[1], face_status[2] = analyze(img)
    # Times analysis
    if face_status is not [None, None, None]:
        # Left eye timing
        if l_t.ticking == False and face_status[0] == False:
            l_t.start()
        if l_t.ticking and face_status[0] == False:
            x, y = find(position, 1)
            l_t.check()
            if l_t.elapsed_time >= SHORT_BLINK and l_t.elapsed_time < LONG_BLINK:
                new_button = Button((10+DELTA*y, 50+DELTA*x), (70, 70), (255,255,0), 0, bcg)
                new_button.draw_button(key_list[x][y])
            elif l_t.elapsed_time > LONG_BLINK:
                new_button = Button((10+DELTA*y, 50+DELTA*x), (70, 70), (0,255,255), 0, bcg)
                new_button.draw_button(key_list[x][y])
        if l_t.ticking and face_status[0]:
            end = l_t.stop()
            if end >= SHORT_BLINK and end < LONG_BLINK:
                left = 1
            elif end > LONG_BLINK:
                left = 2
        # Right eye timing
        if r_t.ticking == False and face_status[1] == False:
            r_t.start()
        if r_t.ticking and face_status[1] == False:
            x, y = find(position, 1)
            r_t.check()
            if r_t.elapsed_time >= SHORT_BLINK and r_t.elapsed_time < LONG_BLINK:
                new_button = Button((10+DELTA*y, 50+DELTA*x), (70, 70), (255,255,0), 0, bcg)
                new_button.draw_button(key_list[x][y])
            elif r_t.elapsed_time > LONG_BLINK:
                new_button = Button((10+DELTA*y, 50+DELTA*x), (70, 70), (0,255,255), 0, bcg)
                new_button.draw_button(key_list[x][y])
        if r_t.ticking and face_status[1]:
            end = r_t.stop()
            if end >= SHORT_BLINK and end < LONG_BLINK:
                right = 1
            elif end > LONG_BLINK:
                right = 2
        # Mouth timing
        if c_t.ticking == False and face_status[2] == True:
            c_t.start()
        if c_t.ticking and face_status[2] == True:
            x, y = find(position, 1)
            c_t.check()
            if c_t.elapsed_time >= SHORT_BLINK and c_t.elapsed_time < LONG_BLINK_APPROVE:
                new_button = Button((10+DELTA*y, 50+DELTA*x), (70, 70), (255,255,0), 0, bcg)
                new_button.draw_button(key_list[x][y])
            elif c_t.elapsed_time > LONG_BLINK_APPROVE:
                new_button = Button((10+DELTA*y, 50+DELTA*x), (70, 70), (0,255,255), 0, bcg)
                new_button.draw_button(key_list[x][y])
        if c_t.ticking and face_status[2] == False:
            end = c_t.stop()
            if end >= SHORT_BLINK and end < LONG_BLINK_APPROVE:
                c = 1
            elif end > LONG_BLINK_APPROVE:
                c = 2  
    # Movements on the keyboard
    if left == 1:
        draw_board(bcg, key_list, DELTA, (5, 10))
        x, y = find(position, 1)
        if y < 9:
            new_button = Button((10+DELTA*(y+1), 50+DELTA*x), (70, 70), (255,0,0), 0, bcg)
            new_button.draw_button(key_list[x][y+1])
            position[x][y] = 0
            position[x][y+1] = 1
        elif y == 9:
            new_button = Button((10+DELTA*(0), 50+DELTA*x), (70, 70), (255,0,0), 0, bcg)
            new_button.draw_button(key_list[x][0])
            position[x][y] = 0
            position[x][0] = 1
    if left == 2:
        draw_board(bcg, key_list, DELTA, (5, 10))
        x, y = find(position, 1)
        if y > 0:
            new_button = Button((10+DELTA*(y-1), 50+DELTA*x), (70, 70), (255,0,0), 0, bcg)
            new_button.draw_button(key_list[x][y-1])
            position[x][y] = 0
            position[x][y-1] = 1
        elif y == 0:
            new_button = Button((10+DELTA*(9), 50+DELTA*x), (70, 70), (255,0,0), 0, bcg)
            new_button.draw_button(key_list[x][9])
            position[x][y] = 0
            position[x][9] = 1
    if right == 1:
        draw_board(bcg, key_list, DELTA, (5, 10))
        x, y = find(position, 1)
        if x < 4:
            new_button = Button((10+DELTA*(y), 50+DELTA*(x+1)), (70, 70), (255,0,0), 0, bcg)
            new_button.draw_button(key_list[x+1][y])
            position[x][y] = 0
            position[x+1][y] = 1
        elif x == 4:
            new_button = Button((10+DELTA*(y), 50+DELTA*0), (70, 70), (255,0,0), 0, bcg)
            new_button.draw_button(key_list[0][y])
            position[x][y] = 0
            position[0][y] = 1
    if right == 2:
        draw_board(bcg, key_list, DELTA, (5, 10))
        x, y = find(position, 1)
        if x > 0:
            new_button = Button((10+DELTA*(y), 50+DELTA*(x-1)), (70, 70), (255,0,0), 0, bcg)
            new_button.draw_button(key_list[x-1][y])
            position[x][y] = 0
            position[x-1][y] = 1
        elif x == 0:
            new_button = Button((10+DELTA*(y), 50+DELTA*4), (70, 70), (255,0,0), 0, bcg)
            new_button.draw_button(key_list[4][y])
            position[x][y] = 0
            position[4][y] = 1
    if c == 1:
        x, y = find(position, 1)
        if key_list[x][y] != 'BS':
            message += key_list[x][y]
            text_field.insert(Tk.END, key_list[x][y])
        else:
            message = message[:-1]
            text_field.delete(1.0, Tk.END)
            text_field.insert(Tk.END, message)
    if c == 2:
        synthesis.say(message)
        synthesis.runAndWait()
        synthesis.stop()
        message = ''
        text_field.delete(1.0, Tk.END)
    imgtk = ImageTk.PhotoImage(image=bcg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    root.after(8, main)
    
# Keyboard display
imgtk = ImageTk.PhotoImage(image=bcg)

# Text field
text_field = Tk.Text(master=root, height=5, background='lightgray')
text_field.pack(side=Tk.TOP, fill='both')

# Field for keyboard display
lmain = Tk.Label(master=root, height=900, width=850)
lmain.pack(side=Tk.TOP, fill='both')
lmain.imgtk = imgtk
lmain.configure(image=imgtk)

# Main loop with logic
main()

# Window app main loop
root.mainloop()

