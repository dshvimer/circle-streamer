import numpy as np
import cv2
import socket
import ctypes
import math

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ("127.0.0.1" , 8000)
sock.connect(address)

def process(img):
    blur = cv2.GaussianBlur(img, (3,3), 0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 75, 255, cv2.THRESH_BINARY)
    # mask = cv2.erode(thresh, None , iterations = 1)
    # mask = cv2.dilate(mask, None , iterations = 1)
    # return mask
    return thresh

def isCircular(con):
    area = cv2.contourArea(con)
    perimeter = cv2.arcLength(con, True)
    if perimeter == 0:
        return False
    circularity = 4*math.pi*(area/ (perimeter**2))
    if (area < 20) and (area > 40):
        return False
    elif perimeter == 0:
        return False
    elif circularity < 0.75:
        return False
    else:
        return True


def main():
    # cap = cv2.VideoCapture("./circles.mp4")
    cap = cv2.VideoCapture(0)
    while(cap.isOpened()):
        _, img = cap.read()
        img = cv2.resize(img, (0, 0), fy=0.25, fx=0.25)
        # yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        # yuv[:,:,0] = cv2.equalizeHist(yuv[:,:,0])
        # img = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)

        mask = process(img)

        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [c for c in contours if isCircular(c)]
    
        circles = [cv2.minEnclosingCircle(c) for c in contours]

        data = bytearray()
        for circle in circles:
            ((x,y),radius) = circle
            cv2.circle(img,(int(x),int(y)), int(radius),(0, 255, 0), 2)
            data.append(ctypes.c_uint8(int(x)).value)
            data.append(ctypes.c_uint8(int(y)).value)
            # data.append(ctypes.c_uint8(int(radius)).value)
        sock.send(data)

        tile = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        images = np.vstack((img, tile))
        cv2.imshow('frame', images)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def shutdown():
    cv2.destroyAllWindows()
    sock.close()

if __name__ == "__main__":
    # execute only if run as a script
    main()
