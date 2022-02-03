import json
import logging
import random
from http.server import BaseHTTPRequestHandler, HTTPServer


class StartsWithError(Exception):
    pass

class Config:
    hibyemessage = True
    errorlogging = True
    hostname = "localhost"
    port = 8080

class Baka(BaseHTTPRequestHandler):
    global pathlist
    global patht
    global torender
    global himessage
    global byemessage

    byemessage = ["why awe you weaving *looks at you* me :( bye bye" , "pwease dont go" , "bye f-f-fwen" , "dont go wuv"]
    himessage = ["hi sewvews wunnying nyow *whispers to self* :p *runs away*" , "omg hi how awe y-you!!11" , "whats up f-f-fwen"]

    pathlist = []
    patht = []
    foo = []
    torender = []

    def do_GET(self):
        pathtype = None
        if self.path in pathlist:

            for item in patht:
                try:
                    pathtype = item[self.path]
                    break;
                except:
                    pass
            for i in torender:
                try:
                    value = i[self.path]
                    break;
                except:
                    pass

            if pathtype == "html":
                self.send_response(200)
                self.send_header("Content-type" , "text/html")
                self.end_headers()
                try:
                    self.wfile.write(bytes(value , "utf-8"))
                except:
                    pass
            elif pathtype == "special":
                self.send_response(200)
                self.send_header("Content-type" , "text/html")
                self.end_headers()
                try:
                    self.wfile.write(bytes(value , "utf-8"))
                except:
                    pass
            elif pathtype == "json":
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(str(value).encode(encoding='utf_8'))
            else:
                if Config.errorlogging:
                    logging.log(40 , f" Error '{self.path}', can't find path type '{pathtype}'")
                self.send_response(400)
                self.send_header("Content-type" , "text/html")
                self.end_headers()
                self.wfile.write(bytes("<h1>Error!</h1>" , "utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type" , "text/html")
            self.end_headers()
            self.wfile.write(bytes("<h1>404 Not found</h1>" , "utf-8"))
            if Config.errorlogging:
                logging.log(40 , f"Error path {self.path} not found")

def add_path(pathy : str):
    if pathy.startswith("/"):
        pathlist.append(pathy)
    else:
        raise StartsWithError("Path must start with '/' ")

def add_path_type(pathy : str , typey : str):
    patht.append({pathy : typey})

def add_render(pathy : str , daty : str):
    torender.append({pathy : daty})

def render_template(filename : str):
    with open(filename , "r") as file:
        return file.read()

def run():
    hostName = Config.hostname
    serverPort = Config.port
    webServer = HTTPServer((hostName, serverPort), Baka)
    if Config.hibyemessage: print(random.choice(himessage))
    print("Server started at http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    if Config.hibyemessage: print(random.choice(byemessage))
    print("Server stopped.")

