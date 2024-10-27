import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import certifi
from dotenv import load_dotenv

# SSL証明書のパスを確認
print(certifi.where())

# ゲームルームの管理
rooms = {}
countdown_done = False  # カウントダウンの状態を管理

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True  # すべてのオリジンを許可

    def open(self):
        global countdown_done
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

        self.room_id = room_id
        self.player_id = f"player{len(rooms[room_id]) + 1}" 
        print(f"WebSocket opened, assigned to room {room_id}, player ID: {self.player_id}")

        # プレイヤーの初期状態を設定
        player_data = {
            "id": self.player_id,
            "count": 0,
            "position": (640, 360), 
            "flag": True
        }
        
        rooms[room_id].append((self, player_data))  # WebSocketオブジェクトとプレイヤーデータを保存

        # ルームIDとプレイヤーIDをクライアントに送信
        self.write_message(json.dumps({"type": "room_id", "room_id": room_id, "player_id": self.player_id}))

        # プレイヤーが2人揃ったらカウントダウンを開始
        if len(rooms[room_id]) == 2 and not countdown_done:
            for client, _ in rooms[room_id]:
                client.write_message(json.dumps({"type": "start_countdown"}))

    def on_close(self):
        if hasattr(self, 'room_id'):
            # プレイヤーをルームから削除
            rooms[self.room_id] = [(client, data) for client, data in rooms[self.room_id] if client != self]
            if len(rooms[self.room_id]) == 0:
                del rooms[self.room_id]
        print("WebSocket closed")

    def on_message(self, message):
        global countdown_done
        print(f"Received message: {message}")
        # メッセージを解析
        data = json.loads(message)

        # プレイヤーの状態を更新
        if hasattr(self, 'room_id'):
            for i, (client, player_data) in enumerate(rooms[self.room_id]):
                if player_data["id"] == self.player_id:
                    # 状態を更新
                    player_data["count"] = data.get("count", player_data["count"])
                    player_data["position"] = (data.get("x", player_data["position"][0]), data.get("y", player_data["position"][1]))
                    player_data["flag"] = data.get("flag", player_data["flag"])

                    # 他のプレイヤーに状態を送信
                    for other_client, other_data in rooms[self.room_id]:
                        if other_client != self:
                            other_client.write_message(json.dumps({"type": "update", "player_data": player_data}))

                    break

def make_app():
    return tornado.web.Application([
        (r"/websocket", WebSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080, address="0.0.0.0")  # サーバーがポート8080でリッスン
    print("Server started on port 8080")
    tornado.ioloop.IOLoop.instance().start()