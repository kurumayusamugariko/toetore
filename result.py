import pygame
from component import action

class resultScene():
    def __init__(self, game):
        self._game = game
        self.font = pygame.font.Font(None, 50)
        self._image = pygame.image.load("./image/win.png")
        self._image = pygame.transform.scale(self._image, (350, 200))
        self._image2 = pygame.image.load("./image/lose.png")
        self._image2 = pygame.transform.scale(self._image2, (350, 200))

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:  # スペースキーが押されたら
            self._game.reset()  # ゲームをリセット

    def win_image(self, screen):
        screen.blit(self._image, (450, 200))

    def lose_image(self, screen):
        screen.blit(self._image2, (450, 200))

    def draw(self, screen):
        score_msg = self.font.render(f"Your Score: {self._game._count}", True, (0, 0, 0))
        screen.blit(score_msg, (500, 420))  # 結果を画面に描画



