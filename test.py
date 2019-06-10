from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = 'localhost'
PORT_NUMBER = int(input())
CONTENT = '''temperature:100
humidity:100
pressure:200'''
class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        status = 200
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        print(self.path)
        self.wfile.write(bytes(CONTENT, 'utf8'))


if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()