import pygame
from config import *
import math
from pygame.locals import *
from cutscene import *


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(black)
        return sprite

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
        self.animation_loop = 1

        self.image = pygame.image.load(r'C:\Users\saira\paragame\ParaNOTnormal-Investigating\Paranotnormal Investigating\img\boy01.png')
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize)) #sprite size/image

        self.rect = self.image.get_rect() #hitbox the same size as sprite image
        self.rect.x = self.x
        self.rect.y = self.y
    
    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(0, 0, self.width, (self.height - 2)),
            self.game.character_spritesheet.get_sprite(64, 0, self.width, (self.height - 2)),
            self.game.character_spritesheet.get_sprite(128, 0, self.width, (self.height - 2)),
            self.game.character_spritesheet.get_sprite(192, 0, self.width, (self.height - 2))]

        up_animations = [self.game.character_spritesheet.get_sprite(0, 124, self.width, (self.height - 2)),
            self.game.character_spritesheet.get_sprite(64, 124, self.width, (self.height - 2)),
            self.game.character_spritesheet.get_sprite(126, 124, self.width, (self.height - 2)),
            self.game.character_spritesheet.get_sprite(192, 124, self.width, (self.height - 2))]

        left_animations = [self.game.character_spritesheet.get_sprite(0, 187, self.width, (self.height - 2)),
            self.game.character_spritesheet.get_sprite(64, 187, self.width, (self.height - 2)),
            self.game.character_spritesheet.get_sprite(128, 187, self.width, (self.height - 2)),
            self.game.character_spritesheet.get_sprite(192, 187, self.width, (self.height - 2))]

        right_animations = [self.game.character_spritesheet.get_sprite(0, 64, self.width, (self.height - 4)),
            self.game.character_spritesheet.get_sprite(64, 64, self.width, (self.height - 4)),
            self.game.character_spritesheet.get_sprite(128, 64, self.width, (self.height - 4)),
            self.game.character_spritesheet.get_sprite(192, 64, self.width, (self.height - 4))]
        
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, (self.height - 2))
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.12
                if self.animation_loop >=4:
                    self.animation_loop = 1
        
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 124, self.width, (self.height - 2))
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.12
                if self.animation_loop >=4:
                    self.animation_loop = 1
        
        if self.facing == 'right':
            if self.x_change == 0:
                self.game.character_spritesheet.get_sprite(64, 0, self.width, (self.height - 4))
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.12
                if self.animation_loop >=4:
                    self.animation_loop = 1
        
        if self.facing == 'left':
            if self.x_change == 0:
                self.game.character_spritesheet.get_sprite(0, 187, self.width, (self.height - 2))
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.12
                if self.animation_loop >=4:
                    self.animation_loop = 1
    
    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.collide('x')
        self.collideCat('x')
        self.collideMainDoor('x')
        self.collideDoor('x')
        self.collideCorner('x')
        self.collideWoman('x')
        self.collideEnemy('x')
        self.rect.y += self.y_change
        self.collide('y')
        self.collideMainDoor('y')
        self.collideCat('y')
        
        self.collideCorner('y')
        self.collideWoman('y')
        self.collideEnemy('y')
        self.collideDoor('y')



        


        self.x_change = 0
        self.y_change = 0







    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += player_speed
            self.x_change -= player_speed
            self.facing = 'left'

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -=player_speed
            self.x_change += player_speed
            self.facing = 'right'

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += player_speed
            self.y_change -= player_speed
            self.facing = 'up'
        
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= player_speed
            self.y_change += player_speed
            self.facing = 'down'

    def collide(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks , False)
            
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
    def collideCorner(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.cornerBlock , False)
            
            if hits:
                #right
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0: #left
                    #hits[0] = wall colliding with
                    self.rect.x = hits[0].rect.right
       
        
                    
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.cornerBlock, False)
           

            if hits:
                #down
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def collideCat(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.cat , False)
            
            if hits:
                #right
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0: #left
                    #hits[0] = wall colliding with
                    self.rect.x = hits[0].rect.right
       
        
                    
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.cat, False)
           

            if hits:
                #down
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
    def collideWoman(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.woman , False)
            
            if hits:
                #right
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0: #left
                    #hits[0] = wall colliding with
                    self.rect.x = hits[0].rect.right
       
        
                    
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.woman, False)
           

            if hits:
                #down
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def collideEnemy(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.ghost, False)
            
            if hits:
                self.kill()
                self.game.playing = False
       
        
     


    def collideMainDoor(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.mainDoor , False)
            
            if hits:
                #right
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0: #left
                    #hits[0] = wall colliding with
                    self.rect.x = hits[0].rect.right
       
        
                    
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.mainDoor, False)
           

            if hits:
                #down
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def collideDoor(self, direction):

        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.door , False)
            
            if hits:
                #right
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0: #left
                    #hits[0] = wall colliding with
                    self.rect.x = hits[0].rect.right
       

       
        
                    
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.door, False)
           

            if hits:
                #down
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
      

       






            
            
            
   

            
    
        
    

                
       
               

