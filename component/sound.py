import pygame

class Sound():
    _instance = None 

    def __init__(self):
        self._shot1 = pygame.mixer.Sound("./audio/銃火器・空撃ち.mp3")
        self._shot2 = pygame.mixer.Sound("./audio/特殊攻撃03.mp3")
        self._start = pygame.mixer.Sound("./audio/銃火器・構える03.mp3")

    def attack1(self):
        self._shot1.play()

    def attack2(self):
        self._shot2.play()

    def start(self):
        self._start.play()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Sound()
        return cls._instance