package client

import (
	"fmt"
	"net"
	"src/key"
	"src/myerror"
)

const PUBKEY string = "publicKey.pem"

func Client() {
	var addr string
	var msg string
	fmt.Println("Input server address:")
	fmt.Scanln(&addr)
	fmt.Println("Input message:")
	fmt.Scanln(&msg)
	authSocket, err := net.Dial("tcp", addr)
	myerror.CheckError(err)
	defer authSocket.Close()
	encryptMsg := key.Encrypt(PUBKEY, []byte(msg))
	authSocket.Write(encryptMsg)
}
