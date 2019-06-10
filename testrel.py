from http.server import BaseHTTPRequestHandler, HTTPServer
HOST_NAME = 'localhost'
PORT_NUMBER = int(input())
class Server(BaseHTTPRequestHandler):
    status = 'off'
    def generate_data(self):
        CONTENT = f'''status:{self.status}
power:100
current:200'''
        return CONTENT
    def stats(self, on):
        self.status = on
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        print(self.status)
        if self.path == '/on':
            self.stats('on')
            print('status switched to on')
            return 
        if self.path == '/off':
            self.stats('off')
            print('status switched to off')
            return
        self.wfile.write(bytes(self.generate_data(), 'utf8'))


if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()