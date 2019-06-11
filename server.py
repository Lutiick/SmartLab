## -*- coding: utf-8 -*-
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import requests
import time
import urllib.parse
import os
INDEX = open('index.html', 'r').read()

class Default(dict):
    def __missing__(self, key):
        return ''


class Plate:
    def __init__(self, ip, name):
        self.ip = ip
        self.name = name
        self.data = {}

    def reloadData(self):
        try:
            req = requests.get(self.ip).text
            self.data = {x.split(':')[0]:x.split(':')[1] for x in req.split()}
        except:
            print(f'can not reload ({self.name}, {self.ip})')
    
    def getData(self):
        return self.data
    

class Climat(Plate):
    def getType(self):
        return 'climat'


class Relay(Plate):
    def onRelay(self):
        try:
            r = requests.get(self.ip + '/on')
            if r.status_code == 200:
                return True
            else:
                return False
        except:
            return False

    def offRelay(self):
        try:
            r = requests.get(self.ip + '/off')
            if r.status_code == 200:
                return True
            else:
                return False
        except:
            return False
    
    def getType(self):
        return 'relay'


class Requester:
    def __init__(self, plates):
        self.plates = plates
        self.last_time = time.time()
    
    def ask(self):
        for plate in self.plates:
            plate.reloadData()

    def loop(self):
        while True:
            if time.time() - self.last_time > 10:
                self.ask()
            else:
                time.sleep(0.5)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class Server(SimpleHTTPRequestHandler):
    def _main(self):
        relays = []
        climat = []
        for plate in plates:
            data = plate.getData()
            if not data:
                continue
            plate_type = plate.getType()
            if plate_type == 'relay':
                relays.append(f'<li class="relay">Plate - {plate.name}:<button id="{plate.name}" class="switch {data["status"]}">switch</button> Current: {data["current"]}; Power: {data["power"]}</li>')
            elif plate_type == 'climat':
                print(data)
                climat.append(f'<li class="climat">Plate - {plate.name}: hum: {data["humidity"]}; temp: {data["temperature"]}; press: {data["pressure"]}</li>')
        page = INDEX.format_map({'relays': '\n'.join(relays), 'climat': '\n'.join(climat)})
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(page, 'utf8'))

    def _on(self, args):
        if 'name' in args and args['name'] in relayIpByName:
            return relayIpByName[args['name']].onRelay()

    def _off(self, args):
        if 'name' in args and args['name'] in relayIpByName:
            return relayIpByName[args['name']].offRelay()

    def send_file(self):
        path = self.translate_path(self.path)
        f = None
        try:
            f = open(path, 'rb')
            return f
        except OSError:
            return None
        

    def do_GET(self):
        routes = {
            "/" : self._main,
        }
        f = self.send_file()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()
            return
        if self.path in routes:
            routes[self.path]()
    
    def do_POST(self):
        routes = {
            "/on": self._on,
            "/off": self._off
        }
        parsed = urllib.parse.urlsplit(self.path)
        path = parsed.path
        args = dict(urllib.parse.parse_qsl(parsed.query, keep_blank_values=True))
        if path in routes:
            result = routes[path](args)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
        if result:
            self.wfile.write(bytes('successfully', 'utf8'))
        else:
            self.wfile.write(bytes('failed', 'utf8'))


if __name__ == '__main__':
    HOST_NAME = 'localhost'
    PORT_NUMBER = 80
    types = {
        'relay': Relay,
        'climat': Climat
    }
    plates = [st.split(';') for st in open('plates.csv', 'r').read().split('\n')]
    plates = [types[plate[0]](*plate[1:]) for plate in plates]
    relayIpByName = {plate.name: plate for plate in plates if plate.getType() == 'relay'}
    for i in plates:
        i.reloadData()
    httpd = ThreadedHTTPServer((HOST_NAME, PORT_NUMBER), Server)
    try:
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        requester = Requester(plates)
        requester.loop()
    except KeyboardInterrupt:
        pass
    httpd.server_close()