package main

import (
	"fmt"
	"os"
)

func checkError(err error) {
	if err != nil {
		fmt.Fprintf(os.Stderr, "error: %s", err.Error())
		os.Exit(1)
	}
}

func isThere(path string) bool {
	_, err := os.Stat(path)
	return err == nil || os.IsExist(err)
}
