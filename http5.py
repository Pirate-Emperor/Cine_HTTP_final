import pandas as pd
from simple_http_server import route, server
import urllib

@route("/")
def index():
    return {"hello": "world"}   



import os
from simple_http_server import request_map
from simple_http_server import Response
from simple_http_server import MultipartFile
from simple_http_server import Parameter
from simple_http_server import Parameters
from simple_http_server import Header
from simple_http_server import JSONBody
from simple_http_server import HttpError
from simple_http_server import StaticFile
from simple_http_server import Headers
from simple_http_server import Cookies
from simple_http_server import Cookie
from simple_http_server import Redirect
from simple_http_server import ModelDict
from simple_http_server import Session, PathValue, _logger
from simple_http_server import Request, RequestBodyReader
# request_map has an alias name `route`, you can select the one you familiar with.
port=9998
@request_map("/index")
def my_ctrl():
    return Response(status_code=100,body={'code': 100,'message': "Success"}) # You can return a dictionary, a string or a `simple_http_server.simple_http_server.Response` object.

#_logger.setLevel("INFO")
"""@route("/say_hello", method=["GET", "POST"])
def my_ctrl2(name, name2=Parameter("name", default="KEIJACK"), model=ModelDict()):

    name == name2 # True
    name == model["name"] # True
    return "<!DOCTYPE html><html><body>hello, %s, %s, %s</body></html>" % (name, name2, model["name"])"""
@route("/add", method=["POST"])
def my_ctrl21(userId, name, city, locations):
    data = pd.read_csv('users.csv')  
    if len(data[data.userId==userId]): return Response(status_code=226,body={'code': 226,'message': data})
    new = [userId, name, city, locations] 
    data.loc[len(data.index)] = new
    #data = data.append(pd.Series(new, index=data.columns[:len(new)]), ignore_index=True)
    data.to_csv('users.csv',index=False)
    data = data.to_dict()
    return Response(status_code=201,body={'code': 201,'message': data})

@route("/update", method=["PUT"])
def my_ctrl22(userId, name, city, locations):
    data = pd.read_csv('users.csv')  
    if not len(data[data.userId==userId]): return Response(status_code=204,body={'code': 204,'message': "userId not found"})
    data[data.userId==userId] = [userId, name, city, locations] 
    data.to_csv('users.csv',index=False)
    data = data.to_dict()
    return Response(status_code=202,body={'code': 202,'message': data})
@route("/users", method=["GET"])
def my_ctrl23():
    data = pd.read_csv('users.csv')  
    data = data.to_dict()
    return Response(status_code=200,body={'code': 200,'message': data})

@route("/users", method="HEAD")
def my_ctrl24(header=Headers()):
    print(header)
    return Response(status_code=200,body={'code': 200,'message': header})
@route("/users", method=["POST","PUT","DELETE"])
def my_ctrl24():
    return Response(status_code=501,body={'code': 501,'message': "POST, PUT, DELETE methods haven't been implemented for /users"})

@route("/users/", method="GET")
def my_ctrl31(id=Parameter("id")):
    data = pd.read_csv('users.csv')  
    data = data[data.userId==id]
    data = data.to_dict()
    return Response(status_code=200,body={'code': 200,'message': data})

@route("/users/", method="POST")
def my_ctrl32(request=Request(),head=Headers()):
    json=request.json
    new =[i for i in json.values()]
    data = pd.read_csv('users.csv')  
    if len(data[data.userId==new[0]]): return Response(status_code=226,body={'code': 226,'message': "Duplicate Entries are not allowed"})
    #new = [userId, name, city, locations] 
    data.loc[len(data.index)] = new
    #data = data.append(pd.Series(new, index=data.columns[:len(new)]), ignore_index=True)
    data.to_csv('users.csv',index=False)
    data = data.to_dict()
    return Response(status_code=201,body={'code': 201,'message': data})

@route("/users/", method="PUT")
def my_ctrl33(id=Parameter("id"), request=Request()):
    json=request.json
    new =[id]
    new.extend([i for i in json.values()])
    data = pd.read_csv('users.csv')  
    if not len(data[data.userId==new[0]]): return Response(status_code=204,body={'code': 204,'message': "userId not found"})
    data[data.userId==new[0]] = new 
    data.to_csv('users.csv',index=False)
    data = data.to_dict()
    return Response(status_code=202,body={'code': 202,'message': data})

@route("/users/", method="HEAD")
def my_ctrl34(header=Headers()):
    print(header)
    return Response(status_code=200,body={'code': 200,'message': header})

@route("/users/", method=["DELETE"])
def my_ctrl35(id=Parameter("id")):
    data = pd.read_csv('users.csv')  
    data = data[data.userId!=id]
    data.to_csv('users.csv',index=False)
    data = data.to_dict()
    return Response(status_code=200,body={'code': 200,'message': data})

