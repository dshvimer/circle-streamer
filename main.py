import numpy as np
import cv2
import socket
import ctypes

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ("127.0.0.1" , 8000)
sock.connect(address)

def main():
    cap = cv2.VideoCapture("./circles.mp4")
    while(cap.isOpened()):
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        circles = [cv2.minEnclosingCircle(c) for c in contours]

        for circle in circles:
            ((x,y),radius) = circle
            cv2.circle(img,(int(x),int(y)), int(radius),(0, 255, 0), 2)
            data = bytearray()
            data.append(ctypes.c_uint8(int(x)).value)
            data.append(ctypes.c_uint8(int(y)).value)
            # data.append(ctypes.c_uint8(int(radius)).value)
            sock.send(data)

        cv2.imshow('frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def shutdown():
    cv2.destroyAllWindows()
    sock.close()

if __name__ == "__main__":
    # execute only if run as a script
    main()
