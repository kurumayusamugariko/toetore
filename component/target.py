import pygame 
import random

class Target():
    def __init__(self):
        # 画像プロパティ
        self._image = pygame.image.load("./image/target.png")
        self._image = pygame.transform.scale(self._image, (100, 100))
        
        # ターゲットの初期位置
        self._rect = self._image.get_rect()
        self._rect.x = random.randint(0, 1280 - self._rect.width)
        self._rect.y = random.randint(0, 720 - self._rect.height)

        # スピード
        self._speed = 5  # 移動する距離

        # 移動距離
        self._moved = 0

        # 上がる上限
        self._up = True


    def update(self):
        # 画像の上下移動
        if self._up:
            self._rect.y -= self._speed  # 上に移動
            self._moved += self._speed
            if self._moved >= 300:
                self._up = False
                self._moved = 0
        else:
            self._rect.y += self._speed  # 下に移動
            self._moved += self._speed
            if self._moved >= 300:
                self._up = True
                self._moved = 0
        

    def draw(self, screen):
        screen.blit(self._image, self._rect)