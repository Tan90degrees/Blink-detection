import cv2 as cv
import dlib
import getpath
import camera
import draw
from eye import ear_value
from imutils import face_utils


def check_blink():
    THRESHOLD = 0.3
    AVG_THRESHOLD = 0.25
    pic_path = getpath.get_3rd_path('result', 'line.png')
    shape_detector_path = getpath.get_3rd_path('models', 'shape_predictor_68_face_landmarks.dat')
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_detector_path)
    Cam = camera.Camera(0)
    frame_count = 0
    blink_count = 0
    cam = Cam.open()
    drawline = draw.Draw()
    while cam.isOpened():
        frame_count = frame_count + 1
        flag, video_frame = cam.read()
        gray_frame = cv.cvtColor(video_frame, cv.COLOR_BGR2GRAY)
        checks = detector(gray_frame, 0)
        for check in checks:
            print('-' * 40)
            points = predictor(gray_frame, check)
            np_points = face_utils.shape_to_np(points)
            left_points = np_points[36:42]
            right_points = np_points[42:48]
            left_ear = ear_value(left_points)
            right_ear = ear_value(right_points)
            equal_ear = (left_ear + right_ear) / 2
            drawline.update(equal_ear, 0.033)
            if right_ear <= THRESHOLD:
                print('Right eye blink!')
            if left_ear <= THRESHOLD:
                print('Left eye blink!')
            if equal_ear <= AVG_THRESHOLD:
                print('All eyes blink!')
                blink_count = blink_count + 1
            cv.putText(video_frame, 'left_ear: {:.3f}'.format(left_ear), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.75,
                       (255, 0, 0), 1)
            cv.putText(video_frame, 'right_ear: {:.3f}'.format(right_ear), (10, 50), cv.FONT_HERSHEY_SIMPLEX, 0.75,
                       (255, 0, 0), 1)
            cv.putText(video_frame, 'blink_count: {:d}'.format(blink_count), (250, 30), cv.FONT_HERSHEY_SIMPLEX, 0.75,
                       (255, 0, 0), 1)
            cv.putText(video_frame, 'frame_count: {:d}'.format(frame_count), (250, 50), cv.FONT_HERSHEY_SIMPLEX, 0.75,
                       (255, 0, 0), 1)
            left_eye_hull = cv.convexHull(left_points)
            right_eye_hull = cv.convexHull(right_points)
            cv.drawContours(video_frame, [left_eye_hull], -1, (0, 255, 0), 1)
            cv.drawContours(video_frame, [right_eye_hull], -1, (0, 255, 0), 1)
        cv.imshow("BLINK_CHECK", video_frame)
        if cv.waitKey(1) & 0xFF == ord("q"):
            drawline.save_pic(pic_path)
            draw.draw_stop()
            break
    Cam.close()
    cv.destroyAllWindows()


if __name__ == '__main__':
    check_blink()
