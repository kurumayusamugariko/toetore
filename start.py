import pygame
import time
import os

def countdown(screen, font):
    audio_path = os.path.join(os.path.dirname(__file__), 'audio', '銃火器・構える03.mp3')
    ready_sound = pygame.mixer.Sound(audio_path)
    white_color = (255, 255, 255)
    black_color = (0, 0, 0)
    for i in range(5, 0, -1):
        screen.fill(white_color)
        text = font.render(str(i), True, black_color)
        screen.blit(text, (screen.get_width() / 2 - 50, screen.get_height() / 2 - 50))
        pygame.display.update()
        time.sleep(1)
    screen.fill(white_color)
    text = font.render('START', True, black_color)
    screen.blit(text, (screen.get_width() / 2 - 100, screen.get_height() / 2 - 50))
    pygame.display.update()
    time.sleep(1)
    ready_sound.play()

# class Main:
#     def __init__(self):
#         self.w, self.h = 1280, 720
#         self.screen = pygame.display.set_mode((self.w, self.h))
#         self.clock = pygame.time.Clock()
#         pygame.init()

#     def display_text(self, text, size, color, x, y):
#         font = pygame.font.Font(None, size)
#         text_surface = font.render(text, True, color)
#         self.screen.blit(text_surface, (x, y))

#     def draw_button(self, text, x, y, width, height, color):
#         pygame.draw.rect(self.screen, color, (x, y, width, height))
#         self.display_text(text, 30, (255, 255, 255), x + 10, y + 10)

#     def is_mouse_over_button(self, x, y, width, height):
#         mouse_pos = pygame.mouse.get_pos()
#         return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

#     def main(self):
#         game_start = False
#         white_color = (255, 255, 255)
#         black_color = (0, 0, 0)
#         button_color = (0, 128, 0)

#         while True:
#             self.screen.fill(white_color)
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     return

#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     if self.is_mouse_over_button(540, 360, 200, 50):
#                         game_start = True  # ゲームを開始

#             # ボタンを描画
#             self.draw_button("START", 540, 360, 200, 50, button_color)

#             if game_start:
#                 # ゲームが始まった場合の処理
#                 self.screen.fill(black_color)  # 画面を黒に
#                 self.display_text("Game Started!", 50, white_color, self.w / 2 - 100, self.h / 2)
            
#             pygame.display.update()
#             self.clock.tick(30)

# if __name__ == "__main__":
#     game = Main()
#     game.main()
