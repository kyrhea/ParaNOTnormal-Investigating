import pygame 
from pygame.locals import * 
pygame.init() 
w = 800       # width 
h = 400       # height 
screen = pygame.display.set_mode((w, h))     #screen 
running = True 
rect = pygame.Rect(100, 100, 100, 100)     # a rectangle  
while running:                 # game loop 
   event_list = pygame.event.get()     # returns an event list 
   for event in event_list:        # event "controller" loop 
     if event.type== KEYDOWN and event.key== K_ESCAPE:  # if user press Esc 
        running=False 
     elif event.type== QUIT:      # if user press close button 
        running=False 
     if event.type == MOUSEBUTTONDOWN: # if the user pressed a mouse button 
        mouse_pos = pygame.mouse.get_pos() # get the mouse pos 
        if rect.collidepoint(mouse_pos): #checking if the mouse_pos is inside the rectangle 
            print('Hello') 
   screen.fill((0,0,0))       #fill the screen with black 
   pygame.draw.rect(screen, (255,255,255), rect) # draw rectangle on the screen 
   pygame.display.flip() # update the screen 
