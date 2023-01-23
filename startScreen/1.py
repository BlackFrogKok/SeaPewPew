import pygame
import sys
import button


pygame.init()

res = width, height = (640, 512)

fps = 60
fpsClock = pygame.time.Clock()

sc = pygame.display.set_mode((width, height))

screen = pygame.display.set_mode(res)

dog_surf = pygame.image.load('mor.gif')
dog_rect = dog_surf.get_rect(
    bottomright=(width, height))
sc.blit(dog_surf, dog_rect)


while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()

    for object in button.objects:
        object.process()

    pygame.display.flip()
    fpsClock.tick(fps)
    pygame.display.update()





