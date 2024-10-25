import pygame
from pygame.locals import * 
import sys
import random
from component import player
from component import target

class Main():
    def main():
        pygame.init() 

        # 画面設定
        screen = pygame.display.set_mode((1280, 720)) 
        
        # targetインスタンス化
        target_instance = target.Target()

        # playerインスタンス化
        player_instance = player.Player() 


        # 当たった回数
        count = 0

        # 当たった回数を表示
        font1 = pygame.font.SysFont("hg正楷書体pro", 30)

        # スペースキーが押されたかどうか
        space_pressed = False
        hit = False

        while True:
            # 画面の背景色を設定
            screen.fill((255, 255, 255))

            target_instance.update()  # targetの位置を更新
            target_instance.draw(screen)  # targetを描画
            
            player_instance.update()  # playerの位置を更新
            player_instance.draw(screen)  # playerを描画


            # 撃つ処理
            keys = pygame.key.get_pressed()  # キーの状態を取得
            if keys[K_SPACE]:
                if not hit and not space_pressed:
                    if target_instance._rect.colliderect(player_instance._rect):  # playerのrectを使う
                        hit = True
                        count += 1  # カウントを更新
                        # ターゲットの位置を再設定
                        target_instance._rect.x = random.randint(0, w - target_instance._rect.width)
                        target_instance._rect.y = random.randint(0, h - target_instance._rect.height)
                    space_pressed = True
            else:
                space_pressed = False
                hit = False
            
            # 画像の描画
            target_instance.draw(screen) 

            # カウントテキストを描画
            count_text = font1.render(f"Count: {count}", True, (0, 0, 0))
            screen.blit(count_text, (1100, 650))
            
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
