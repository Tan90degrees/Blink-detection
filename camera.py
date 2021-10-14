import cv2 as cv


class Camera:

    def __init__(self, cam_num) -> None:
        self.cam = cv.VideoCapture(cam_num)
        self.fps = int(self.cam.get(cv.CAP_PROP_FPS))
        self.width = int(self.cam.get(cv.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cam.get(cv.CAP_PROP_FRAME_HEIGHT))

    def open(self) -> cv.VideoCapture:
        if not self.cam.isOpened():
            print("Camera open failed!\n")
            exit()
        else:
            print("Camera is opened!")
            return self.cam

    def close(self):
        self.cam.release()
        print("Camera is closed!\n")

    def para(self):
        return self.fps, self.width, self.height
