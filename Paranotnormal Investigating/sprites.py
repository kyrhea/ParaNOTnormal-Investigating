import pygame
from config import *
import math
import random
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = player_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height =  tilesize

        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'

        self.image = pygame.image.load('./img/boy01.png')
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize)) #sprite size/image

        self.rect = self.image.get_rect() #hitbox the same size as sprite image
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        self.movement()
        

        self.rect.x += self.x_change
        self.collide('x')
        self.rect.y += self.y_change
        self.collide('y')

        


        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += player_speed
            self.x_change -= player_speed
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -=player_speed
            self.x_change += player_speed
            self.facing = 'right'

        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += player_speed
            self.y_change -= player_speed
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= player_speed
            self.y_change += player_speed
            self.facing = 'down'

    def collide(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
           # hits = pygame.sprite.spritecollide(self, self.game.door, False)
            hit = pygame.sprite.spritecollide(self,self.game.door, True)

            if hits:
                #right
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0: #left
                    #hits[0] = wall colliding with
                    self.rect.x = hits[0].rect.right
       
        
                    
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                #down
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
            
   

            
    
        
    

                
       
               




#NOT FINISHED
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.layer = enemy_layer
        self.groups = self.game.all_sprites, self.game.ghosts
        pygame.sprite.Sprite._init_(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.x_change = 0
        self.y_change = 0

        #self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)

        #self.image.set_colorkey(black)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

        



class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(blue)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        




class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('./img/pixel_font.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)
    
    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class mainDoor(pygame.sprite.Sprite):
    def __init__(self,game,x,y):

        self.game = game
        self._layer = player_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

    

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(white)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

       
                

   
        




#NOT FINISHED
class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game = game
        self.x = x
        self.y = y
        self.width = tilesize
        self.height = tilesize

        self.animation_loop = 0


        self.image = self.game.attack_spritesheet.get_sprite(0,0, self.width, self.height)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing



        
class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(green)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        #self.clicked = False


class Cat(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = player_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height =  tilesize

    
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(white)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if rect.collidepoint(pos):
                    Text.message1()
    def update(self):
        self.is_clicked()
                    

        
class Text(pygame.sprite.Sprite):
    def __init__(self, x, y, messages):
        self.font = pygame.font.Font('freesansbold.ttf', 24)

        self.snip = font.render('', True, 'white')
        self.counter = 0
        self.speed = 3
        
        self.done = True
        self.message= messages[self.active_message]


        def message1(self):
            self.clock.tick(60)
            self.messages = ["hi"]
            pygame.draw.rect(self.screen, 'dark gray', [0, 300, 800,200])
            self.active_message =0

            if self.counter < self.speed * len(self.message):
                self.counter +=1
            elif self.counter >= self.speed*len(self.message):
                self.done = True
            
##            keys = pygame.key.get_pressed()
##            if keys[pygame.K_RETURN and self.done and self.active_message < len(self.message)-1:
##                    self.active_message += 1
##                    self.done = False
##                    self.message = messages{active_message]
##                    self.counter = 0

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and done and self.active_message < len(self.messages)-1 :
                             self.active_message +=1
                             self.done = False
                             self.message = messages[active_message]
                             self.counter = 0
            
        
    
        
 
       
        




##
##class openDoor(pygame.sprite.Sprite):
##    def __init__(self, game, x,y):
##        self.game = game
##        self._layer = player_layer
##        self.groups = self.game.all_sprites, self.game.door
##        pygame.sprite.Sprite.__init__(self, self.groups)
##        self.x = x
##        self.y = y
##        self.width = tilesize
##        self.height = tilesize
##
##        self.animation_loop = 0
##
##
##        self.image = self.game.attack_spritesheet.get_sprite(0,0, self.width, self.height)
##
##
##        self.rect = self.image.get_rect()
##        self.rect.x = self.x
##        self.rect.y = self.y
##
##    def update(self):
##        self.animate()
##        self.collide()
##
##    def collide(self):
##        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
##
##    def animate(self):
##        direction = self.game.player.facing
##
##



    





        
  
    

    