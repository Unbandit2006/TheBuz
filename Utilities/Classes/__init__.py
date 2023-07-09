import pygame
pygame.init()

class IntroPage:
    def __init__(self, parent: pygame.surface.SurfaceType) -> None:
        pass

    def draw(self):
        pass

    def handle_event(self):
        pass


class Main:
    def __init__(self, parent: pygame.surface.SurfaceType) -> None:
        '''
        This is the main class it will be the only thing running in BuzzerEditor.py
        All events and things will go through this class
        '''

        self.parent = parent

    def draw(self):
        pass

