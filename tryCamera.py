import cv2
import numpy as np

def rotateImage(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

class Camera():

    cv2.namedWindow("Preview")
    vc = cv2.VideoCapture(0)
    def startPreview(self):
        if vc.isOpened():
            rval, frame = vc.read()
        else:
            rval = false
        while rval:
            cv2.imshow("Preview", rotateImage(frame, 90))
            rval, frame = vc.read()
            key = cv2.waitKey(20)
            if key == 27:
                break
        cv2.destroyWindow("Preview")
