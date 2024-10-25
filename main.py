import pygame
import importlib
pygame.init()
def GetScene(name):
    return importlib.import_module(name).main()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
gamen = [GetScene("game")]
index = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                index += 1
                gamen = []
                gamen.append(GetScene("Gamen" + str((index % 2) + 1)))
    screen.fill((255, 255, 255))
    for g in gamen:
        g.update()
        g.draw(screen)
    pygame.display.update() 
    clock.tick(60)

pygame.quit()