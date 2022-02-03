# B-baka

A simple and lightweight web framework for beginners.

## Config

There are 4 config options.

- `hidebymessage`
- `errorlogging`
- `hostname`
- `port`

The first two are `bool`'s, the third one is a string and the fourth is an integer.

They can be changed by doing the following

```py
from baka import Config
Config.hidebymessage = False
Config.errorlogging = False
Config.hostname =  "hostnamehere"
Config.port = "4000"
```

# Baka

There are only 5 simple functions.

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

# Types

- `html`
- `json`
- `special`

# Example

```py
from baka import run , add_path , add_path_type , add_render , render_template
from baka import Config

Config.hibyemessage = False

add_path("/")
add_path_type("/" , "html")
add_render("/" , render_template("index.html"))

add_path("/favicon.ico")
add_path_type("/favicon.ico", "special")
add_render("/favicon.ico" , render_template("fav.html"))

add_path("/test")
add_path_type("/test" , "json")
a = {
    "hello" : "b",
    "wow" : "dang lol"
    }
add_render("/test" , a)
run()
```
