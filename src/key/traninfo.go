package key

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"os"
)

func Encrypt(path string, msg []byte) []byte {
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

func Decrypt(path string, msg []byte) []byte {
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
