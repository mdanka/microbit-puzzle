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

ARROW_WE_IMAGE = Image("09090:"
                       "66066:"
                       "99999:"
                       "66066:"
                       "09090")

while True:
  if CURRENT_LEVEL == 1:
    display.scroll('1')
    game_arrows()
    CURRENT_LEVEL = CURRENT_LEVEL + 1

  if CURRENT_LEVEL == 2:
    display.scroll('2')
    game_shake()
    CURRENT_LEVEL = CURRENT_LEVEL + 1

  if CURRENT_LEVEL == 3:
    display.scroll('3')
    game_collect()
    CURRENT_LEVEL = CURRENT_LEVEL + 1

  if CURRENT_LEVEL == 4:
    display.scroll('4')
    game_facedown()
    CURRENT_LEVEL = CURRENT_LEVEL + 1

  if CURRENT_LEVEL > 4:
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

def game_arrows():
  steps = ['left', 'right', 'left', 'left', 'both', 'right', 'both']
  stepIndex = 0
  stepNumber = len(steps)
  while stepIndex < stepNumber:
    currentStep = steps[stepIndex]
    currentImage = None
    if currentStep == 'left':
      currentImage = Image.ARROW_W
    elif currentStep == 'right':
      currentImage = Image.ARROW_E
    else:
      currentImage = ARROW_WE_IMAGE
    display.show(currentImage)
    while True:
      leftPressed = button_a.is_pressed()
      rightPressed = button_b.is_pressed()
      leftPressedOnly = leftPressed and (not rightPressed)
      rightPressedOnly = (not leftPressed) and rightPressed
      bothPressed = leftPressed and rightPressed
      correctPressed = (currentStep == 'left' and leftPressedOnly) or (currentStep == 'right' and rightPressedOnly) or (currentStep == 'both' and bothPressed)
      if correctPressed:
        stepIndex = stepIndex + 1
        break

def game_facedown():
  happyUp = Image("00000:"
                  "09090:"
                  "00000:"
                  "90009:"
                  "09990")
  happyDown = Image("09990:"
                    "90009:"
                    "00000:"
                    "09090:"
                    "00000")
  happyImages = [happyUp, happyDown]
  imageIndex = 0
  imageNumber = len(happyImages)
  while True:
    currentImage = SHAKE_IMAGES[imageIndex]
    display.show(currentImage)
    sleep(1000)
    imageIndex = (imageIndex + 1) % imageNumber
    if accelerometer.was_gesture("face down"):
      return True

def game_collect():
  level = [[0, 0, 0, 5, 0],
           [0, 5, 0, 0, 0],
           [0, 0, 0, 0, 5],
           [0, 5, 0, 5, 0],
           [0, 0, 5, 5, 0]]
  currentPosition = [0, 0]  # column, row
  sleepIndex = 0
  sleepMax = 500
  while True:
    # Left-right
    leftIncrease = button_a.get_presses()
    rightIncrease = button_a.get_presses()
    currentPosition[0] = (currentPosition[0] - leftIncrease + rightIncrease) % 5

    # Down
    sleepIndex = sleepIndex + 1
    if sleepIndex == sleepMax:
      currentPosition[1] = (currentPosition[1] + 1) % 5
      sleepIndex = 0

    # Collect points
    level[currentPosition[0], currentPosition[1]] = 0

    # Render image
    currentImageArray = level[:]
    currentImageArray[currentPosition[0], currentPosition[1]] = 9
    currentImage = microbit.Image(5, 5, currentImageArray)
    display.show(currentImage)

    # Check if done
    flattenedList = [item for sublist in level for item in sublist]
    zeroCount = flattenedList.count(0)
    if zeroCount == 25:
      return True

    # Wait
    sleep(1)

    