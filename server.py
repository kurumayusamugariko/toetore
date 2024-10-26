import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import uuid

# ゲームルームの管理
rooms = {}

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True  # すべてのオリジンを許可

    def open(self):
        # 空いているルームを探す
        room_id = None
        for rid, clients in rooms.items():
            if len(clients) < 2:
                room_id = rid
                break

        # 空いているルームがない場合、新しいルームを作成
        if room_id is None:
            room_id = len(rooms) + 1
            rooms[room_id] = []

        rooms[room_id].append(self)
        self.room_id = room_id
        self.player_id = f"player{len(rooms[room_id])}"  # プレイヤーIDを "player1" または "player2" に設定
        print(f"WebSocket opened, assigned to room {room_id}, player ID: {self.player_id}")

        # ルームIDとプレイヤーIDをクライアントに送信
        self.write_message(json.dumps({"type": "room_id", "room_id": room_id, "player_id": self.player_id}))

    def on_close(self):
        if hasattr(self, 'room_id') and self in rooms[self.room_id]:
            rooms[self.room_id].remove(self)
            if len(rooms[self.room_id]) == 0:
                del rooms[self.room_id]
        print("WebSocket closed")

    def on_message(self, message):
        print(f"Received message: {message}")
        for client in rooms[self.room_id]:
            if client != self:
                client.write_message(message)
                print(f"Sent message to client in room {self.room_id}: {message}")

def make_app():
    return tornado.web.Application([
        (r"/websocket", WebSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(3001)
    print("Server started on port 3001")
    tornado.ioloop.IOLoop.instance().start()