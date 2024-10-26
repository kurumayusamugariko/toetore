import pygame
from pygame.locals import *
import sys
import json
import asyncio
import websockets
from component import player
from component import target
from component import action
import result

class Main:
    async def main(self):
        pygame.init()

        # 画面設定
        screen = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()  # Clockを初期化

        # プレイヤーの初期設定
        global player_id, room_id
        player_id = None
        room_id = None
        players = {}

        # インスタンス化
        target_instance = target.Target()
        player_instance = player.Player()
        game = action.Action(target_instance, player_instance)
        resultScene = result.resultScene(game)

        uri = "ws://127.0.0.1:3001/websocket"
        async with websockets.connect(uri) as websocket:
            # サーバーからの初期メッセージを受信
            response = await websocket.recv()
            data = json.loads(response)
            print(data)

            if data["type"] == "room_id":
                room_id = data["room_id"]
                player_id = data["player_id"]
                players[player_id] = {"count": 0, "position": (640, 360), "flag": True}

                print(f"My player ID: {player_id}")

            while True:
                screen.fill((255, 255, 255))

                if player_id in players:
                    if game.is_playing():
                        game.update()
                        game.draw(screen)

                        x = player_instance._rect.x
                        y = player_instance._rect.y
                    else:
                        resultScene.draw(screen)

                    count = game._count

                    await websocket.send(json.dumps({
                        "id": player_id,
                        "count": count,
                        "x": x,
                        "y": y,
                        "flag": game._is_playing
                    }))

                # 他のプレイヤーの位置を受信
                try:
                    response = await websocket.recv()
                    data2 = json.loads(response)
                    print("Received data:", data2)

                    if data2["type"] == "update":
                        player_data = data2["player_data"]
                        players[player_data["id"]] = {
                            "count": player_data["count"],
                            "position": tuple(player_data["position"]),
                            "flag": player_data["flag"]
                        }

                        print("結果")
                        print(players)

                        # 自分のプレイヤーIDを取得
                        my_player_id = player_id

                        # 相手のプレイヤーIDを取得（自分以外のプレイヤーを選択）
                        for pid in players:
                            if pid != my_player_id:
                                target_player_id = pid  # 相手のプレイヤーID
                                break  # 最初の相手を選択

                        # 相手のflagを取り出す
                        try:
                            flag_value = players[target_player_id]['flag']
                            print(f"Flag for {target_player_id}: {flag_value}")
                        except KeyError:
                            print(f"Player {target_player_id} not found or does not have a flag.")

                except Exception as e:
                    print(f"Receive error: {e}")

                # ルームID表示
                if room_id is not None:
                    font = pygame.font.Font(None, 36)
                    room_text = font.render(f"Room ID: {room_id}", True, (0, 0, 0))
                    screen.blit(room_text, (10, 10))

                pygame.display.update()
                clock.tick(30)

                # イベント処理
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            sys.exit()

# asyncio.run()を使用して非同期関数を実行
if __name__ == "__main__":
    main_instance = Main()
    asyncio.run(main_instance.main())
