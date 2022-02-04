import json
import logging
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from sqlite3 import paramstyle
from config import Config
from error import StartsWithError
from urllib.parse import urlparse , parse_qs

class Baka(BaseHTTPRequestHandler):
    global path_list
    global patht
    global to_render
    global hi_message
    global bye_message
    global headers
    global params
    global req_type
    

    bye_message = [
        "why awe you weaving *looks at you* me :( bye bye",
        "pwease dont go",
        "bye f-f-fwen",
        "dont go wuv",
    ]
    hi_message = [
        "hi sewvews wunnying nyow *whispers to self* :p *runs away*",
        "omg hi how awe y-you!!11",
        "whats up f-f-fwen",
    ]

    path_list = []
    patht = []
    to_render = []
    headers = []
    params = []
    req_type = []

    def do_GET(self):
        req = None
        path_type = None
        value = None

        for item in req_type:
            try:
                req = item[self.path.split("?")[0]]

                break
            except:
                #logging.log(100 , item[self.path.split("?")[0]])
                #logging.log(100 , item[str if str.startswith(self.path) else None])
                pass

        if req == "GET":
            if self.path.split("?")[0] in path_list:

                for item in patht:
                    try:
                        path_type = item[self.path.split("?")[0]]
                        break
                    except:
                        logging.log(100 , item[self.path.split("?")[0]])
                        #logging.log(100 , item[str if str.startswith(self.path) else None])
                        pass
                

                for i in to_render:
                    try:
                        value = i[self.path.split("?")[0]]
                        break
                    except:
                        pass

                if path_type == "html":
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    if Config.CORS_HTML:
                        self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    try:
                        self.wfile.write(bytes(value, "utf-8"))
                    except:
                        pass
                elif path_type == "special":
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    try:
                        self.wfile.write(bytes(value, "utf-8"))
                    except:
                        pass
                elif path_type == "json":
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    if Config.CORS:
                        self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(str(value).encode(encoding="utf_8"))
                else:
                    if Config.error_logging:
                        logging.log(
                            40, f" Error '{self.path}', can't find path type '{path_type}'"
                        )
                    self.send_response(400)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes("<h1>Error!</h1>", "utf-8"))
                            
                try:
                    query = urlparse(self.path).query
                    query_components = dict(qc.split("=") for qc in query.split("&"))
                    if query_components == []:
                        pass
                    else:
                        params.clear()
                        params.append(query_components)
                except:
                    pass
                else:
                    self.send_response(404)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes("<h1>404 Not found</h1>", "utf-8"))
                    if Config.error_logging:
                        logging.log(40, f"Error path {self.path} not found")
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<h1>Method not allowed</h1>", "utf-8"))
            if Config.error_logging:
                logging.log(40, f"Error method not allowed")           


    def do_POST(self):
        for item in req_type:
            try:
                req = item[self.path.split("?")[0]]
                break
            except:
                pass
        if req == "POST":
            #logging.log(100 , dict(self.headers))
            headers.append(dict(self.headers))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<h1>Method not allowed</h1>", "utf-8"))
            if Config.error_logging:
                logging.log(40, f"Error method not allowed")   

        

    def get_headers():
        return headers


    def add_path(pathy: str):
        if pathy.startswith("/"):
            path_list.append(pathy)
        else:
            raise StartsWithError("Path must start with '/' ")


    def add_path_type(pathy: str, typey: str):
        patht.append({pathy: typey})


    def add_render(pathy: str, daty: str):
        to_render.append({pathy: daty})

    def add_req_type(pathy : str , typey : str):
        req_type.append({pathy : typey})

    def render_template(filename: str):
        with open(filename, "r") as file:
            return file.read()


    def get_params():
        return params

def run():
    host_name = Config.host_name
    server_port = Config.port
    web_server = HTTPServer((host_name, server_port), Baka)
    if Config.hi_bye_message:
        print(random.choice(hi_message))
    print("Server started at http://%s:%s" % (host_name, server_port))
    
    
    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    if Config.hi_bye_message:
        print(random.choice(bye_message))
    print("Server stopped.")
