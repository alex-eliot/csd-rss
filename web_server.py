from http.server import BaseHTTPRequestHandler, HTTPServer
import asyncio
import threading

import bot

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>How'd you get here?</h1></body></html>".encode("utf-8"))

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>How'd you get here?</h1></body></html>".encode("utf-8"))
        
def run(server_class=HTTPServer, handler_class=S, port=443):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def initiate(iter):
    funcs = [bot.start, run]
    loop = asyncio.new_event_loop()
    loop.run_until_complete(funcs[iter]())

if __name__ == "__main__":
    t1 = threading.Thread(target=initiate, args=(0,)) # discord bot
    t2 = threading.Thread(target=initiate, args=(1,)) # dummy web server

    t1.start()
    t2.start()
    t1.join()
    t2.join()