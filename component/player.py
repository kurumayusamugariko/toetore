import pygame 

class Player():
    def __init__(self):
        # 初期画像プロパティ
        self._image = pygame.image.load("./image/エイム.png")
        self._image = pygame.transform.scale(self._image, (100, 100))
        
        # プレイヤーの初期位置
        self._rect = pygame.Rect(1280 / 2, 720 / 2, 100, 100)

        # プレイヤーのスピード
        self._speed = 50

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
        # プレイヤーの初期位置
        self._rect = pygame.Rect(1280 / 2, 720 / 2, 100, 100)

    def draw(self, screen):
        screen.blit(self._image, self._rect)

    def change_image(self, new_image):
        """画像を切り替えるメソッド"""
        self._image = new_image
