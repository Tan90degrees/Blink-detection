package myerror

import (
	"fmt"
	"os"
)

func CheckError(err error) {
	if err != nil {
		fmt.Fprintf(os.Stderr, "error: %s", err.Error())
		os.Exit(1)
	}
}

func IsThere(path string) bool {
	_, err := os.Stat(path)
	return err == nil || os.IsExist(err)
}
