import pygame 
import random

class Action():
    def __init__(self, target_instance, player_instance):
        self._count = 0
        self._target_instance = target_instance
        self._player_instance = player_instance
        self._font1 = pygame.font.SysFont("hg正楷書体pro", 36)
        self._space_pressed = False
        self._hit = False
        self._is_playing = True

    def is_playing(self):
        return self._is_playing

    def reset(self):
        self._is_playing = True
        self._count = 0
        self._player_instance.reset()
        self._target_instance.reset()

    def update(self):
        keys = pygame.key.get_pressed()
        self._target_instance.update()
        self._player_instance.update()

        if keys[pygame.K_SPACE]:
            if not self._hit and not self._space_pressed:
                # プレイヤーの矩形を取得
                player_rect = self._player_instance._rect
                player_rect = pygame.Rect(player_rect.x, player_rect.y, 50, 50)
                # 各ターゲットの矩形を作成
                target_rects = [
                    pygame.Rect(self._target_instance._x, self._target_instance._y, 20, 20),
                    pygame.Rect(self._target_instance._x2, self._target_instance._y2, 100, 100),
                    pygame.Rect(self._target_instance._x3, self._target_instance._y3, 100, 100)
                ]
                
                
                if target_rects[0].colliderect(player_rect):
                    self._hit = True
                    self._count += 1
                    if self._count >= 5:
                        self._is_playing = False
                    self._target_instance.reset()  # 新しい問題に切り替え

                self._space_pressed = True
        else:
            self._space_pressed = False
            self._hit = False

    def draw(self, screen):
        self._target_instance.draw(screen)
        self._player_instance.draw(screen)
        count_text = self._font1.render(f"Your Score: {self._count}", True, (0, 0, 0))
        screen.blit(count_text, (800, 50))