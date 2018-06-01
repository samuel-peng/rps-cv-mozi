import time

import cv2
import numpy as np
import rpsimgproc as imp

import timer
import filters
import imutils

from colorBalance import colorBalance

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
        self.cam.set(3, size * 48) #width
        self.cam.set(4, size * 64) #height

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

    def processImg(self, image):
       #return imutils.rotate_bound(colorBalance(image), 270)
       return imp.fastRotate(colorBalance(image))


    def startPreview(self):
        if self.cam.isOpened():
            rval, frame = self.cam.read()
        else:
            rval = false
        while rval:
            #cv2.imshow("Preview", self.rotatedImage(frame, 90))
            self.processedImg = self.processImg(frame)
            cv2.imshow("Preview", self.processedImg)
            rrval, frame = self.cam.read()
            key = cv2.waitKey(20)
            if key == 27:
                break
        cv2.destroyWindow("Preview")

if __name__=="__main__":
    c = Camera(10, 40, False, False)
    c.startPreview()
