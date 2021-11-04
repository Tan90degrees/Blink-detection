import pymysql
import socket


def trnsData(avrg, host, user, password, database):
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


def httpTranData(avrg):
    data = "HTTP/1.1 200 OK\r\ncontent-type: text/html\r\n\r\n%s" % avrg
    edata = data.encode("utf-8")
    servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servSocket.bind(("0.0.0.0", 10086))
    servSocket.listen()
    while True:
        conn, addr = servSocket.accept()
        # req = conn.recv(1024)
        conn.send(bytes(edata))
        print("Request from:", addr)
        conn.close()


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

