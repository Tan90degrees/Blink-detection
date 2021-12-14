import cv2 as cv
import dlib
import os
import camera
import get_model

from write_data import write_txt
from imutils import face_utils
from scipy.spatial import distance


def ear_value(eye):
    ear = (distance.euclidean(eye[1], eye[5]) + distance.euclidean(eye[2], eye[4])) / (
        distance.euclidean(eye[0], eye[3]) * 2
    )
    return ear


class GetEar:
    def __init__(self, filename):
        get_model.download_model()
        pwd = os.getcwd()
        model_path = os.path.join(pwd, "models")
        shape_detector_path = os.path.join(
            model_path, "shape_predictor_68_face_landmarks.dat"
        )
        data_path = os.path.join(pwd, "data")
        self.data = os.path.join(data_path, filename)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(shape_detector_path)
        self.input_data = open(self.data, "w")
        self.Cam = camera.Camera(0)
        self.cam = self.Cam.open()
        self.frame_count = 0
        self.ear_vector = []
        self.data_count = 0
        self.cam_flag, self.video_frame = self.cam.read()

    def ear(self):
        gray_frame = cv.cvtColor(self.video_frame, cv.COLOR_BGR2GRAY)
        checks = self.detector(gray_frame, 0)
        for check in checks:
            self.frame_count = self.frame_count + 1
            points = self.predictor(gray_frame, check)
            np_points = face_utils.shape_to_np(points)
            left_points = np_points[36:42]
            right_points = np_points[42:48]
            left_ear = ear_value(left_points)
            right_ear = ear_value(right_points)
            equal_ear = (left_ear + right_ear) / 2
            write_txt(self.input_data, equal_ear, self.ear_vector)
            self.data_count = self.data_count + 1
            cv.putText(
                self.video_frame,
                "left_ear: {:.3f}".format(left_ear),
                (10, 30),
                cv.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 0, 0),
                1,
            )
            cv.putText(
                self.video_frame,
                "right_ear: {:.3f}".format(right_ear),
                (10, 50),
                cv.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 0, 0),
                1,
            )
            cv.putText(
                self.video_frame,
                "frame_count: {:d}".format(self.frame_count),
                (250, 30),
                cv.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 0, 0),
                1,
            )
            left_eye_hull = cv.convexHull(left_points)
            right_eye_hull = cv.convexHull(right_points)
            cv.drawContours(self.video_frame, [left_eye_hull], -1, (0, 255, 0), 1)
            cv.drawContours(self.video_frame, [right_eye_hull], -1, (0, 255, 0), 1)

    def show_video(self):
        cv.imshow("BLINK_CHECK", self.video_frame)