@request_map("/error")
def my_ctrl3():
    return Response(status_code=500,body={'code': 500,'message': "Error in Implementation"})
@request_map("/error404")
def my_ctrl3():
    return Response(status_code=404,body={'code': 404,'message': "Resource Not Found"})
@request_map("/error405")
def my_ctrl3():
    return Response(status_code=405,body={'code': 405,'message': "Method Not Allowed"})

@request_map("/exception")
def exception_ctrl():
    raise HttpError(400, "Exception")

@request_map("/upload", method="GET")
def show_upload():
    root = os.path.dirname(os.path.abspath(__file__))
    print(root)
    return StaticFile("%s/my_dev/my_test_index.html" % root, "text/html; charset=utf-8")


@request_map("/upload", method="POST")
def my_upload(img=MultipartFile("img")):
    root = os.path.dirname(os.path.abspath(__file__))
    print(root)
    img.save_to_file(root + "/my_dev/imgs/" + img.filename)
    return "<!DOCTYPE html><html><body>upload ok!</body></html>"


@request_map("/post_txt", method="POST")
def normal_form_post(txt):
    return "<!DOCTYPE html><html><body>hi, %s</body></html>" % txt

@request_map("/tuple")
def tuple_results():
    # The order here is not important, we consider the first `int` value as status code,
    # All `Headers` object will be sent to the response
    # And the first valid object whose type in (str, unicode, dict, StaticFile, bytes) will
    # be considered as the body
    return 200, Headers({"my-header": "headers"}), {"success": True}

"""
" Cookie_sc will not be written to response. It's just some kind of default
" value
"""
@request_map("cookie")
def tuple_with_cookies(headers=Headers(),request=Request(),all_cookies=Cookies(), cookie_sc=Cookie("sc")):
    print("=====>headers")
    print(headers)
    print("=====>request")
    print(request.json)
    print("=====> cookies ")
    print(all_cookies)
    print("=====> cookie ")
    print(cookie_sc)
    print("======<")
    import datetime
    expires = datetime.datetime(2018, 12, 31)

    cks = Cookies()
    # cks = cookies.SimpleCookie() # you could also use the build-in cookie objects
    cks["ck1"] ="Rahul"
    cks["ck1"]["Path"] = "/"
    cks["ck1"]["Expires"] = expires.strftime(Cookies.EXPIRE_DATE_FORMAT)
    # You can ignore status code, headers, cookies even body in this tuple.
    return Header({"xx": "yyy"}), cks, "<html><body>OK</body></html>"

"""
" If you visit /a/b/xyz/x，this controller function will be called, and `path_val` will be `xyz`
"""
@request_map("/a/b/{path_val}/x")
def my_path_val_ctr(path_val=PathValue()):
    return f"<html><body>{path_val}</body></html>"

@request_map("/star/*") # /star/c will find this controller, but /star/c/d not.
@request_map("*/star") # /c/star will find this controller, but /c/d/star not.
def star_path(path_val=PathValue()):
    return f"<html><body>{path_val}</body></html>"

@request_map("/star/**") # Both /star/c and /star/c/d will find this controller.
@request_map("**/star") # Both /c/star and /c/d/stars will find this controller.
def star_path(path_val=PathValue()):
    return f"<html><body>{path_val}</body></html>"

@request_map("/redirect")
def redirect():
    return Redirect("/index")

@request_map("session")
def test_session(session=Session(), invalid=False):
    ins = session.get_attribute("in-session")
    if not ins:
        session.set_attribute("in-session", "Hello, Session!")

    _logger.info("session id: %s" % session.id)
    if invalid:
        _logger.info("session[%s] is being invalidated. " % session.id)
        session.invalidate()
    return "<!DOCTYPE html><html><body>%s</body></html>" % str(ins)

# use coroutine, these controller functions will work both in a coroutine mode or threading mode.

async def say(sth: str = ""):
    _logger.info(f"Say: {sth}")
    return f"Success! {sth}"

@request_map("/ad/coroutine")
async def coroutine_ctrl(hey: str = "Hey!"):
    return await say(hey)

@route("/res/write/bytes")
def res_writer(response: Response):
    response.status_code = 200
    response.add_header("Content-Type", "application/octet-stream")
    response.write_bytes(b'abcd')
    response.write_bytes(bytearray(b'efg'))
    response.close()


import simple_http_server.server as server
#import my_test_ctrl


"""def main(*args):
    # The following method can import several controller files once.
    server.scan("my_ctr_pkg", r".*controller.*")"""
server.start(port=port)

"""if __name__ == "__main__":
    main()"""