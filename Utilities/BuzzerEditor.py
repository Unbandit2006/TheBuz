import pygame
from Classes import *
pygame.init()

window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption('Buzzer Editor')
clock = pygame.time.Clock()

program = Main(window)

running = True
while running:
    window.fill("#121212")

    program.draw()

    clock.tick(60)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

