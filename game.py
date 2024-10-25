import pygame
from pygame.locals import * 
import sys
import random
from component import player
from component import target
from component import action
import result

class Main():
    def main():
        pygame.init()

        # 画面設定
        screen = pygame.display.set_mode((1280, 720))

        # targetインスタンス化
        target_instance = target.Target()

        # playerインスタンス化
        player_instance = player.Player()

        # actionインスタンス化
        game = action.Action(target_instance, player_instance)

        resultScene = result.resultScene(game)  # スコアは直接ゲームから取得

        clock = pygame.time.Clock()  # Clockを初期化

        while True:
            screen.fill((255, 255, 255))

            if game.is_playing():
                game.update()  # 当たり判定を更新
                game.draw(screen)  # カウントを描画
            else:
                resultScene.draw(screen)  # 結果を描画

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



    if __name__ == "__main__":
        main()
