from scipy.spatial import distance

def mar_value(eye):
    mar = (distance.euclidean(eye[1], eye[7]) + distance.euclidean(eye[3], eye[5])) / (
        distance.euclidean(eye[0], eye[4]) * 2
    )
    return mar