class Enemy2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = enemy_layer
        self.groups = self.game.all_sprites, self.game.ghost
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.screen = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)


        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.x_change = 0
        self.y_change = 0

        #self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)

        #self.image.set_colorkey(black)
        self.image = self.game.cuteghost_spritesheet.get_sprite(0, 0, self.width, (self.height-10))
        self.animation_loop = 1
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.clicked = False
        self.t = False
        self.r = False
        self.p = False
    def transform(self):
        self.transform_spritesheet = Spritesheet(r'C:\Users\saira\paragame\ParaNOTnormal-Investigating\Paranotnormal Investigating\img\evo_ss.png')
        
        self.transform_animations = [self.transform_spritesheet.get_sprite(0, 0, self.width, (self.height-10)),
        self.transform_spritesheet.get_sprite(64, 0, self.width, (self.height-10)),
        self.transform_spritesheet.get_sprite(128, 0, self.width, (self.height-10)),
        self.transform_spritesheet.get_sprite(0, 64, self.width, (self.height-10)),
        self.transform_spritesheet.get_sprite(64, 64, self.width, (self.height-10)),]


        
        self.image = self.transform_animations[math.floor(self.animation_loop)]
        
        self.animation_loop += 0.02
        if self.animation_loop >=4:
            self.animation_loop = 1
    def update(self):
        self.transform()
        pygame.time.delay(400)
        self.game.main4()
        
       
       



