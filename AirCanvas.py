import HandTracking as htm
import cv2
import numpy as np
import RectBoxes as Rb

wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.HandDetector(detectionCon=0.8, maxHands=1)

canvas = np.zeros((720, 1280, 3), np.uint8)

# Initialising
px, py = 0, 0
brushColor = (255, 0, 0)
brushSize = 5
eraserSize = 20

colorsBtn = Rb.RectBox(200, 0, 100, 100, (120, 0, 0), 'Colors')

colors = [
    Rb.RectBox(x, 0, 70, 100, color) for x, color in [
        (300, (0, 0, 255)),     # red
        (370, (138, 10, 242)),  # pink
        (440, (255, 0, 0)),     # blue
        (510, (255, 255, 0)),   # cyan
        (580, (0, 255, 0)),     # green
        (650, (0, 255, 255)),   # yellow
        (720, (5, 132, 250)),   # orange
    ]
]
new_color_box = Rb.RectBox(790, 0, 100, 100, (0, 0, 0), "Erase")

colors.insert(5, new_color_box)
clear = Rb.RectBox(900, 0, 100, 100, (100, 100, 100), "Clear")  # clear

pens = []
for i, penSize in enumerate(range(5, 25, 5)):
    pens.append(Rb.RectBox(1100, 50 + 100 * i, 100, 100, (50, 50, 50), str(penSize)))

penBtn = Rb.RectBox(1100, 0, 100, 50, brushColor, 'Pen')
boardBtn = Rb.RectBox(50, 0, 100, 100, (255, 255, 0), 'Board')
whiteBoard = Rb.RectBox(50, 120, 1020, 580, (255, 255, 255), alpha=0.6)

coolingCounter = 20
hideBoard = True
hideColors = True
hidePenSizes = True

while True:

    if coolingCounter:
        coolingCounter -= 1
        print(coolingCounter)

    success, img = cap.read()

    img = cv2.resize(img, (1280, 720))
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        upFingers = detector.fingersUp()

        if upFingers:
            x, y = lmList[8][1], lmList[8][2]
            if upFingers[1] and not whiteBoard.onButton(x, y):
                px, py = 0, 0
                if not hidePenSizes:  # Pen Size buttons
                    for pen in pens:
                        if pen.onButton(x, y):
                            brushSize = int(pen.text)
                            eraserSize = int(pen.text)
                            pen.alpha = 0
                        else:
                            pen.alpha = 0.5

                if not hideColors:  # Colors
                    for c in colors:
                        if c.onButton(x, y):
                            brushColor = c.color
                            c.alpha = 0
                        else:
                            c.alpha = 0.5

                if clear.onButton(x, y):  # clear button
                    clear.alpha = 0
                    canvas = np.zeros((720, 1280, 3), np.uint8)
                else:
                    clear.alpha = 0.5

                if colorsBtn.onButton(x, y) and not coolingCounter: # color button toggle
                    coolingCounter = 50
                    colorsBtn.alpha = 0
                    hideColors = not hideColors
                    colorsBtn.text = 'Colors' if hideColors else 'Close'
                else:
                    colorsBtn.alpha = 0.5

                if penBtn.onButton(x, y) and not coolingCounter: # pen button
                    coolingCounter = 50
                    penBtn.alpha = 0
                    hidePenSizes = not hidePenSizes
                    penBtn.text = 'Pen' if hidePenSizes else 'Close'
                else:
                    penBtn.alpha = 0.5

                if boardBtn.onButton(x, y) and not coolingCounter:  # opening board button toggle
                    coolingCounter = 50
                    boardBtn.alpha = 0
                    hideBoard = not hideBoard
                    boardBtn.text = 'Board' if hideBoard else 'Close'
                else:
                    boardBtn.alpha = 0.5

            # To draw with index finger
            elif upFingers[1] and not upFingers[2]:
                if whiteBoard.onButton(x, y) and not hideBoard:
                    cv2.circle(img, (lmList[8][1], lmList[8][2]), brushSize, brushColor, 3)
                    if px == 0 and py == 0:
                        px, py = lmList[8][1], lmList[8][2]
                    if brushColor == (0, 0, 0):
                        cv2.line(canvas, (px, py), (lmList[8][1], lmList[8][2]), brushColor, eraserSize)
                    else:
                        cv2.line(canvas, (px, py), (lmList[8][1], lmList[8][2]), brushColor, brushSize)
                    px, py = lmList[8][1], lmList[8][2]

            else:
                px, py = 0, 0

    colorsBtn.drawRect(img)
    cv2.rectangle(img, (colorsBtn.x, colorsBtn.y), (colorsBtn.x + colorsBtn.w, colorsBtn.y + colorsBtn.h),
                  (255, 255, 255), 2)

    boardBtn.drawRect(img)
    cv2.rectangle(img, (boardBtn.x, boardBtn.y), (boardBtn.x + boardBtn.w, boardBtn.y + boardBtn.h), (255, 255, 255),
                  2)

    if not hideBoard:
        whiteBoard.drawRect(img)
        canvasGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(canvasGray, 20, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, canvas)

    if not hideColors:
        for c in colors:
            c.drawRect(img)
            cv2.rectangle(img, (c.x, c.y), (c.x + c.w, c.y + c.h), (255, 255, 255), 2)

        clear.drawRect(img)
        cv2.rectangle(img, (clear.x, clear.y), (clear.x + clear.w, clear.y + clear.h), (255, 255, 255), 2)

    penBtn.color = brushColor
    penBtn.drawRect(img)
    cv2.rectangle(img, (penBtn.x, penBtn.y), (penBtn.x + penBtn.w, penBtn.y + penBtn.h), (255, 255, 255), 2)
    if not hidePenSizes:
        for pen in pens:
            pen.drawRect(img)
            cv2.rectangle(img, (pen.x, pen.y), (pen.x + pen.w, pen.y + pen.h), (255, 255, 255), 2)

    cv2.imshow('video', img)
    x = cv2.waitKey(1)
    if x == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
