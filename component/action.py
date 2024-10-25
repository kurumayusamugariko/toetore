import pygame 
import random

class Action():
    def __init__(self, target_instance, player_instance):
        self._count = 0
        self._target_instance = target_instance
        self._player_instance = player_instance
        self._font1 = pygame.font.SysFont("hg正楷書体pro", 30)
        self._space_pressed = False
        self._hit = False
        self._is_playing = True  # 初期化

    def is_playing(self):
        return self._is_playing

    def reset(self):
        self._is_playing = True
        self._count = 0  # カウントをリセット
        self._player_instance.reset()
        self._target_instance.update()

    def update(self):
        keys = pygame.key.get_pressed()
        self._target_instance.update()
        self._player_instance.update()

        if keys[pygame.K_SPACE]:
            if not self._hit and not self._space_pressed:
                if self._target_instance._rect.colliderect(self._player_instance._rect):
                    self._hit = True
                    self._count += 1
                    if self._count >= 5:  # 5回当たったら
                        self._is_playing = False
                    self._target_instance._rect.x = random.randint(0, 1280 - self._target_instance._rect.width)
                    self._target_instance._rect.y = random.randint(0, 720 - self._target_instance._rect.height)
                self._space_pressed = True
        else:
            self._space_pressed = False
            self._hit = False

    def draw(self, screen):
        self._target_instance.draw(screen)
        self._player_instance.draw(screen)
        count_text = self._font1.render(f"Count: {self._count}", True, (0, 0, 0))
        screen.blit(count_text, (1100, 650))
