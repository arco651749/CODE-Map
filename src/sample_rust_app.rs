pub struct WebServer {
    host: String,
    port: u16,
}

impl WebServer {
    pub fn new(host: &str, port: u16) -> Self {
        WebServer {
            host: host.to_string(),
            port,
        }
    }

    pub fn start(&self) {
        println!("啟動 WebServer 於 {}:{}", self.host, self.port);
        self.bind_socket();
        self.listen_connections();
    }

    fn bind_socket(&self) {
        println!("正在綁定 Socket 通訊埠...");
    }

    fn listen_connections(&self) {
        // 尚未實作連線處理，引發危害警告
        todo!("連線處理常式尚未實作");
    }
}

fn main() {
    let server = WebServer::new("127.0.0.1", 8080);
    server.start();
}
