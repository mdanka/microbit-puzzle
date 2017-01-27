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

happyUp = Image("00000:"
                "09090:"
                "00000:"
                "90009:"
                "09990")
happyRight = Image("09000:"
                   "90090:"
                   "90000:"
                   "90090:"
                   "09000")
happyDown = Image("09990:"
                  "90009:"
                  "00000:"
                  "09090:"
                  "00000")
happyLeft = Image("00090:"
                  "09009:"
                  "00009:"
                  "09009:"
                  "00090")
HAPPY_IMAGES = [happyUp, happyRight, happyDown, happyLeft]

ARROW_WE_IMAGE = Image("09090:"
                       "66066:"
                       "99999:"
                       "66066:"
                       "09090")

def game_shake():
  imageIndex = 0
  imageNumber = len(SHAKE_IMAGES)
  while True:
    currentImage = SHAKE_IMAGES[imageIndex]
    display.show(currentImage)
    sleep(50)
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
  happyImages = [happyUp, happyDown]
  imageIndex = 0
  imageNumber = len(happyImages)
  time = 0
  isDownDone = False
  while True:
    time = (time + 1) % 1000
    if time > 500:
      imageIndex = 1
    else:
      imageIndex = 0
    currentImage = happyImages[imageIndex]
    display.show(currentImage)
    gesture = accelerometer.current_gesture()
    if gesture == "face down":
      isDownDone = True
    if isDownDone and gesture == "face up":
      return True

def game_collect():
  level = [[0, 0, 0, 5, 0],
           [0, 5, 0, 0, 0],
           [0, 0, 0, 0, 5],
           [0, 5, 0, 5, 0],
           [0, 0, 5, 5, 0]]
  currentPosition = [0, 0]  # row, column
  sleepIndex = 0
  sleepMax = 5
  while True:
    # Left-right
    leftIncrease = button_a.get_presses()
    rightIncrease = button_b.get_presses()
    currentPosition[1] = (currentPosition[1] - leftIncrease + rightIncrease) % 5

    # Down
    sleepIndex = sleepIndex + 1
    if sleepIndex == sleepMax:
      currentPosition[0] = (currentPosition[0] + 1) % 5
      sleepIndex = 0

    # Collect points
    level[currentPosition[0]][currentPosition[1]] = 0

    # Render image
    # currentImageArray = map(lambda sublist: sublist[:], level)
    currentImageArray = [sublist[:] for sublist in level]
    currentImageArray[currentPosition[0]][currentPosition[1]] = 9
    currentImageArrayWithStringEntries = map(lambda sublist: map(str, sublist), currentImageArray)
    currentImageArrayWithStringRows = map(lambda sublist: ''.join(sublist), currentImageArrayWithStringEntries)
    currentImageArrayWithStringMatrix = ':'.join(currentImageArrayWithStringRows)
    currentImage = Image(currentImageArrayWithStringMatrix)
    display.show(currentImage)

    # Check if done
    flattenedList = [item for sublist in level for item in sublist]
    zeroCount = flattenedList.count(0)
    if zeroCount == 25:
      return True

    # Wait
    sleep(1)

    
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
      display.scroll('NYERTEL!!!')
      display.show(HAPPY_IMAGES, delay=200)
      display.show(HAPPY_IMAGES, delay=200)
      display.show(HAPPY_IMAGES, delay=200)
      # sleep(2000)
