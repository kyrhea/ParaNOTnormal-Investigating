import pygame
win = pygame.display.set_mode((1000,800))


def fade(width, height): 
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        redrawWindow()
        win.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(5)


def redrawWindow():
    win.fill((255,255,255))
    pygame.draw.rect(win,(255,0,0),(200,300,200,200),0)
    pygame.draw.rect(win,(0,255,0),(500,500,100,200),0)



run = True
while run:
    redrawWindow()
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            fade(1000,800)
    pygame.display.update()

