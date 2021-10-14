import requests
import os
import bz2
import getpath


def download_model():
    models = getpath.get_2rd_path('models')
    if os.path.isdir(models):
        pass
    else:
        os.mkdir(models)
    model = getpath.get_3rd_path('models', 'shape_predictor_68_face_landmarks.dat.bz2')
    dat = getpath.get_3rd_path('models', 'shape_predictor_68_face_landmarks.dat')
    if os.path.exists(dat):
        if os.path.isfile(dat):
            return
    if os.path.exists(model):
        if os.path.isfile(model):
            print('model already exists!')
        else:
            print('Downloading model!')
            url = 'http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'
            r = requests.get(url)
            with open(model, 'wb') as f:
                f.write(r.content)
                f.close()
                print('Download successful!')
    else:
        print('Downloading model!')
        url = 'http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'
        r = requests.get(url)
        with open(model, 'wb') as f:
            f.write(r.content)
            f.close()
            print('Download successful!')
    print('Unzipping!')
    with bz2.open(model, 'rb') as r, open(dat, 'wb') as w:
        w.write(r.read())
        r.close()
        w.close()
        print('Unzipped!')
