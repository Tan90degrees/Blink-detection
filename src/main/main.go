package main

import (
	"flag"
	"fmt"
	"os"
	"src/client"
	"src/key"
	"src/server"
)

var coma string

func main() {
	strength := flag.Int("key", 2048, "RSA加密强度")
	serverIf := flag.Bool("server", false, "是否开启服务端")
	clientIf := flag.Bool("client", false, "是否开启客户端")
	flag.Parse()
	fmt.Println(*strength)
	key.GenKey(*strength)
	if flag.NArg() != 0 {
		for *serverIf {
			server.Server()
		}
		for *clientIf {
			client.Client()
		}
		os.Exit(0)
	}
	for {
		if flag.NArg() == 0 {
			fmt.Print("Input your option:")
			pline()
			fmt.Scan(&coma)
			switch coma {
			case "server":
				fmt.Println("Auth server started!")
				server.Server()
			case "client":
				fmt.Println("Auth client started!")
				client.Client()
			case "exit":
				os.Exit(0)
			default:
				fmt.Println("Please input server or client.")
			}
		}
	}
}
