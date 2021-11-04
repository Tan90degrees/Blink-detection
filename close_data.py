import eye
import cv2 as cv


def close_data():
    print("准备开始采集闭眼数据，请保持眼睛关闭")
    print("按 s 可以继续采集数据")
    print("按 p 可以暂停采集数据")
    print("按 q 可以结束采集数据")
    flag = 1
    getEye = eye.GetEar("close_data.txt")
    getEye.show_video()
    while 1:
        if flag == 1:
            getEye.ear()
        key = cv.waitKey(1)
        if key & 0xFF == ord("s"):
            print("开始收集数据......")
            flag = 1
        elif key & 0xFF == ord("p"):
            print("已经暂停收集数据")
            print("目前已经保存了", getEye.data_count, "组数据", "按s继续采集，q结束采集")
            flag = 0
        elif key & 0xFF == ord("q"):
            print("quit")
            getEye.input_data.close()
            getEye.cam.release()
            cv.destroyAllWindows()
            print("总共保存了", getEye.data_count, "组数据")
            break
