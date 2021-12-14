package main

import "C"

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"net"
	"os"
)

const PUBKEY string = "publicKey.pem"

func encrypt(path string, msg []byte) []byte {
	fp, _ := os.Open(path)
	defer fp.Close()
	fs, _ := fp.Stat()
	buf := make([]byte, fs.Size())
	fp.Read(buf)
	block, _ := pem.Decode(buf)
	pub, _ := x509.ParsePKCS1PublicKey(block.Bytes)
	encryptMsg, _ := rsa.EncryptPKCS1v15(rand.Reader, pub, msg)
	return encryptMsg
}

//export Client
func Client(addr string, msg string) {
	if isThere(PUBKEY) {
		authSocket, err := net.Dial("tcp", addr)
		checkError(err)
		defer authSocket.Close()
		encryptMsg := encrypt(PUBKEY, []byte(msg))
		authSocket.Write(encryptMsg)
	} else {
		os.Exit(0)
	}
}
