package server

import (
	"fmt"
	"net"
	"src/key"
	"src/myerror"
)

const PRIKEY string = "privateKey.pem"

func Server() {
	s := make([]byte, 256)
	authSocket, err := net.Listen("tcp", ":4321")
	myerror.CheckError(err)
	defer authSocket.Close()
	authConn, err := authSocket.Accept()
	myerror.CheckError(err)
	defer authConn.Close()
	fmt.Print("Accept from:", authConn.RemoteAddr())
	_, err = authConn.Read(s)
	myerror.CheckError(err)
	msg := key.Decrypt(PRIKEY, s)
	fmt.Println(string(msg))
}
