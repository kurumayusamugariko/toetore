import pygame
from pygame.locals import *
import sys
import random
import json
import asyncio
import websockets
from component import player
from component import target
from component import action
import result

class Main():
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

        uri = "ws://127.0.0.1:3001/websocket"
        async with websockets.connect(uri) as websocket:
            # プレイヤーIDをサーバーから受信
            response = await websocket.recv()
            data = json.loads(response)
            if data["type"] == "room_id":
                room_id = data["room_id"]
                player_id = data["player_id"]
                print(f"Assigned to room ID: {room_id}, player ID: {player_id}")

                # プレイヤーの初期位置を設定
                players[player_id] = (100, 100) if len(players) == 0 else (600, 100)
                await websocket.send(json.dumps({"id": player_id, "x": players[player_id][0], "y": players[player_id][1]}))

            # actionインスタンス化
            target_instance = target.Target()
            player_instance = player.Player()
            game = action.Action(target_instance, player_instance)
            resultScene = result.resultScene(game)

            while True:
                screen.fill((255, 255, 255))

                if player_id in players:
                    x, y = players[player_id]
                    if game.is_playing():
                        game.update()  # 当たり判定を更新
                        game.draw(screen)  # カウントを描画
                    else:
                        resultScene.draw(screen)  # 結果を描画

                    players[player_id] = (x, y)
                    # プレイヤーの位置をサーバーに送信
                    await websocket.send(json.dumps({"id": player_id, "x": x, "y": y}))
                    print(f"Sent: {x},{y}")

                # 他のプレイヤーの位置を受信
                try:
                    response = await websocket.recv()
                    data = json.loads(response)
                    players[data["id"]] = (data["x"], data["y"])
                    print(f"Received: {data}")
                except Exception as e:
                    print(f"Receive error: {e}")

                # 画面の描画
                for pid, (x, y) in players.items():
                    color = (255, 0, 0) if pid != player_id else (0, 128, 255)
                    pygame.draw.rect(screen, color, pygame.Rect(x - 25, y - 25, 50, 50))

                # ルームIDを画面に表示
                if room_id is not None:
                    font = pygame.font.Font(None, 36)  # フォントの設定
                    room_text = font.render(f"Room ID: {room_id}", True, (0, 0, 0))
                    screen.blit(room_text, (10, 10))

                pygame.display.update()
                clock.tick(30)  # 30 FPSに設定

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
