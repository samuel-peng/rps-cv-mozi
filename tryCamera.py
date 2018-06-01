import time

import cv2
import numpy as np

import timer
import filters

class Camera():

    def __init__(self, size=10, frameRate=40, hflip=False, vflip=False):
        self.active = False
        cv2.namedWindow("Preview")
        try:
            if type(size) is not int:
                raise TypeError("Size must be an integer")
            elif 1 <= size and size <= 51:
                self.size = size
                self.hRes = size * 64
                self.vRes = size * 48
            else:
                raise ValueError("Size must be in range 1 to 51")
        except  TypeError or ValueError:
            raise
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, vRes)
        self.cam.set(4, hRes)

    def close(self):
        self.stop()
        self.cam.release()

    def rotatedImage(self, image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        #rows, cols = image.shape
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        #result = cv2.warpAffine(image, rot_mat,(cols, rows))
        return result

    def startPreview(self):
        if self.cam.isOpened():
            rval, frame = self.vc.read()
        else:
            rval = false
        while rval:
            cv2.imshow("Preview", self.rotatedImage(frame, 90))
            rval, frame = self.cam.read()
            key = cv2.waitKey(20)
            if key == 27:
                break
        cv2.destroyWindow("Preview")

if __name__=="__main__":
    c = Camera(10, 40, False, False)
    c.startPreview()
