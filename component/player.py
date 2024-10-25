import pygame 

class Player():
    def __init__(self):
        # 画像プロパティ
        self._image = pygame.image.load("./image/エイム.png")
        self._image = pygame.transform.scale(self._image, (100, 100))
        
        # playerの初期位置
        self._rect = pygame.Rect(1280 / 2, 720 / 2, 100, 100)
        
        # playerのスピード
        self._speed = 30




    def update(self):
        key = pygame.key.get_pressed()

        # 移動処理
        if key[pygame.K_LEFT]:
            self._rect.move_ip(-self._speed, 0)
        if key[pygame.K_RIGHT]:
            self._rect.move_ip(self._speed, 0)
        if key[pygame.K_UP]:
            self._rect.move_ip(0, -self._speed)
        if key[pygame.K_DOWN]:
            self._rect.move_ip(0, self._speed)

    def reset(self):        
        # playerの初期位置
        self._rect = pygame.Rect(1280 / 2, 720 / 2, 100, 100)


    def draw(self, screen):
        screen.blit(self._image, self._rect)