import pygame
from pygame.locals import *
import random

pygame.init()

Clock=pygame.time.Clock()
fps = 60


screen_width=550
screen_height=700

screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('flappy bird')


#col and font
font=pygame.font.SysFont('Bauhaus 93',60)
white=(255,255,255)

#define game variable
ground_scroll = 0
scroll_speed = 4
#flying , set to false while starting of the game
flying=False
#add game over variable
game_over=False

#add pipe gap
pipe_gap=150
#fre
pipe_frequency=1500 #millisecond
last_pipe=pygame.time.get_ticks() - pipe_frequency
score=0
pass_pipe=False



#load image
bg=pygame.image.load(r'C:\Users\acer\Desktop\cp\python\bg.png')
ground_img=pygame.image.load(r'C:\Users\acer\Desktop\cp\python\ground.png')
button_img=pygame.image.load(r'C:\Users\acer\Desktop\cp\python\restart.png')

#display score
def draw_text(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    screen.blit(img,(x,y))


def reset_game():
    #reinitialise the pipes again
    pipe_group.empty()
    #reposition the bird to og position
    flappy.rect.x=100
    flappy.rect.y=int(screen_height/2)
    score=0
    return score
    



class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        #to make animation we make a list of images and swap 
        self.images=[]
        self.index=0
        self.counter=0
        for num in range(1,4):
            img=pygame.image.load(r'C:\Users\acer\Desktop\cp\python\bird{}.png'.format(num))
            self.images.append(img)


        #assign the image to sprite
        self.image=self.images[self.index]
        #make a rectangle around it
        self.rect = self.image.get_rect()
        #position the rec
        self.rect.center = [x,y]
        #define vel
        self.vel=0
        #add a triger so mouse hold doesnt work
        self.clicked=False

    def update(self):
        #GRAVITY
        if flying==True:#inc vel at each itr
            self.vel+=0.5

            #add a upper limit to vel 
            if self.vel>8:
                self.vel=8
            #print(self.vel)
            if self.rect.bottom <768:
                self.rect.y+=int(self.vel)
        
        if game_over==False:
            #JUMP
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                self.clicked=True
                self.vel=-9
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked=False


            #handle the animation
            self.counter +=1
            flap_cooldown=5

            if self.counter>flap_cooldown:
                #reset the counter
                self.counter=0
                self.index+=1
                if self.index >= len(self.images):
                    self.index=0
            self.image = self.images[self.index]

            #rotate th bird while falling
            self.image=pygame.transform.rotate(self.images[self.index],self.vel*-2)
        else:
            self.image=pygame.transform.rotate(self.images[self.index],-90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(r'C:\Users\acer\Desktop\cp\python\pipe.png')
        self.rect=self.image.get_rect()
        #position 1 from top , -1 is from bottom
        if position==1:
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft=[x,y-int(pipe_gap/2)]
        if position==-1:
            self.rect.topleft=[x,y+int(pipe_gap/2)]


    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right<0:
            self.kill()

class Button():
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)

    def draw(self):

        #define the action
        action=False

        #get mouse posn
        pos=pygame.mouse.get_pos()
        #check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1:
                action=True

        #draw the button
        screen.blit(self.image,(self.rect.x,self.rect.y))

        return action



bird_group = pygame.sprite.Group()
pipe_group=pygame.sprite.Group()

flappy = Bird(100,int(screen_height/2))

bird_group.add(flappy)


#create restart button instance
button=Button(screen_width//2 -50, screen_height //2 -100,button_img)


run=True
while run:

    Clock.tick(fps)

    #to load the bg image on screen we use blit
    #draw bg
    screen.blit(bg,(0,0))

    bird_group.draw(screen)

    bird_group.update()

    #similarly add update for pipr
    pipe_group.draw(screen)

    

    #draw and scroll the ground
    screen.blit(ground_img,(ground_scroll,768))

    #check score
    if len(pipe_group)>0:
        if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right<pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe=True
        if pass_pipe==True:
            if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.left:
                score +=1
                pass_pipe=False

    draw_text(str(score),font,white,int(screen_width/2),20)
        
    


    ##look for collison
    if pygame.sprite.groupcollide(bird_group,pipe_group,False,False) or flappy.rect.top<0:
        game_over=True
    #check if bird has hit grounf
    #check if rect as gone beyond ground
    if flappy.rect.bottom >=768:
        game_over=True
        flying=False



    if game_over==False and flying==True:

        #create extra pipes when game is running
        time_now=pygame.time.get_ticks()
        if time_now-last_pipe>pipe_frequency:
                #that means we can add extra pipe
            pipe_height=random.randint(-100,100)
            btm_pipe=Pipe(screen_width,int(screen_height/2)+pipe_height,-1)
            top_pipe=Pipe(screen_width,int(screen_height/2)+pipe_height,1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe=time_now

        #it increases on the left side
        ground_scroll -= scroll_speed 
        if abs(ground_scroll)>35:
            ground_scroll=0

        pipe_group.update() 
    

    #check for gameover and reset
    if game_over==True:
        if button.draw()==True:
            game_over=False
            score=reset_game()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==pygame.MOUSEBUTTONDOWN and flying==False and game_over==False:
            flying=True

    pygame.display.update()

pygame.quit()