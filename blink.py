from re import T
import time
import cv2 as cv
import dlib
import getpath
import camera

# import draw
import get_model
import trandata
from eye import ear_value
from mouth import mar_value
from imutils import face_utils


def check_blink():
    get_model.download_landmarks_model()
    THRESHOLD = 0.3
    AVG_THRESHOLD = 0.25
    # pic_path = getpath.get_3rd_path("result", "line.png")
    shape_detector_path = getpath.get_3rd_path(
        "models", "shape_predictor_68_face_landmarks.dat"
    )
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_detector_path)
    Cam = camera.Camera(0)
    frame_count = 0
    blink_count = 0
    cam = Cam.open()
    camPara = Cam.para()
    vWidth = 640
    vHeight = 360
    if camPara[1] > camPara[2]:
        rez = camPara[2] / camPara[1]
        if rez == 0.75:
            vWidth = 640
            vHeight = 480
        if camPara[2] > camPara[1]:
            rez = camPara[1] / camPara[2]
            if rez == 0.75:
                vWidth = 480
                vHeight = 640
            else:
                vWidth = 360
                vHeight = 640
    # drawline = draw.Draw()
    while cam.isOpened():
        timeStart = time.time()
        frame_count = frame_count + 1
        flag, video_frame = cam.read()
        if not flag:
            break
        video_frame = cv.resize(video_frame, (vWidth, vHeight), 0, 0, cv.INTER_AREA)
        gray_frame = cv.cvtColor(video_frame, cv.COLOR_BGR2GRAY)
        checks = detector(gray_frame, 0)
        for check in checks:
            # print("-" * 40)
            points = predictor(gray_frame, check)
            np_points = face_utils.shape_to_np(points)
            left_points = np_points[36:42]
            right_points = np_points[42:48]
            left_ear = ear_value(left_points)
            right_ear = ear_value(right_points)
            equal_ear = (left_ear + right_ear) / 2
            # drawline.update(equal_ear, 0.033)
            # if right_ear <= THRESHOLD:
            #     print("Right eye blink!")
            # if left_ear <= THRESHOLD:
            #     print("Left eye blink!")
            if equal_ear <= AVG_THRESHOLD:
                # print("All eyes blink!")
                blink_count = blink_count + 1
            cv.putText(
                video_frame,
                "left_ear: {:.3f}".format(left_ear),
                (10, 30),
                cv.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 0, 0),
                1,
            )
            cv.putText(
                video_frame,
                "right_ear: {:.3f}".format(right_ear),
                (10, 50),
                cv.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 0, 0),
                1,
            )
            cv.putText(
                video_frame,
                "blink_frame: {:d}".format(blink_count),
                (250, 30),
                cv.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 0, 0),
                1,
            )
            cv.putText(
                video_frame,
                "frame_count: {:d}".format(frame_count),
                (250, 50),
                cv.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 0, 0),
                1,
            )
            left_eye_hull = cv.convexHull(left_points)
            right_eye_hull = cv.convexHull(right_points)
            cv.drawContours(video_frame, [left_eye_hull], -1, (0, 255, 0), 1)
            cv.drawContours(video_frame, [right_eye_hull], -1, (0, 255, 0), 1)
        timeEnd = time.time()
        cv.putText(
            video_frame,
            "FPS: {:.1f}".format(1 / (timeEnd - timeStart)),
            (10, 100),
            cv.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 255),
            1,
        )
        cv.imshow("BLINK_CHECK", video_frame)
        if cv.waitKey(1) & 0xFF == ord("q"):
            # drawline.save_pic(pic_path)
            # draw.draw_stop()
            break
    Cam.close()
    cv.destroyAllWindows()


