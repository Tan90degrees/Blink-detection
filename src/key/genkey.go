package main

import "C"

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"os"
)

const PRIKEY string = "privateKey.pem"
const PUBKEY string = "publicKey.pem"

//export GenKey
func GenKey(strength int) {
	if isThere(PRIKEY) || isThere(PUBKEY) {
		fmt.Println("There have been keys.")
		return
	}
	// Private key
	priKey, err := rsa.GenerateKey(rand.Reader, strength)
	checkError(err)
	x509priKey := x509.MarshalPKCS1PrivateKey(priKey)
	priFp, err := os.Create(PRIKEY)
	checkError(err)
	defer priFp.Close()
	priPemBlock := pem.Block{
		Type:  "PRIVATE KEY",
		Bytes: x509priKey,
	}
	pem.Encode(priFp, &priPemBlock)

	// Public key
	pubFp, err := os.Create(PUBKEY)
	checkError(err)
	defer pubFp.Close()
	pubKey := priKey.PublicKey
	x509pubKey := x509.MarshalPKCS1PublicKey(&pubKey)
	pubPemBlock := pem.Block{
		Type:  "PUBLIC KEY",
		Bytes: x509pubKey,
	}
	pem.Encode(pubFp, &pubPemBlock)
}
