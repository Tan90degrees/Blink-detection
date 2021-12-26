import pymysql
import socket
import threading


def trnsDatas(avrg, host, user, password, database):
    db = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id FROM id2table WHERE idid = '1';")
        db.commit()
    except:
        db.rollback()
    pt = cursor.fetchone()
    try:
        cursor.execute(
            ("UPDATE blinktable SET blink = '%d' WHERE blinkid = '%d';" % (avrg, pt[0]))
        )
        db.commit()
    except:
        db.rollback()
    db.close()

def trnsData(avrg, host, user, password, database):
    db = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = db.cursor()
    try:
        cursor.execute(
            ("UPDATE tired SET istired = '%d' WHERE id = '1';" % (avrg))
        )
        db.commit()
    except:
        print("Dassdasdsd")
        db.rollback()
    db.close()

class httpTranData(threading.Thread):
    def __init__(self, threadID, avrg, servSocket, threadlock) -> None:
        threading.Thread.__init__(self)
        self.threadID = threadID
        data = "HTTP/1.1 200 OK\r\ncontent-type: text/html\r\n\r\n%s" % avrg
        self.edata = data.encode("utf-8")
        self.servSocket = servSocket
        self.threadlock = threadlock

    def run(self) -> None:
        print("线程", self.threadID, "开始")
        self.threadlock.acquire()
        # try:
        #     self.servSocket.bind(("0.0.0.0", 10086))
        # except OSError:
        #     # self.servSocket.shutdown(socket.SHUT_RDWR)
        #     self.servSocket.close()
        #     print("222")
        #     self.servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     self.servSocket.bind(("0.0.0.0", 10086))
        try:
            self.servSocket.listen()
        except OSError:
            print("线程", self.threadID, "结束")
            return
        try:
            conn, addr = self.servSocket.accept()
        except OSError:
            print("线程", self.threadID, "结束")
            return
        # self.servSocket.close()
        # req = conn.recv(1024)
        try:
            conn.send(bytes(self.edata))
        except ConnectionResetError:
            conn.close()
            print("线程", self.threadID, "结束")
            return
        print("Request from:", addr)
        conn.close()
        if self.threadlock.locked():
            self.threadlock.release()
        print("线程", self.threadID, "结束")
        return


def httpTranImg(imgPath):
    imgP = open(imgPath, "rb")
    img = imgP.read(16696)
    data = (
        "HTTP/1.1 200 OK\r\ncontent-type: image/png\r\nContent-Length: 16696\r\n\r\n%s"
        % img
    )
    edata = data.encode("utf-8")
    servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servSocket.bind(("0.0.0.0", 10086))
    servSocket.listen()
    while True:
        conn, addr = servSocket.accept()
        req = conn.recv(1024)
        conn.send(edata)
        print(edata)
        conn.close()

def sockTranData(data):
    servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        servSocket.connect(("127.0.0.1", 4321))
    except:
        return
    servSocket.sendall(data)
    servSocket.close()