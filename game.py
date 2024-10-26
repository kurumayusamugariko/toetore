import pygame
import asyncio
import websockets
import json
import traceback

pygame.init()
display = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# プレイヤーの初期設定
player_id = None
room_id = None
players = {}

async def main():
    uri = 'ws://44.201.122.14/websocket'  # サーバーのパブリックIPアドレスとポートを使用
    print(uri)
    try:
        await asyncio.gather(
            handle_websocket(uri),
            game_loop()
        )
    except Exception as e:
        print(f"Error in main: {e}")
        traceback.print_exc()

async def handle_websocket(uri):
    print("uri", uri)
    global player_id, room_id
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket")
            # プレイヤーIDをサーバーから受信
            response = await websocket.recv()
            print("1")
            data = json.loads(response)
            print("2")
            if data["type"] == "room_id":
                print("3")
                room_id = data["room_id"]
                player_id = data["player_id"]
                print(f"Assigned to room ID: {room_id}, player ID: {player_id}")

                # プレイヤーの初期位置を設定
                players[player_id] = {"x": 100, "y": 100}

            while True:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=0.1)
                    data = json.loads(message)
                    if data["type"] == "update":
                        players[data["player_id"]] = data["position"]
                except asyncio.TimeoutError:
                    pass
    except Exception as e:
        print(f"WebSocket error: {e}")
        traceback.print_exc()

async def game_loop():
    print("Starting game loop")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # 画面をクリア
        display.fill((0, 0, 0))

        # プレイヤーを描画
        print("players", players)
        for player in players.values():
            pygame.draw.rect(display, (255, 0, 0), (player["x"], player["y"], 100, 50))

        pygame.display.flip()
        clock.tick(60)

        await asyncio.sleep(0)  # イベントループを他のタスクに譲る

# メインループ
asyncio.run(main())