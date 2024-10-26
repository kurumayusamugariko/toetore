import pygame 
import random
import json

class Target():
    def rand_ints_nodup(self, a, b, k):
        ns = []
        while len(ns) < k:
            n = random.randint(a, b)
            if n not in ns:
                ns.append(n)
        return ns

    def __init__(self):
        self.load_data()
        self.select_questions()
        self.initialize_positions()
        self.initialize_movement()

    def load_data(self):
        try:
            with open("./anyway.json", "r") as file:
                self._data = json.load(file)
        except FileNotFoundError:
            print("Error: File not found. Please check the file path.")
            return

    def select_questions(self):
        max_id = len(self._data) - 1
        self._list = self.rand_ints_nodup(1, max_id, 3)
        self._ID1, self._ID2, self._ID3 = map(str, self._list)

        self._font = pygame.font.Font(None, 36)
        self.update_question_data(self._ID1)

    def update_question_data(self, question_id):
        self._sentence = self._data[question_id][1]
        self._sentence_surface = self._font.render(self._sentence, True, (0, 0, 0))

        self._japanese = self._data[question_id][3]
        self._japanese_surface = self._font.render(self._japanese, True, (0, 0, 0))

        self._anser = self._data[question_id][2]
        self._anser_surface = self._font.render(self._anser, True, (0, 0, 0))
        self._dammy1 = self._data[self._ID2][2]
        self._dammy1_surface = self._font.render(self._dammy1, True, (0, 0, 0))
        self._dammy2 = self._data[self._ID3][2]
        self._dammy2_surface = self._font.render(self._dammy2, True, (0, 0, 0))

    def initialize_positions(self):
        text_width, text_height = self._anser_surface.get_size()
        self._x = random.randint(0, 1100 - text_width)
        self._y = random.randint(0, 600 - text_height)

        self._x2 = random.randint(0, 1100 - text_width)
        self._y2 = random.randint(0, 600 - text_height)

        self._x3 = random.randint(0, 1100 - text_width)
        self._y3 = random.randint(0, 600 - text_height)

    def initialize_movement(self):
        self._speed = 5
        self._moved = self._moved2 = self._moved3 = 0
        self._up = self._up2 = self._up3 = True

    def update(self):
        self.move_target()
        
    def move_target(self):
        # メインターゲットの上下移動
        if self._up:
            self._y -= self._speed
            self._moved += self._speed
            if self._moved >= 100:
                self._up = False
                self._moved = 0
        else:
            self._y += self._speed
            self._moved += self._speed
            if self._moved >= 100:
                self._up = True
                self._moved = 0

        # ダミー1
        if self._up2:
            self._y2 -= self._speed
            self._moved2 += self._speed
            if self._moved2 >= 100:
                self._up2 = False
                self._moved2 = 0
        else:
            self._y2 += self._speed
            self._moved2 += self._speed
            if self._moved2 >= 100:
                self._up2 = True
                self._moved2 = 0

        # ダミー2
        if self._up3:
            self._y3 -= self._speed
            self._moved3 += self._speed
            if self._moved3 >= 100:
                self._up3 = False
                self._moved3 = 0
        else:
            self._y3 += self._speed
            self._moved3 += self._speed
            if self._moved3 >= 100:
                self._up3 = True
                self._moved3 = 0

    def draw(self, screen):
        screen.blit(self._anser_surface, (self._x, self._y))  
        screen.blit(self._dammy1_surface, (self._x2, self._y2))  
        screen.blit(self._dammy2_surface, (self._x3, self._y3)) 
        screen.blit(self._sentence_surface, (640, 650))
        screen.blit(self._japanese_surface, (640, 550))

    def reset(self):
        self.select_questions()
        self.initialize_positions()