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
        players = {player_id: {"count": 0}}

        # インスタンス化
        target_instance = target.Target()
        player_instance = player.Player()
        game = action.Action(target_instance, player_instance)
        resultScene = result.resultScene(game)

        uri = "ws://127.0.0.1:3001/websocket"
        async with websockets.connect(uri) as websocket:
            response = await websocket.recv()
            data = json.loads(response)
            print(data)
            if data["type"] == "room_id":
                room_id = data["room_id"]
                player_id = data["player_id"]
                players[player_id] = {"count": 0} 

            while True:
                screen.fill((255, 255, 255))

                if player_id in players:
                    game._count = players[player_id]["count"]

                    if game.is_playing():
                        game.update()
                        game.draw(screen)

                        # 現在の位置を取得
                        x = player_instance._rect.x
                        y = player_instance._rect.y
                        # print(data)
                    else:
                        resultScene.draw(screen)

                    players[player_id]["count"] = game._count

                    # 位置とカウントを送信
                    await websocket.send(json.dumps({
                        "id": player_id,
                        "count": players[player_id]["count"],
                        "x": x,
                        "y": y,
                        "flag": game._is_playing
                    }))

                # 他のプレイヤーの位置を受信
                try:
                    response = await websocket.recv()
                    data = json.loads(response)
                    
                    print("Received data:", data)  # 受信したデータを表示
                    
                    if data["id"] in players:
                        players[data["id"]]["count"] = data["count"]
                        players[data["id"]]["position"] = (data["x"], data["y"])
                        players[data["id"]]["flag"] = data["flag"]
                    else:
                        players[data["id"]] = {
                            "count": data["count"],
                            "position": (data["x"], data["y"]),
                            "flag": data["flag"]
                        }

                    print("結果")
                    print(players)
                    for player_id, player_data in players.items():
                        print(f"id: {player_id}")
                        print(f"data: {player_data}")

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
