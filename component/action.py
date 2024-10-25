import pygame 
import random

class Action():
    def __init__(self, target_instance, player_instance):
        self._count = 0
        self._target_instance = target_instance
        self._player_instance = player_instance

        # 当たった回数を表示
        self._font1 = pygame.font.SysFont("hg正楷書体pro", 30)

        # スペースキーが押されたかどうか
        self._space_pressed = False
        self._hit = False

    def update(self):
        keys = pygame.key.get_pressed()  # キーの状態を取得
        if keys[pygame.K_SPACE]:
            if not self._hit and not self._space_pressed:
                if self._target_instance._rect.colliderect(self._player_instance._rect):  # playerのrectを使う
                    self._hit = True
                    self._count += 1  # カウントを更新
                    # ターゲットの位置を再設定
                    self._target_instance._rect.x = random.randint(0, 1280 - self._target_instance._rect.width)
                    self._target_instance._rect.y = random.randint(0, 720 - self._target_instance._rect.height)
                self._space_pressed = True
        else:
            self._space_pressed = False
            self._hit = False

    def draw(self, screen):
        # カウントテキストを描画        
        count_text = self._font1.render(f"Count: {self._count}", True, (0, 0, 0))
        screen.blit(count_text, (1100, 650))
