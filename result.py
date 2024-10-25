import pygame
from component import action

class resultScene():
    def __init__(self, game):
        self._game = game
        self.font = pygame.font.Font(None, 50)

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:  # スペースキーが押されたら
            self._game.reset()  # ゲームをリセット

    def draw(self, screen):
        score_msg = self.font.render(f"Your Score: {self._game._count}", True, (0, 0, 0))
        screen.blit(score_msg, (640, 360))  # 結果を画面に描画



