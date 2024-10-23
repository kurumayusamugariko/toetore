import tornado.ioloop
import tornado.web
import tornado.websocket
import time
import os

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("open success")
        self.timer = tornado.ioloop.PeriodicCallback(self.send_data, 1000)
        self.timer.start()

    def on_close(self):
        self.timer.stop()

    def send_data(self):
        self.write_message('Now is ' + str(time.time()))

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # index.htmlファイルを読み込んで提供
        with open("index.html", "r") as f:
            self.write(f.read())

application = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/websocket', WebSocketHandler),
])

if __name__ == '__main__':
    application.listen(3001)
    tornado.ioloop.IOLoop.instance().start()
