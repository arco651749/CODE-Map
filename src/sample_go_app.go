package main

import (
	"fmt"
	"time"
)

type APIGateway struct {
	host string
	port int
}

func (gw *APIGateway) Start() {
	fmt.Printf("啟動 APIGateway 於 %s:%d\n", gw.host, gw.port)
	gw.registerRoutes()
	gw.listen()
}

func (gw *APIGateway) registerRoutes() {
	fmt.Println("註冊微服務路由表...")
}

func (gw *APIGateway) listen() {
	// 尚未完成網路輪詢實作，觸發執行期恐慌中斷
	time.Sleep(100 * time.Millisecond)
	panic("網路監聽常式尚未實作，引發致命恐慌")
}

func main() {
	gateway := &APIGateway{host: "0.0.0.0", port: 9000}
	gateway.Start()
}
