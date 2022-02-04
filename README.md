# B-baka!

A simple and lightweight web framework for beginners.

## TODO

- [x] GET
- [x] POST
- [x] PATH
- [x] 404
- [x] CORS
- [x] Json
- [x] HTML
- [x] Get Headers
- [x] Better File System
- [x] Path Params
- [ ] Return Headers
- [ ] Hot reload
- [x] Denying Certain Reqs
- [ ] Database LIB
- [ ] PyPi

## Config

There are 6 config options.

- `hi_bye_message`
- `error_logging`
- `host_name`
- `port`
- `CORS`
- `CORS_HTML`

The first two and the last two are booleans (`bool`) , the third one is a string and the fourth is an integer (`int`).

They can be changed by doing the following:

```py
from baka import Config
Config.hi_bye_message = False
Config.error_logging = False
Config.host_name =  "hostnamehere"
Config.port = "4000"
Config.CORS = True
Config.CORS_HTML = True
```

# Baka

There are only 6 simple functions.

## - `add_path`

### Adds a certain endpoint to the path list

```py
add_path("/")
add_path("/api")
add_path("/home")
add_path("/login")
```
 
## - `add_path_type`

### Add the type of the path

```py
add_path_type("/" , "html")
add_path_type("/api" , "json")
add_path_type("/login" , "html")
```

## - `add_render`

### Used to render things

```py
add_render("/" , render_template("index.html"))
```

```py
add_render("/" , "<h1>Hello!</h1>")
```

```py
a = {
    "hello" : "b",
    "wow" : "dang lol"
    }
add_render("/test" , a)
```

## - `render_template`

### Used to convert HTML to bytes

```py
add_render("/" , render_template("index.html"))
```

## - `run`

### Run the APP

#### Just call it :p

```py
run()
```

## - `get_headers`

### Get headers
#### This makes it a lil complicated but it's fine.

```py
import threading
. . . # normal code here
th = threading.Thread(target=run)
th.daemon = True
th.start()
while True:
    print(Baka.get_params())
```
And similarly for Get Params from URLs

# Types

- `html`
- `json`
- `special`

# Example

```py
from config import Config
from baka import Baka , run
import threading # for getting headers

Config.hi_bye_message = False # disable uwu messages
Config.CORS = True # enable CORS for json

Baka.add_path("/") # add route
Baka.add_path_type("/" , "html") # add type
Baka.add_render("/" , Baka.render_template("index.html")) #render an html file

Baka.add_path("/favicon.ico")
Baka.add_path_type("/favicon.ico", "special")
Baka.add_render("/favicon.ico" , Baka.render_template("fav.html"))

Baka.add_path("/test")
Baka.add_path_type("/test" , "json")

a = {
    "hello" : "b",
    "wow" : "dang lol"
    }
Baka.add_render("/test" , a)

th = threading.Thread(target=run) 
th.daemon = True
th.start() # run server in thread
while True:
    print(Baka.get_headers()) # get headers on POST
```