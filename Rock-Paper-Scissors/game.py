import cv2
import time
import os
import random
import HandTrackingModule as htm

wCam, hCam = 1280, 960

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "FingerImages"
myList = os.listdir(folderPath)
print(myList)

overlayList = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))
pTime = 0

detector = htm.handDetector(detectionCon=0.65)
comp_lst = ["R", "S", "P"]

while True:
    # 1. Import image
    success, img = cap.read()

    # 2. Find Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    # Variables for the Game
    winner = -1
    p1 = None
    p2 = random.choice(comp_lst)

    if len(lmList) != 0:
        # 3. Check which fingers are up
        fingers = detector.fingersUp()

        # 4. Player's - Scissors, Rock and Paper
        if fingers[0] == 0 and fingers[1] and fingers[2] and fingers[3] == 0 and fingers[4] == 0:
            p1 = "S"
            h, w, c = overlayList[1].shape
            img[0:h, 0:w] = overlayList[1]
            cv2.putText(img, "Scissors", (40, 375), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 12)

        elif fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            p1 = "R"
            h, w, c = overlayList[5].shape
            img[0:h, 0:w] = overlayList[5]
            cv2.putText(img, "Rock", (40, 375), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 12)

        elif fingers[0] and fingers[1] and fingers[2] and fingers[3] and fingers[4]:
            p1 = "P"
            h, w, c = overlayList[4].shape
            img[0:h, 0:w] = overlayList[4]
            cv2.putText(img, "Paper", (40, 375), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 12)

    # 5. Game Logic
    if p1 != None:
        # 6. Computer's - Scissors, Rock and Paper
        if p2 == "S":
            h, w, c = overlayList[1].shape
            img[0:h, wCam - w:wCam] = overlayList[1]
            cv2.putText(img, "C-Scissor", (800, 375), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 12)

        elif p2 == "R":
            h, w, c = overlayList[5].shape
            img[0:h, wCam - w:wCam] = overlayList[5]
            cv2.putText(img, "C - Rock", (800, 375), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 12)

        elif p1 == "P":
            h, w, c = overlayList[4].shape
            img[0:h, wCam - w:wCam] = overlayList[4]
            cv2.putText(img, "C - Paper", (800, 375), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 12)

        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        if winner == 0:
            cv2.putText(img, "You Won!!", (400, 600), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 10)
            cv2.putText(img, f"You: {p1} and Comp: {p2}", (100, 700), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 10)
            time.sleep(0.5)
        elif winner == 1:
            cv2.putText(img, "You Lost!!", (400, 600), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 10)
            cv2.putText(img, f"You: {p1} and Comp: {p2}", (100, 700), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 10)
            time.sleep(0.5)
        elif winner == -1:
            cv2.putText(img, "It's a Tie!!", (400, 600), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 10)
            cv2.putText(img, f"You: {p1} and Comp: {p2}", (100, 700), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 10)
            time.sleep(0.5)
    else:
        cv2.putText(img, "Make a move", (400, 700), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 10)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
