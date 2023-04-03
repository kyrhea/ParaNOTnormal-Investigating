import pygame, sys

from sprites import *
from config import *
from cutscene import *

from pygame.locals import *



class Game:
    def __init__(self):
        pygame.init()
        self.state = 'intro'
        self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.screen = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)

        self.fullscreen = False
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('.\img\pixel_font.ttf', 32)
        self.running = True

        pygame.mixer.music.load('./img/back_music.wav')
        pygame.mixer.music.play(-1)

        self.intro_background = pygame.image.load('.\img\start_para.png')
        self.intro_background = pygame.transform.scale(self.intro_background, (win_width, win_height))

        self.character_spritesheet = Spritesheet('./img/boy_ss.png')
        self.tile_spritesheet = Spritesheet('./img/tile_ss.png')
        self.cute_spritesheet = Spritesheet('./img/cute_ss.png')
        self.cat_spritesheet = Spritesheet('./img/cat_ss.png')

        self.cut_scene_manager = CutSceneManager(self.screen)
        self.fog = pygame.Surface((2000, 2000))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pygame.image.load(r'C:\Users\saira\paragame\ParaNOTnormal-Investigating\Paranotnormal Investigating\img\light_350_med.png').convert_alpha()
        self.light_mask = pygame.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
        self.camera = Camera(win_width, win_height)


    def createTilemap(self):
        #loop through tilemap
        #enumerate gets position and content of item
        
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                Ground2(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == "M":
                    mainDoor(self, j, i)
                if column == 'Q':
                    cornerBlock(self, j, i)
                if column == 'W':
                    woman(self, j, i)
                
                    
    def createTilemap2(self):
        #loop through tilemap
        #enumerate gets position and content of item
        for i, row in enumerate(tilemap2):
            for j, column in enumerate(row):
                Ground(self, j, i)
                Ground1(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == "D":
                    Door(self, j, i)
                if column == "C":
                    Cat(self,j,i)
                if column == 'K':
                    k(self, j, i)
                if column == 'E':
                    Enemy(self, j, i)
                if column == 'S':
                    Block2(self, j, i)
                if column == 'T':
                    Block3(self,j,i)
            
    



    def newGame(self):
        #new game starts
        self.playing = True #if player dies or quits

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.ghost = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.door = pygame.sprite.LayeredUpdates()
        self.mainDoor = pygame.sprite.LayeredUpdates()
        self.cat = pygame.sprite.LayeredUpdates()
        self.key = pygame.sprite.LayeredUpdates()
        self.cornerBlock = pygame.sprite.LayeredUpdates()
        self.woman = pygame.sprite.LayeredUpdates()



        self.createTilemap()




    def newGame2(self):
        #new game starts
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.ghost = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.door = pygame.sprite.LayeredUpdates()
        self.mainDoor = pygame.sprite.LayeredUpdates()
        self.cat = pygame.sprite.LayeredUpdates()
        self.key = pygame.sprite.LayeredUpdates()
        self.cornerBlock = pygame.sprite.LayeredUpdates()
        self.woman = pygame.sprite.LayeredUpdates()
        

        self.createTilemap2()
    

    def events(self):
        #game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == VIDEORESIZE:
                if not self.fullscreen:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == KEYDOWN:
                if event.key == K_f:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
                    else:
                        self.screen = pygame.display.set_mode((self.screen.get_width(), self.screen.get_height()), pygame.RESIZABLE)
                            
    def update(self):
        #game loop updates
        self.all_sprites.update()
        
        self.cut_scene_manager.update()

    def render_fog(self):
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0,0), special_flags= pygame.BLEND_MULT)


        
    
    def draw(self):
        self.screen.fill(black)
        self.all_sprites.draw(self.screen)
        self.clock.tick(fps)
        self.cut_scene_manager.draw()
        #self.render_fog()
        pygame.display.update()
        
                


    def main(self):
        #game loop
        
        
        while self.playing:
            self.events()
            self.update()
            self.draw()
           

            


            pygame.display.update()
        
    def redraw(self):
        self.screen.fill(black)
        self.all_sprites.draw(self.screen)
        self.clock.tick(fps)
        self.cut_scene_manager.draw()
        self.render_fog()

        pygame.display.update()        
            
            
        

    def gameOver(self):
        text = self.font.render('Game Over', True, white)
        text_rect = text.get_rect(center=(win_width/2, win_height/2))

        restart_button = Button(10, win_height - 60, 120, 50, white, black, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running  = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(fps)
            pygame.display.update()
    
    def main2(self):

        pygame.display.update()

        self.newGame2()
        
        while self.playing:
            self.events()
            self.update()
            
            self.redraw()
            
           
            
            
        
        
 
        
    
    def startScreen(self):
        intro = True
        

        #title = self.font.render('ParaNOTnormal Investigating', True, white)
        #title_rect = title.get_rect(x=10,y=10)

        play_button = Button(280, 310, 150, 80, white, dark_blue, 'PLAY', 50)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                
                intro = False
                self.state = 'main'

            self.screen.blit(self.intro_background, (0,0))
            #self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(fps)
            pygame.display.update()
            
    def state_manager(self):
        if self.state == 'intro':
            self.startScreen()
        if self.state == 'main':
            self.main()
        if self.state == 'main2':
            self.main2()
        

g = Game()
g.startScreen()
g.newGame()
while g.running:
    g.state_manager()
    g.gameOver()

pygame.quit()
sys.exit()
