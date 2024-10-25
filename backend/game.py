import pygame
import sys
import asyncio
import websockets
import json

pygame.init()
display = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# プレイヤーの初期設定
player_id = None
room_id = None
players = {}

async def game_loop():
    global player_id, room_id
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

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # マウスクリックでターゲットを追加
                    x, y = event.pos
                    players[player_id] = (x, y)
                    # クリック位置をサーバーに送信
                    await websocket.send(json.dumps({"id": player_id, "x": x, "y": y}))
                    print(f"Sent: {x},{y}")

            keys = pygame.key.get_pressed()
            if player_id in players:
                x, y = players[player_id]
                if keys[pygame.K_LEFT]:
                    x -= 5
                if keys[pygame.K_RIGHT]:
                    x += 5
                if keys[pygame.K_UP]:
                    y -= 5
                if keys[pygame.K_DOWN]:
                    y += 5
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
            display.fill((245, 245, 245))
            for pid, (x, y) in players.items():
                color = (255, 0, 0) if pid != player_id else (0, 128, 255)
                pygame.draw.rect(display, color, pygame.Rect(x - 25, y - 25, 50, 50))

            # ルームIDを画面に表示
            if room_id is not None:
                room_text = font.render(f"Room ID: {room_id}", True, (0, 0, 0))
                display.blit(room_text, (10, 10))

            pygame.display.update()
            clock.tick(60)

# asyncio.run()を使用して非同期関数を実行
asyncio.run(game_loop())