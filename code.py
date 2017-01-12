# Add your Python code here. E.g.
from microbit import *

CURRENT_LEVEL = 1

shake0 = Image("00000:"
               "78900:"
               "78900:"
               "78900:"
               "00000")
shake1 = Image("00000:"
               "07890:"
               "07890:"
               "07890:"
               "00000")
shake2 = Image("00000:"
               "00789:"
               "00789:"
               "00789:"
               "00000")
shake3 = Image("00000:"
               "00888:"
               "00888:"
               "00888:"
               "00000")
shake4 = Image("00000:"
               "00987:"
               "00987:"
               "00987:"
               "00000")
shake5 = Image("00000:"
               "09870:"
               "09870:"
               "09870:"
               "00000")
shake6 = Image("00000:"
               "98700:"
               "98700:"
               "98700:"
               "00000")
shake7 = Image("00000:"
               "88800:"
               "88800:"
               "88800:"
               "00000")
SHAKE_IMAGES = [shake0, shake1, shake2, shake3, shake4, shake5, shake6, shake7]

while True:
    if CURRENT_LEVEL == 1:
        display.scroll('1')
        game_shake()
        CURRENT_LEVEL = CURRENT_LEVEL + 1
    
    while True:
        display.scroll('NYERTÉL!!!')
        display.show(Image.HAPPY)
        sleep(2000)


def game_shake():
    imageIndex = 0
    imageNumber = len(SHAKE_IMAGES)
    while True:
        currentImage = SHAKE_IMAGES[imageIndex]
        display.show(currentImage)
        sleep(100)
        imageIndex = (imageIndex + 1) % imageNumber
        if accelerometer.was_gesture("shake"):
            return True

