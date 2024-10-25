import pygame
from pygame.locals import * 
import sys
import random
from component import player
from component import target
from component import action

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

        while True:
            # 画面の背景色を設定
            screen.fill((255, 255, 255))

            target_instance.update()  # targetの位置を更新
            target_instance.draw(screen)  # targetを描画
            
            player_instance.update()  # playerの位置を更新
            player_instance.draw(screen)  # playerを描画

            game.update()  # 当たり判定を更新
            game.draw(screen)  # カウントを描画
            
            # 画面更新
            pygame.display.update() 
            
            # 更新時間間隔
            pygame.time.wait(30)
            
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
