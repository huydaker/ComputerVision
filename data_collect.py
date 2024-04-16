import cv2
import pickle

img = cv2.imread("output_image.png")

width, height = (170-100), (245-214)
# cv2.rectangle(img, (51,193), (157,240), (255,0,255), 2) #Thiết kế hình chữ nhật 
# cv2.rectangle(img, (145,193), (214,240), (255,0,255), 2) #Thiết kế hình chữ nhật 
try:
    with open('CarParkPicked_2', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open('CarParkPicked_2', 'wb') as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread("output_image.png")

    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    # Tạo cửa sổ với kích thước bằng với kích thước của ảnh
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("image", img.shape[1], img.shape[0])

    cv2.imshow("image", img)
    cv2.setMouseCallback("image", mouseClick)
    k = cv2.waitKey(10)
    if k == ord('q'):  # Bấm 'q' để thoát
        break
