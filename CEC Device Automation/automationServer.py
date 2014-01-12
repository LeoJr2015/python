import os
import tornado.httpserver
import tornado.ioloop

def handle_request(request):
    raw = request.uri
    if "?" in raw:
        if "dev=TV" in raw:
            if "cmd=On" in raw:
                os.system('echo "on 0" | cec-client -d 1 -s')
            elif "cmd=Off" in raw:
                os.system('echo "standby 0" | cec-client -d 1 -s')
        elif "dev=PS3" in raw:
            if "cmd=On" in raw:
                os.system('echo "on 4" | cec-client -d 1 -s')
            elif "cmd=Off" in raw:
                os.sytem('echo "standby 4" | cec-client -d 1 -d')
   
    message = "You requested %s\n" % request.uri
    request.write("HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s" % (
                 len(message), message))
    request.finish()

http_server = tornado.httpserver.HTTPServer(handle_request)
http_server.listen(58080)
tornado.ioloop.IOLoop.instance().start()
