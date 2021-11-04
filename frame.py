import socket

import cv2 as cv

import numpy as np

import struct

import pickle

from getpath import get_3rd_path

UNIX_SOCK_PATH = get_3rd_path("tmp", "conn.sock")
SERV_IP = "127.0.0.1"
PORT = 1234
WIDTH = 1920
HEIGHT = 1080
FPS = 30


class server:
    def __init__(self, fps, quality):
        self.encode_param = [int(cv.IMWRITE_JPEG_QUALITY), quality]  # quality 1~100
        self.servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servSocket.bind((SERV_IP, PORT))
        # self.servSocket.connect((SERV_IP, PORT))
        # self.servSocket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # self.servSocket.connect(UNIX_SOCK_PATH)

    def frameToSend(self, videoFrame):
        ret, imgEncoded = cv.imencode(".jpg", videoFrame, self.encode_param)
        print("ret1:", ret)
        data = np.array(imgEncoded)
        dataToSend = data.tobytes()
        return dataToSend

    def sendFrame(self, dataToSend):
        self.servSocket.listen(5)
        print("LISTENING AT:", (SERV_IP, PORT))
        clientSocket, caddr = self.servSocket.accept()
        print("GOT CONNECTION FROM:", caddr)
        clientSocket.send(str.encode(str(len(dataToSend)).ljust(16)))
        clientSocket.send(dataToSend)
        # ret = self.servSocket.recv(1024)
        # print('ret2', ret)


class client:
    def __init__(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.clientSocket.bind((SERV_IP, PORT))
        self.clientSocket.connect((SERV_IP, PORT))
        # self.clientSocket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # self.clientSocket.connect(UNIX_SOCK_PATH)

    def recvFrame(self):
        data = b""
        payloadSize = struct.calcsize("Q")
        while len(data) < payloadSize:
            packet = self.clientSocket.recv(4 * 1024)
            if not packet:
                break
            data += packet
        packedMsgSize = data[:payloadSize]
        data = data[payloadSize:]
        msgSize = struct.unpack("Q", packedMsgSize)[0]
        while len(data) < msgSize:
            data += self.clientSocket.recv(4 * 1024)
        frameData = data[:msgSize]
        data = data[msgSize:]
        frame = pickle.loads(frameData)
        return frame

