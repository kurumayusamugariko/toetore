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
import start  # start.pyからインポート

class Main:
    async def main(self):
        pygame.init()

        # 画面設定
        screen = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()  # Clockを初期化
        font = pygame.font.Font('./HGRGY.TTC', 50)
        text = font.render('日本語', True, (0, 0, 0))

        # プレイヤーの初期設定
        global player_id, room_id
        player_id = None
        room_id = None
        players = {}
        target_player_id = None  # 初期化

        # インスタンス化
        target_instance = target.Target()
        player_instance = player.Player()
        game = action.Action(target_instance, player_instance)
        resultScene = result.resultScene(game)

        uri = "ws://44.201.122.14/websocket"
        async with websockets.connect(uri) as websocket:
            # サーバーからの初期メッセージを受信
            response = await websocket.recv()
            data = json.loads(response)
            print(data)

            if data["type"] == "room_id":
                room_id = data["room_id"]
                player_id = data["player_id"]
                players[player_id] = {"score": 0, "position": (640, 360), "flag": True}

                print(f"My player ID: {player_id}")

                countdown_done = data.get("countdown_done", False)  # サーバーからカウントダウンの状態を受信

            while True:
                if not countdown_done:
                    # サーバーからカウントダウンの開始通知を受信
                    response = await websocket.recv()
                    data = json.loads(response)
                    if data["type"] == "start_countdown":
                        start.countdown(screen, font)
                        countdown_done = True
                        await websocket.send(json.dumps({"type": "countdown_done"}))  # サーバーにカウントダウンが完了したことを通知

                screen.fill((255, 255, 255))

                # x と y の初期化
                x, y = player_instance._rect.x, player_instance._rect.y

                if player_id in players:
                    # target_player_idがNoneでないことを確認
                    if target_player_id is not None:
                        if game.is_playing() and players[target_player_id]['flag']:
                            game.update()
                            game.draw(screen)
                            if target_player_id is not None and target_player_id in players:
                                opponent_score_surface = pygame.font.Font(None, 36).render(f"Opponent's Score: {players[target_player_id]['score']}", True, (0, 0, 0))
                                screen.blit(opponent_score_surface, (200, 50))
                        else:
                            # ゲームが終了している場合、勝利または敗北の判定
                            if players[target_player_id]['flag']:
                                resultScene.win_image(screen)
                            else:
                                resultScene.lose_image(screen)
                            resultScene.draw(screen)
                    else:
                        # target_player_idがNoneの場合の処理
                        print("Target player ID is None.")

                    count = game._count
                    players[player_id]['score'] = count  # 自分のスコアを更新

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

                    if data2["type"] == "update":
                        player_data = data2["player_data"]
                        players[player_data["id"]] = {
                            "score": player_data["count"],  # スコアを更新
                            "position": tuple(player_data["position"]),
                            "flag": player_data["flag"]
                        }

                        # 相手のプレイヤーIDを取得
                        my_player_id = player_id
                        for pid in players:
                            if pid != my_player_id:
                                target_player_id = pid  # 相手のプレイヤーID
                                break  # 最初の相手を選択

                except Exception as e:
                    print(f"Receive error: {e}")

                # ルームID表示
                if room_id is not None:
                    font = pygame.font.Font(None, 36)
                    room_text = font.render(f"Room ID: {room_id}", True, (0, 0, 0))
                    screen.blit(room_text, (10, 10))


                pygame.display.update()
                clock.tick(30)
                
                #イベント処理
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