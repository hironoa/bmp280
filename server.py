# coding:utf-8
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import time
import os
from bme280 import readData
 
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("WebSocket Opened")
        self.temps = []
 
    def on_message(self, message):
        print("Message Received")
        while True:
            pres, temp, hum= readData()
            self.temps.append(temp)
            n_temp = len(self.temps)
            if n_temp > 12:
                self.temps = self.temps[1:]
            payload = {"temp":self.temps}
            message = json.dumps(payload)
            self.write_message(message)
            print(temp)
            print(pres)
            print(hum)
            time.sleep(5) #何秒に一回データを取るか
            
    def on_close(self):
        print("WebSocket Closed")
        return 0

class MainHandler(tornado.web.RequestHandler):
    def get(self):  
        self.render('index.html')
 
application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", WebSocketHandler),
    ],
    template_path=os.path.join(os.getcwd(), "templates"),
    static_path=os.path.join(os.getcwd(), "static")
)
 
if __name__ == "__main__":
    application.listen(9999)
    tornado.ioloop.IOLoop.current().start()