import json, logging, random
from http.server import BaseHTTPRequestHandler, HTTPServer
from sqlite3 import paramstyle
from config import Config
from error import StartsWithError
from urllib.parse import urlparse, parse_qs
from http.client import OK, NOT_FOUND, BAD_REQUEST


class HttpStatus:
    ok = OK.real   # 200
    not_found = NOT_FOUND.real  # 404
    bad_request = BAD_REQUEST.real  # 400


class BakaMessages:
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


class Baka(BaseHTTPRequestHandler):
    # global (
    #     path_list,
    #     patht,
    #     to_render,
    #     hi_message,
    #     bye_message,
    #     headers,
    #     params,
    #     req_type
    # )
    default_encoding: str = "utf-8"  # Default encoding Is utf-8 User can be able to Change it

    path_list = []
    patht = []
    to_render = []
    headers = []
    params = []
    req_type = []


    @staticmethod
    def remove_qparam(value_to_split: str, split_by="?", index_to_get=0):
        # item[self.path.split("?")[0]]

        return value_to_split.split(split_by)[index_to_get]

    def send_response_(self, status_code: HttpStatus | int, header=None, end_headers=True,
                       socket_wfile=False, socket_value_to_write=None) -> None:
        """
        Sends Status Code, header, and writes to socket.wfile

        :Args:
        status_code: Should Be a valid HttpStatus Code Takes it as an Integer or HttpStatus Class Variable

        header: Header Should be a Tuple or List, If Header == None Does not Send the Header

        end_header = If it is True Will Automatically call the end_header() method

        socket_wfile: Writes The Given Text To socket.wfile, If it is != None

        socket_value_to_write: If socket_wfile is True and socket_value_to_write is False will Raise An Error
        """

        if status_code:
            self.send_response(status_code)

        if header:
            if type(header) != tuple and type(header) != list:
                raise TypeError("Invalid Type: header Must Be a Tuple or a List")

            if len(header) != 2:
                raise ValueError("Header Must Contain Exactly two Values")

            self.send_header(str(header[0]), str(header[1]))

        if end_headers:
            self.end_headers()

        if socket_wfile:
            # If socket_write_file is True But value is Not Provided We Raise an Error
            if not socket_value_to_write:
                raise ValueError("'socket_value_to_write' Not Provided")

            self.wfile.write(bytes(str(socket_value_to_write), self.default_encoding))


    def do_GET(self):
        req = None
        path_type = None
        value = None

        for item in self.req_type:
            try:
                req = item[self.remove_qparam(self.path)]
                break

            except:
                # logging.log(100 , item[self.path.split("?")[0]])
                # logging.log(100 , item[str if str.startswith(self.path) else None])
                pass

        if req == "GET":
            if self.remove_qparam(self.path) in self.path_list:
                for item in self.patht:
                    try:
                        path_type = item[self.remove_qparam(self.path)]
                        break
                    except:
                        logging.log(100, item[self.remove_qparam(self.path)])
                        # logging.log(100 , item[str if str.startswith(self.path) else None])
                        # pass

                for i in self.to_render:
                    try:
                        value = i[self.remove_qparam(self.path)]
                        break
                    except:
                        pass

                if path_type == "html":
                    self.send_response_(
                        HttpStatus.ok,
                        header=("Content-type", "text/html"),
                        end_headers=False
                    )
                    if Config.CORS_HTML:
                        self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    try:
                        self.wfile.write(bytes(value, self.default_encoding))
                    except:
                        pass

                elif path_type == "special":
                    try:
                        self.send_response_(
                            HttpStatus.ok,
                            header=("Content-type", "text/html"),
                            socket_wfile=True,
                            socket_value_to_write=value
                        )
                    except:
                        pass
                    # self.send_response(200)
                    # # self.send_header
                    # self.end_headers()
                    # try:
                    #     self.wfile.write(bytes(value, self.default_encoding))
                    # except:
                    #     pass

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
                    self.send_response_(
                        HttpStatus.not_found,
                        header=("Content-type", "text/html"),
                        socket_wfile=True,
                        socket_value_to_write="<h1>Error!</h1>",
                    )
                    # self.send_response(400)
                    # self.send_header()
                    # self.end_headers()
                    # self.wfile.write(bytes("<h1>Error!</h1>", self.default_encoding))

                try:
                    query = urlparse(self.path).query
                    query_components = dict(qc.split("=") for qc in query.split("&"))

                    if not query_components:
                        # If query_components is not Empty
                        self.params.clear()
                        self.params.append(query_components)

                except:
                    pass

                else:
                    self.send_response_(
                        HttpStatus.not_found,
                        header=("Content-type", "text/html"),
                        socket_wfile=True,
                        socket_value_to_write="<h1>404 Not found</h1>",
                    )
                    # self.send_response(404)
                    # self.send_header("Content-type", "text/html")
                    # self.end_headers()
                    # self.wfile.write(bytes("<h1>404 Not found</h1>", self.default_encoding))

                    if Config.error_logging:
                        logging.log(40, f"Error path {self.path} not found")
        else:
            self.send_response_(
                HttpStatus.bad_request,
                header=("Content-type", "text/html"),
                socket_wfile=True,
                socket_value_to_write="<h1>Method not allowed</h1>",
            )
            # self.send_response(404)
            # self.send_header("Content-type", "text/html")
            # self.end_headers()
            # self.wfile.write(bytes("<h1>Method not allowed</h1>", self.default_encoding))

            if Config.error_logging:
                logging.log(40, f"Error method not allowed")

    def do_POST(self):
        for item in self.req_type:
            try:
                req = item[self.remove_qparam(self.path)]
                break
            except:
                pass

        if req == "POST":
            # logging.log(100 , dict(self.headers))
            self.headers.append(dict(self.headers))

        else:
            self.send_response_(
                HttpStatus.bad_request,
                header=("Content-type", "text/html"),
                socket_wfile=True,
                socket_value_to_write="<h1>Method not allowed</h1>",
            )
            # self.send_response(404)
            # self.send_header("Content-type", "text/html")
            # self.end_headers()
            # self.wfile.write(bytes("<h1>Method not allowed</h1>", self.default_encoding))

            if Config.error_logging:
                logging.log(40, f"Error method not allowed")

    def get_headers(self):
        return self.headers

    def add_path(self, pathy: str):
        # If path Does not Start with '/' we just add it here, No Need to Raise an Exception
        if not pathy.startswith('/'):
            pathy = f"/{pathy}"

        self.path_list.append(pathy)

    def add_path_type(self, pathy: str, typey: str):
        self.patht.append({pathy: typey})

    def add_render(self, pathy: str, daty: str):
        self.to_render.append({pathy: daty})

    def add_req_type(self, pathy: str, typey: str):
        self.req_type.append({pathy: typey})

    @staticmethod
    def render_template(filename: str, encoding="utf-8") -> str:
        """ renders the Template object

         :Args:
          filepath/filename
          Encoding: Default = utf-8
        """
        try:
            with open(filename, mode="r", encoding=encoding) as file:
                return file.read()

        except FileNotFoundError:
            raise FileNotFoundError("File Does not Exist In The Root Directory, Try Providing A File Path Instead")

    def get_params(self):
        return self.params


def run():
    host_name = Config.host_name
    server_port = Config.port
    web_server = HTTPServer((host_name, server_port), Baka)

    if Config.hi_bye_message:
        print(random.choice(BakaMessages.hi_message))

    print("Server started at http://%s:%s" % (host_name, server_port))

    try:
        web_server.serve_forever()

    except KeyboardInterrupt:
        web_server.server_close()
        if Config.hi_bye_message:
            print(random.choice(BakaMessages.bye_message))

        print("Server stopped.")