class Enemy3(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = enemy_layer
        self.groups = self.game.all_sprites, self.game.ghost
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.screen = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)


        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.x_change = 0
        self.y_change = 0

        #self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)

        #self.image.set_colorkey(black)
        self.image = self.game.angryghost_spritesheet.get_sprite(0, 0, self.width, (self.height-10))
        self.animation_loop = 1
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.clicked = False
    def angry(self):
        angry_animations = [self.game.angryghost_spritesheet.get_sprite(0, 0, self.width, (self.height-10)),
        self.game.angryghost_spritesheet.get_sprite(64, 0, self.width, (self.height-10)),
        self.game.angryghost_spritesheet.get_sprite(0, 64, self.width, (self.height-10)),
        self.game.angryghost_spritesheet.get_sprite(64, 64, self.width, (self.height-10)),]

        self.image = angry_animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.05
        if self.animation_loop >=4:
            self.animation_loop = 0
    def update(self):
        self.angry()
      


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = enemy_layer
        self.groups = self.game.all_sprites, self.game.ghost
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.screen = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)


        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.x_change = 0
        self.y_change = 0

        #self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)

        #self.image.set_colorkey(black)
        self.image = self.game.cuteghost_spritesheet.get_sprite(0, 0, self.width, (self.height-10))
        self.animation_loop = 1
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.clicked = False
        self.t = False
        self.r = False
        self.p = False
    
    def animate(self):
        cute_animations = [self.game.cuteghost_spritesheet.get_sprite(0, 0, self.width, (self.height-10)),
        self.game.cuteghost_spritesheet.get_sprite(64, 0, self.width, (self.height-10)),
        self.game.cuteghost_spritesheet.get_sprite(0, 64, self.width, (self.height-10)),
        self.game.cuteghost_spritesheet.get_sprite(64, 64, self.width, (self.height-10)),]

        self.image = cute_animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.05
        if self.animation_loop >=4:
            self.animation_loop = 1
    
    def angry(self):
        angry_animations = [self.game.angryghost_spritesheet.get_sprite(0, 0, self.width, (self.height-10)),
        self.game.angryghost_spritesheet.get_sprite(64, 0, self.width, (self.height-10)),
        self.game.angryghost_spritesheet.get_sprite(0, 64, self.width, (self.height-10)),
        self.game.angryghost_spritesheet.get_sprite(64, 64, self.width, (self.height-10)),]

        self.image = angry_animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.05
        if self.animation_loop >=4:
            self.animation_loop = 0


    
    def flick(self):
        r=1
        
        while r<10:
            self.screen.fill(pygame.Color('black'))
            pygame.display.update()
            pygame.time.wait(1)
            self.screen.fill(pygame.Color('white'))
            pygame.display.update()
            pygame.time.wait(1)
            r+=1  
            pygame.time.delay(10)
        
        self.game.main3()

     


   
    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
               
        
                self.clicked = True
                self.flick()
                self.t = True
               
                

            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
        return self.clicked
    
 

    def update(self):
       
       
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.animate()
        self.x_change = 0
        self.y_change = 0
        self.is_clicked()
        if self.p == True:
            self.transform()
        
            #self.r = True
            #self.t = False
        # if self.r == True:
        #     self.angry()


        



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

        self.image = self.game.tile_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Block2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.tile_spritesheet.get_sprite(64, 64, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground1(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ground_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.tile_spritesheet.get_sprite(192, 64, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ground_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.tile_spritesheet.get_sprite(256, 64, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Block3(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.tile_spritesheet.get_sprite(0, 64, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class cornerBlock(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.cornerBlock
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.tile_spritesheet.get_sprite(128, 0, self.width, self.height)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ground_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.tile_spritesheet.get_sprite(192, 64, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        




class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font(r'C:\Users\saira\paragame\ParaNOTnormal-Investigating\Paranotnormal Investigating\img\pixel_font.ttf', fontsize)
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
    def __init__(self,game, x, y):
        self.game = game
        self._layer = player_layer
        self.groups = self.game.all_sprites, self.game.mainDoor
        #self.screen = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)

        #self.win = pygame.display.set_mode((win_width,win_height))
        self.screen = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)

        self.clicked = False
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height =  tilesize

    
        self.image = self.game.tile_spritesheet.get_sprite(128, 64, self.width, (self.height*2))
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))
        #self.image = pygame.transform.scale(self.image, (tilesize, tilesize))
        #self.image.fill(white)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
               
                self.clicked = True
                
                door_noise = pygame.mixer.Sound(r'C:\Users\saira\paragame\ParaNOTnormal-Investigating\Paranotnormal Investigating\img\door_sound.wav')
                pygame.mixer.Sound.play(door_noise)
                
                self.fade(2000, 1000)
                

            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
        return self.clicked
        #self.screen.blit((self.image,(self.rect.x, self.rect.y) ))
        
        
    def update(self):
        self.is_clicked()

    def fade(self, width, height): 
        fade = pygame.Surface((width, height))
        fade.fill((0,0,0))
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(7)
        self.game.main2()
   

            
       
        

                

   
        




#NOT FINISHED
class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game = game
        self._layer = player_layer
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

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
        hits = pygame.sprite.spritecollide(self, self.game.ghost, True)

    def animate(self):
        direction = self.game.player.facing
        right_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                        #    self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                        #    self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                        #    self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           ]

        # down_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
        #                    self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
        #                    self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
        #                    self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height)
        #                    ]

        # left_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
        #                    self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
        #                    self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
        #                    self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height)]

        # up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
        #                    self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
        #                    self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
        #                    self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height)]
        if direction == 'up':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 1:
                self.kill()
        if direction == 'down':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 1:
                self.kill()
        if direction == 'left':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 1:
                self.kill()
        if direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 1:
                self.kill()



        
class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.door
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.tile_spritesheet.get_sprite(128, 64, self.width, (self.height*2))
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.clicked = False
        self.open = False
       
    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked: 
                self.clicked = True
                self.locked()
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
        return self.clicked
    
    def locked(self):
        #Player.collideDoor(self, any)
        #k.inventory(self)
        if self.game.keys != 0:
            self.unlock()
            door_noise = pygame.mixer.Sound(r'C:\Users\saira\paragame\ParaNOTnormal-Investigating\Paranotnormal Investigating\img\door_sound.wav')
            pygame.mixer.Sound.play(door_noise)
            self.game.cut_scene_manager.start_cut_scene(CutSceneFour(self))

            
    
    def unlock(self):
        
        pygame.sprite.spritecollide(self.game.player, self.game.door, True)

        self.kill()

        #self.game.keys -= 1
        self.open = True


    def update(self):
        self.is_clicked()
        




class Cat(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.clock = pygame.time.Clock()
        self.game = game
        self._layer = player_layer
        self.groups = self.game.all_sprites, self.game.cat
        self.screen = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)
        #self.win = pygame.display.set_mode((win_width,win_height))
        self.clicked = False
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height =  tilesize

    
        self.image = self.game.cat_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.animation_loop = 0
        #self.image.fill(white)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def animate(self):
        cat_animations = [self.game.cat_spritesheet.get_sprite(0, 0, self.width, self.height),
        self.game.cat_spritesheet.get_sprite(64, 0, self.width, self.height)]

        self.image = cat_animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.07
        if self.animation_loop >=2:
            self.animation_loop = 0
        
    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
               
                self.clicked = True
                self.message1()
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
        return self.clicked
        #self.screen.blit((self.image,(self.rect.x, self.rect.y) ))
    
  
        
        
    def update(self):
        self.is_clicked()
        self.animate()
       
        

        #pygame.display.update()

        


    def message1(self):
        #pygame.draw.rect(self.screen, 'dark gray', [0, 300, 800,200])
     
        
        self.font = pygame.font.Font('./img/pixel_font.ttf', 24)
        self.snip = self.font.render('', True, 'white')
        self.counter = 0
        self.speed = 3
        self.active_message = 0
        self.done = False
        self.messages = ['hi there',
                         'whats up']
        self.message= self.messages[self.active_message]


        m = True
        while m:
            pygame.draw.rect(self.screen, 'dark gray', [0, 550, 1500,200])


            
            self.clock.tick(fps)
                    
                    
          

            if self.counter < self.speed * len(self.message):
                self.counter +=1
    
            elif self.counter >= self.speed*len(self.message):

                self.done = True
                
           
           
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.done and self.active_message < len(self.messages)-1:
                            
                            self.active_message += 1
                            self.done = False
                            self.message = self.messages[self.active_message]
                            self.counter = 0
                    else:
                        m = False
                          

                    
            snip = self.font.render(self.message[0:self.counter//self.speed], True, 'white')
                #blit the snip
            self.screen.blit(snip, (10, 560))
                    
            pygame.display.flip()


            

class k(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = player_layer
        self.groups = self.game.all_sprites, self.game.key        #self.win = pygame.display.set_mode((win_width,win_height))
        self.clicked = False
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height =  tilesize
        self.game.keys = 0
        self.haveKey = False

    
        self.image = pygame.image.load(r'C:\Users\saira\paragame\ParaNOTnormal-Investigating\Paranotnormal Investigating\img\key.png')
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))
        #self.image.fill(white)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        
    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                self.game.cut_scene_manager.start_cut_scene(CutSceneFive(self))
                self.inventory()
                self.kill()
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
        return self.clicked
    
    def inventory(self):
        
        self.game.keys += 1
        self.haveKey = True
        #Door.unlock(self)
        
        
        
    def update(self):
        self.is_clicked()


           

                        

class woman(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.clock = pygame.time.Clock()
        self.game = game
        self._layer = player_layer
        self.groups = self.game.all_sprites, self.game.woman
        self.screen = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)
        #self.win = pygame.display.set_mode((win_width,win_height))
        self.clicked = False
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height =  tilesize

    
        self.image = pygame.image.load(r'C:\Users\saira\paragame\ParaNOTnormal-Investigating\Paranotnormal Investigating\img\woman.png')
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))
        #self.image.fill(white)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        
    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
               
                self.clicked = True
                #self.game.cut_scene_manager()
                self.game.cut_scene_manager.start_cut_scene(CutSceneOne(self))
                if self.game.cut_scene_manager.cut_scene is None:
                    self.message1()
                
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
        return self.clicked
        #self.screen.blit((self.image,(self.rect.x, self.rect.y) ))
        
        
    def update(self):
        self.is_clicked()
       
        

        #pygame.display.update()

        


    def message1(self):
        #pygame.draw.rect(self.screen, 'dark gray', [0, 300, 800,200])
     
        
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.snip = self.font.render('', True, 'white')
        self.counter = 0
        self.speed = 3
        self.active_message = 0
        self.done = False
        self.messages = ['Please help!']
        self.message= self.messages[self.active_message]


        m = True
        while m:
            pygame.draw.rect(self.screen, 'dark gray', [0, 550, 1500,200])


            
            self.clock.tick(fps)
                    
                    
          

            if self.counter < self.speed * len(self.message):
                self.counter +=1
    
            elif self.counter >= self.speed*len(self.message):

                self.done = True
                
           
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.done and self.active_message < len(self.messages)-1:
                            
                            self.active_message += 1
                            self.done = False
                            self.message = self.messages[self.active_message]
                            self.counter = 0
                    else:
                        m = False
                          

                    
            snip = self.font.render(self.message[0:self.counter//self.speed], True, 'white')
                #blit the snip
            self.screen.blit(snip, (10, 560))
                    
            pygame.display.flip()

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)


        
 
       
        




    





        
  
    

    