package main

import "C"
import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"net"
	"os"
)

const PRIKEY string = "privateKey.pem"

func decrypt(path string, msg []byte) []byte {
	fp, _ := os.Open(path)
	defer fp.Close()
	fs, _ := fp.Stat()
	buf := make([]byte, fs.Size())
	fp.Read(buf)
	block, _ := pem.Decode(buf)
	pri, _ := x509.ParsePKCS1PrivateKey(block.Bytes)
	decryptMsg, _ := rsa.DecryptPKCS1v15(rand.Reader, pri, msg)
	return decryptMsg
}

//export Server
func Server() {
	if isThere(PRIKEY) {
		s := make([]byte, 256)
		authSocket, err := net.Listen("tcp", ":4321")
		checkError(err)
		defer authSocket.Close()
		authConn, err := authSocket.Accept()
		checkError(err)
		defer authConn.Close()
		fmt.Print("Accept from:", authConn.RemoteAddr())
		_, err = authConn.Read(s)
		checkError(err)
		msg := decrypt(PRIKEY, s)
		fmt.Println(string(msg))
	} else {
		os.Exit(0)
	}
}
