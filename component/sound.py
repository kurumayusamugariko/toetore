import pygame

class Sound():
    _instance = None 

    def __init__(self):
        self._shot1 = pygame.mixer.Sound("")
        self._shot2 = pygame.mixer.Sound("")
        self._start = pygame.mixer.Sound("")

    def attack1(self):
        self._shot1.play()

    def attack2(self):
        self._shot2.play()

    def start(self):
        self._start.play

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Sound()
        return cls._instance