def check_blink_cuda():
    get_model.download_landmarks_model()
    get_model.download_face_model()
    YAWN_THRESHOLD = 0.27
    AVG_THRESHOLD = 0.25
    # pic_path = getpath.get_3rd_path("result", "line.png")
    shape_detector_path = getpath.get_3rd_path(
        "models", "shape_predictor_68_face_landmarks.dat"
    )
    detector = dlib.cnn_face_detection_model_v1("models\\mmod_human_face_detector.dat")
    predictor = dlib.shape_predictor(shape_detector_path)
    Cam = camera.Camera(0)
    frame_count = 0
    blink_count = 0
    cam = Cam.open()
    camPara = Cam.para()
    print(camPara)
    vWidth = 640
    vHeight = 360
    if camPara[1] > camPara[2]:
        rez = camPara[2] / camPara[1]
        if rez == 0.75:
            vWidth = 640
            vHeight = 480
    else:
        rez = camPara[1] / camPara[2]
        if rez == 0.75:
            vWidth = 480
            vHeight = 640
        else:
            vWidth = 360
            vHeight = 640
    # drawline = draw.Draw()
    globalTime = time.time()
    blinkFlag = [0, time.time()]
    tiredFlag = [False, True]
    yawnFlag = [False, False]
    while cam.isOpened():
        if (time.time() - globalTime) >= 3:
            tiredFlag[1] = True
            blink_count = 0
            globalTime = time.time()
        timeStart = time.time()
        frame_count = frame_count + 1
        flag, video_frame = cam.read()
        if not flag:
            break
        video_frame = cv.resize(video_frame, (vWidth, vHeight), 0, 0, cv.INTER_AREA)
        gray_frame = cv.cvtColor(video_frame, cv.COLOR_BGR2GRAY)
        checks = detector(gray_frame, 1)
        # for i, d in enumerate(checks):
        #     print(
        #         "Detection {}: Left: {} Top: {} Right: {} Bottom: {} Confidence: {}".format(
        #             i,
        #             d.rect.left(),
        #             d.rect.top(),
        #             d.rect.right(),
        #             d.rect.bottom(),
        #             d.confidence,
        #         )
        #     )
        rects = dlib.rectangles()
        rects.extend([d.rect for d in checks])
        confidence = []
        for _, d in enumerate(checks):
            confidence.append(d.confidence)
        i = 0
        for check in rects:
            # print("-" * 40)
            points = predictor(gray_frame, check)
            np_points = face_utils.shape_to_np(points)
            left_points = np_points[36:42]
            right_points = np_points[42:48]
            mouth_points = np_points[60:68]
            left_ear = ear_value(left_points)
            right_ear = ear_value(right_points)
            mar = mar_value(mouth_points)
            equal_ear = (left_ear + right_ear) / 2
            # drawline.update(equal_ear, 0.033)
            # if right_ear <= THRESHOLD:
            #     print("Right eye blink!")
            # if left_ear <= THRESHOLD:
            #     print("Left eye blink!")
            if equal_ear <= AVG_THRESHOLD:
                # print("All eyes blink!")
                if blinkFlag[0]:
                    if (time.time() - blinkFlag[1]) > 0.1:
                        blink_count = blink_count + 1
                        blinkFlag[1] = time.time()
                else:
                    blinkFlag[0] = 1
                    blinkFlag[1] = time.time()
            else:
                # blink_count = 0
                blinkFlag[0] = 0
            if (blink_count / (time.time() - globalTime)) >= 2:
                cv.putText(
                    video_frame,
                    "Tired",
                    (check.left(), check.top() - 25),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 0, 255),
                    1,
                )
                tiredFlag[0] = True
            else:
                tiredFlag[0] = False

            if time.time() - globalTime >= 1.5:
                if tiredFlag[0] and tiredFlag[1]:
                    trandata.sockTranData(b'1')
                    tiredFlag[1] = False
                elif not tiredFlag[0] and tiredFlag[1]:
                    trandata.sockTranData(b'0')
                    tiredFlag[1] = False

            if mar >= YAWN_THRESHOLD:
                cv.putText(
                    video_frame,
                    "Yawn",
                    (check.left() + 60, check.top() - 25),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 0, 255),
                    1,
                )
            cv.putText(
                video_frame,
                "left_ear: {:.3f}".format(left_ear),
                (10, 30),
                cv.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 0, 0),
                1,
            )
            cv.putText(
                video_frame,
                "right_ear: {:.3f}".format(right_ear),
                (10, 50),
                cv.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 0, 0),
                1,
            )
            cv.putText(
                video_frame,
                "blink_frame: {:d}".format(blink_count),
                (220, 30),
                cv.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 0, 0),
                1,
            )
            cv.putText(
                video_frame,
                "frame_count: {:d}".format(frame_count),
                (220, 50),
                cv.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 0, 0),
                1,
            )
            cv.putText(
                video_frame,
                "MAR: {:3f}".format(mar),
                (450, 30),
                cv.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 0, 0),
                1,
            )
            left_eye_hull = cv.convexHull(left_points)
            right_eye_hull = cv.convexHull(right_points)
            mouth_hull = cv.convexHull(mouth_points)
            cv.drawContours(video_frame, [left_eye_hull], -1, (0, 255, 0), 1)
            cv.drawContours(video_frame, [right_eye_hull], -1, (0, 255, 0), 1)
            cv.drawContours(video_frame, [mouth_hull], -1, (0, 255, 0), 1)
            cv.rectangle(
                video_frame,
                (check.left(), check.top()),
                (check.right(), check.bottom()),
                (255, 0, 255),
                1,
                1,
                0,
            )
            cv.putText(
                video_frame,
                "Confidence: {:.5f}".format(confidence[i]),
                (check.left(), check.top() - 10),
                cv.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 255),
                1,
            )
            i += 1
        timeEnd = time.time()
        cv.putText(
            video_frame,
            "FPS: {:.1f}".format(1 / (timeEnd - timeStart)),
            (10, 100),
            cv.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 255),
            1,
        )
        cv.imshow("BLINK_CHECK", video_frame)
        if cv.waitKey(1) & 0xFF == ord("q"):
            # drawline.save_pic(pic_path)
            # draw.draw_stop()
            break
    Cam.close()
    cv.destroyAllWindows()


if __name__ == "__main__":
    if dlib.DLIB_USE_CUDA:
        check_blink_cuda()
    else:
        check_blink()
    exit(0)
