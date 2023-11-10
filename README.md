# BlinkerBoard

**BlinkerBoard** project is a communication keyboard for people with disabilities. By eyes blinking and mouth moving selecting characters from the keyboard displayed on the monitor are possible. This give a passibility to build entire sentences which will enable a disabled person who cannot speak and move to have a conversation.

### Dependencies

To use face.py, you need to install the mediapipe package and its dependencies. The easiest way is to install it using pip from the Windows console.
```
pip install mediapipe
```
Additionally, the OpenCV, Tkinter, pillow, pyttsx3 and numpy packages are needed to run the app.py. OpenCV and numpy install automatically as mediapipe dependencies. Tkinter is a package that supports window applications written in Python. pyttsx3 package is used for speech synthesis.

### How to use BlinkerBoard

The main requirement for the application to work is to have a camera/webcam. After starting the program, an application window with a graphic keyboard and a text field appears on the screen. By closing our eyes we can move between the keyboard keys, and by opening our mouth we confirm the selected key.
To jump one key to the right, close your left eye for 0.4 seconds, but no longer than 1 second. To make it easier, when you close your eye and after the required time has passed, the key will change from red to yellow. To jump one key to the left, you also need to close your left eye, but for more than 1 second. The key will first turn yellow, then after a full second it will turn blue, and when you open your eye, the checkmark will move to the left. Using the right eye, we control the jumps between the up-down keys in the same way as for the left eye (down 0.4 s, up 1 s).
To accept the sign, you must open your mouth for 0.4 seconds.
After opening your mouth after 0.4 s, the key will turn yellow. When you close your mouth, the selected character will be added to the text box above the keyboard. Then, after building the entire phrase, you should open your mouth for more than 1 second. After this time, after closing your mouth, the computer will read aloud the phrase written in the text field. See animated gif below.

In order to function properly, the program must work in good lighting conditions.
I wish you successful experiments with BlinkerBoard.
Feel free to ask questions.

![BlinkerBoard](/img/BlinkerBoard.gif)
