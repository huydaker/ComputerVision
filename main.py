import cv2
import pickle
import cvzone
import numpy as np

cap = cv2.VideoCapture('carPark_2.mp4')
with open('CarParkPicked_2', 'rb') as f:
        posList = pickle.load(f)
width, height = (170-100), (240-214)
 
def check(imgPro):
    space = 0

    for pos in posList:
        x, y = pos
        
        imgCrop = imgPro[y:y+height,x:x+width]
        # cv2.imshow(str(x+y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count),(x,y+height-10), scale=1, thickness=2, offset=0)
        # cvzone.putTextRect(img, str(count),(x,y+height-10), scale=1.5, thickness=2, offset=0, colorR=(0,0,255))

        if count<230:
            color = (0,255,0)
            thickness = 5
            space +=1
        else:
            color = (0,0,255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), color, thickness)
    cvzone.putTextRect(img, f'Parking Space: {space}/{len(posList)}', (100,50), scale=3)


while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                        cv2.THRESH_BINARY_INV, 25 ,16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3,3), np.int8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)



    check(imgDilate)

    # for pos in posList:
        # cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255,0,255), 2)
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Image", img.shape[1], img.shape[0])

    cv2.imshow("Image", img)
    cv2.imshow("ImageGray", imgGray)
    cv2.imshow("ImageBlur", imgBlur)
    cv2.imshow("ImageThreshold", imgThreshold)
    cv2.imshow("ImageMedian", imgMedian)
    k = cv2.waitKey(10)
    if k == ord('q'):  # Bam q de thoat
        break