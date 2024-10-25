import tornado.ioloop
import tornado.web
import tornado.websocket

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket connection opened")
        try:
            with open("sample.py", "r", encoding="utf-8") as f:
                file_content = f.read()
                self.write_message(file_content)
        except Exception as e:
            self.write_message(f"Error reading file: {e}")

    def on_close(self):
        print("WebSocket connection closed")

class FaviconHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(204)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")  # index.htmlを表示

application = tornado.web.Application([
    (r"/websocket", WebSocketHandler),
    (r"/favicon.ico", FaviconHandler),
    (r"/", IndexHandler),
])

if __name__ == "__main__":
    application.listen(8888)  # ポート8888でリッスン
    print("Server started at http://localhost:8888")
    tornado.ioloop.IOLoop.instance().start()
