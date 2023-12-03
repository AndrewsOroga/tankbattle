from os import kill
import pygame
import sys
import random
import time


pygame.init()
FPS = 60
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


WIDTH, HEIGHT = 1200, 800


p_hp_position = 65
screen = pygame.display.set_mode((WIDTH, HEIGHT))

typ_list = ["barrel","wall"]

font = pygame.font.Font(None, 36)


med_cd = time.time()

rocket_img = pygame.image.load("img/Players/m.png")
bullet_img = pygame.image.load("img/Players/blt.png")
player_img = pygame.image.load("img/Players/tank3.png")
enemy_img = pygame.image.load("img/Players/tank4.png")
bg = pygame.image.load("img/backgrounds/g.jpeg")
bg =  pygame.transform.scale(bg,(WIDTH,HEIGHT))

bg2 = pygame.image.load("img/backgrounds/Phon.jpg")
wall_img = pygame.image.load("img/Textures/StonesBrick Textures/Brickwall4_Texture.png")
barrel_img = pygame.image.load("img/Players/bar.png")
med = pygame.image.load("img/Players/med.png")
objects = [wall_img,barrel_img]

bg2 =  pygame.transform.scale(bg2,(WIDTH,HEIGHT))
bullets = pygame.sprite.Group()
rockets = pygame.sprite.Group()
walls = pygame.sprite.Group()
medkits = pygame.sprite.Group()
players = pygame.sprite.Group()

BLUE = (0,0,255)
GEAN = (0,255,0)
LIME = (205,255,23)
YELLOW = (255,230,0)
ORANGE = (255,153,0)
ORAGE_RED =(255,100,0)
RED = (255,0,0)
HP_color = GEAN
w = {}


def draw_text(surface,x,y,text,colour):
    font = pygame.font.Font("img/Fonts/arial.ttf",25)
    text_surface = font.render(text,True,colour)
    text_rect = text_surface.get_rect()
    text_rect.x = x
    text_rect.y = y
    surface.blit(text_surface,text_rect)
    

def draw_hp(surface,x,y,value,colour):
    strip_lenght = 200
    strip_height = 19
    value_length = (value/player_tank.max_hp) * strip_lenght
    back_rect = pygame.Rect(x,y,strip_lenght,strip_height)
    front_rect = pygame.Rect(x,y,value_length,strip_height)
    pygame.draw.rect(surface,RED,back_rect)
    pygame.draw.rect(surface,colour,front_rect)

class barrel(pygame.sprite.Sprite):
    def __init__(self,img):
         super(barrel, self).__init__()
       
         self.image = pygame.transform.scale(img,(55,55))
         self.rect = self.image.get_rect()
         self.rect.x = random.randint(225,WIDTH-225)
         self.rect.y  = random.randint(75,HEIGHT-75)
         self.hp = random.randint(60,90)
       
  
class medkit(pygame.sprite.Sprite):
    def __init__(self,img):
         super(medkit, self).__init__()
        
         self.image = pygame.transform.scale(img,(42,42))
         self.rect = self.image.get_rect()
         self.rect.x = random.randint(225,WIDTH-225)
         self.rect.y  = random.randint(75,HEIGHT-75)      
         self.healup = random.randint(5,15)
class wall(pygame.sprite.Sprite):
    def __init__(self,img):
         super(wall, self).__init__()
        
         self.image = pygame.transform.scale(img,(random.randint(35,40),random.randint(70,150)))
         self.rect = self.image.get_rect()
         self.rect.x = random.randint(225,WIDTH-225)
         self.rect.y  = random.randint(75,HEIGHT-75)
         self.hp = random.randint(70,120)

        
class bulletc(pygame.sprite.Sprite):
    def __init__(self,img,x,y,bx):
        super(bulletc, self).__init__()
        self.image = pygame.transform.scale(img,(20,10))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_x =bx
        self.speed_y = 0
    def update(self):
        self.rect.y -= self.speed_y
        self.rect.centerx -= self.speed_x
        if self.rect.bottom < 0:
            self.kill()
            
class rocket(pygame.sprite.Sprite):
    def __init__(self,img,x,y,bx):
        super(rocket, self).__init__()
        self.image = pygame.transform.scale(img,(40,25))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_x =bx
        self.speed_y = 0
    def update(self):
        self.rect.y -= self.speed_y
        self.rect.centerx -= self.speed_x
        if self.rect.bottom < 0:
            self.kill()

        
class Tank(pygame.sprite.Sprite):
    def __init__(self,x,player_img):
        super(Tank, self).__init__()
        self.image = pygame.transform.scale(player_img,(180,60))
       
        self.Right = pygame.transform.flip(self.image,True,False)
        self.Left = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx = 240
        self.rect.bottom = 400
        self.speed = 2
        self.hp = 140
        self.max_hp = 160
        self.r_dmg = 40
        self.b_dmg = 6  
        self.rect.x = x
        self.last_shoot = time.time()
        self.last_shoot2 = time.time()
        self.bullets = 200
        self.rockets = 30
    def update(self):
        old_x = self.rect.x 
        old_y = self.rect.y  
        
        hits = pygame.sprite.spritecollide(self,walls,False)
        if hits:
         self.rect.x = old_x
         self.rect.y = old_y   
         



        keys = pygame.key.get_pressed()
        if keys[pygame.K_n]:
           self.image = self.Right 
           
        if keys[pygame.K_b]:
           self.image = self.Left

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            p_hp_position = 65
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            p_hp_position = 0
            
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            
        hits2 = pygame.sprite.spritecollide(self,walls,False)    
        if hits2:
            
             self.rect.x = old_x
             self.rect.y = old_y 

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        elif self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0

    def shoot_2(self,bullet):
           
            
         if self.rockets > 0:
            if self.image == self.Right:
              if time.time() - self.last_shoot >= 3:
               piy = pygame.mixer.Sound("img/Sounds/Shot1.mp3")
               piy.set_volume(0.18)
               piy.play()
               self.last_shoot = time.time()
               self.rockets -= 1
               b = rocket(img=bullet,
                       x = self.rect.centerx+115,
                       y = self.rect.top+30,
                       bx = random.randint(-14,-10))
               all_sprites.add(b)
               rockets.add(b) 
            if self.image == self.Left:
              if time.time() - self.last_shoot >= 3:
               bullet = pygame.transform.flip(bullet,True,False)
               piy = pygame.mixer.Sound("img/Sounds/Shot1.mp3")
               piy.set_volume(0.18)
               piy.play()
               self.last_shoot = time.time()
               self.rockets -= 1
               b = rocket(img=bullet,
                       x = self.rect.centerx-115,
                       y = self.rect.top+30,
                       bx = random.randint(11,15))
             
               all_sprites.add(b)
               rockets.add(b)
               
    def shoot(self,bullet):
           
            
          if self.bullets > 0:
            if self.image == self.Right:
              if time.time() - self.last_shoot2 >= 0.3:
               piy = pygame.mixer.Sound("img/Sounds/Shot1.mp3")
               piy.set_volume(0.1)
               piy.play()
               self.last_shoot2 = time.time()
               b = bulletc(img=bullet_img,
                       x = self.rect.centerx+105,
                       y = self.rect.top+23,
                       bx = random.randint(-12,-7))
               self.bullets -= 1
               all_sprites.add(b)
               bullets.add(b) 
            if self.image == self.Left:
              if time.time() - self.last_shoot2 >= 0.3:
               bulleti = pygame.transform.flip(bullet,True,False)
               piy = pygame.mixer.Sound("img/Sounds/Shot1.mp3")
               piy.set_volume(0.18)
               piy.play()
               self.last_shoot2 = time.time()
               b = bulletc(img=bullet,
                       x = self.rect.centerx-105,
                       y = self.rect.top+23,
                       bx = random.randint(7,12))
               self.bullets -= 1
             
               all_sprites.add(b)
               bullets.add(b)
    
      
        
class Tank2(pygame.sprite.Sprite):
    def __init__(self,x,player_img):
        super(Tank2, self).__init__()
        self.image = pygame.transform.scale(player_img,(180,65))
 
        self.Right = pygame.transform.flip(self.image,True,False)
        self.Left = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx = 240
        self.rect.bottom = 400
        self.speed = 2
        self.hp = 140
        self.max_hp = 160
        self.r_dmg = 40
        self.b_dmg = 6  
        self.rect.x = x
        self.last_shoot = time.time()
        self.last_shoot2 = time.time()
        self.bullets = 200
        self.rockets = 30
    def update(self):
        old_x = self.rect.x 
        old_y = self.rect.y  
        
        hits = pygame.sprite.spritecollide(self,walls,False)
        if hits:
         self.rect.x = old_x
         self.rect.y = old_y   
         



        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
           self.image = self.Right 
           
        if keys[pygame.K_q]:
           self.image = self.Left

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            p_hp_position = 65
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            p_hp_position = 0
            
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
            
        hits2 = pygame.sprite.spritecollide(self,walls,False)    
        if hits2:
            
             self.rect.x = old_x
             self.rect.y = old_y 

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        elif self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0

    def shoot_2(self,bullet):
           
            
         if self.rockets > 0:
            if self.image == self.Right:
              if time.time() - self.last_shoot >= 3:
               piy = pygame.mixer.Sound("img/Sounds/Shot1.mp3")
               piy.set_volume(0.18)
               piy.play()
               self.last_shoot = time.time()
               self.rockets -= 1
               b = rocket(img=bullet,
                       x = self.rect.centerx+110,
                       y = self.rect.top+30,
                       bx = random.randint(-14,-10))
               all_sprites.add(b)
               rockets.add(b) 
            if self.image == self.Left:
              if time.time() - self.last_shoot >= 3:
               bullet = pygame.transform.flip(bullet,True,False)
               piy = pygame.mixer.Sound("img/Sounds/Shot1.mp3")
               piy.set_volume(0.18)
               piy.play()
               self.last_shoot = time.time()
               self.rockets -= 1
               b = rocket(img=bullet,
                       x = self.rect.centerx-110,
                       y = self.rect.top+30,
                       bx = random.randint(11,15))
             
               all_sprites.add(b)
               rockets.add(b)
               
    def shoot(self,bullet):
           
            
          if self.bullets > 0:
            if self.image == self.Right:
              if time.time() - self.last_shoot2 >= 0.3:
               piy = pygame.mixer.Sound("img/Sounds/Shot1.mp3")
               piy.set_volume(0.1)
               piy.play()
               self.last_shoot2 = time.time()
               b = bulletc(img=bullet_img,
                       x = self.rect.centerx+100,
                       y = self.rect.top+26,
                       bx = random.randint(-12,-7))
               self.bullets -= 1
               all_sprites.add(b)
               bullets.add(b) 
            if self.image == self.Left:
              if time.time() - self.last_shoot2 >= 0.3:
               bulleti = pygame.transform.flip(bullet,True,False)
               piy = pygame.mixer.Sound("img/Sounds/Shot1.mp3")
               piy.set_volume(0.18)
               piy.play()
               self.last_shoot2 = time.time()
               b = bulletc(img=bullet,
                       x = self.rect.centerx-100,
                       y = self.rect.top+26,
                       bx = random.randint(7,12))
               self.bullets -= 1
             
               all_sprites.add(b)
               bullets.add(b)

      
        


all_sprites = pygame.sprite.Group()


player_tank = Tank2(0, player_img)
enemy_tank = Tank(1200, enemy_img)



play_button = font.render("Play", True, WHITE)
exit_button = font.render("Exit", True, WHITE)
play_rect = play_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))
exit_rect = exit_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

for i in range(10):

    m1 = wall(wall_img)
    m2 = barrel(barrel_img)
    if random.choice(typ_list) == "wall":
    
     all_sprites.add(m1)
     walls.add(m1)
     
    elif random.choice(typ_list) == "barrel": 
     
     all_sprites.add(m2)
     walls.add(m2)



playing = False
exiting = False

while True:
    screen.blit(bg2, [0, 0])
  
    all_sprites.update()
    

   


    for event in pygame.event.get():
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:               
                  player_tank.shoot_2(rocket_img)
        if keys[pygame.K_f]:               
                  player_tank.shoot(bullet_img)         
        if keys[pygame.K_k]:               
                  enemy_tank.shoot_2(rocket_img)
        if keys[pygame.K_m]:               
                  enemy_tank.shoot(bullet_img)   
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if play_rect.collidepoint(mouse_pos):
                playing = True
            if exit_rect.collidepoint(mouse_pos):
                exiting = True
                

    for i in medkits:    
     
      hits3 = pygame.sprite.spritecollide(enemy_tank,medkits,False)
      if hits3: 
        boom = pygame.mixer.Sound("img/Sounds/pelmeni.mp3")
        boom.set_volume(0.15)
        boom.play()
       
        for wa in hits3:
                  
         if enemy_tank.hp != enemy_tank.max_hp:
            enemy_tank.hp +=  wa.healup
            if enemy_tank.hp > enemy_tank.max_hp:
                enemy_tank.hp= enemy_tank.max_hp

            i.kill()
            wa.kill()
      hits2 = pygame.sprite.spritecollide(player_tank,medkits,False)
      if hits2: 
        boom = pygame.mixer.Sound("img/Sounds/pelmeni.mp3")
        boom.set_volume(0.15)
        boom.play()
       
        for wa in hits2:
                  
         if player_tank.hp != player_tank.max_hp:
            player_tank.hp +=  wa.healup
            if player_tank.hp > player_tank.max_hp:
                player_tank.hp= player_tank.max_hp

            i.kill()
            wa.kill()
             
              
 
    for bullet in rockets:    
     hits = pygame.sprite.spritecollide(bullet,players,False)
     if hits: 
        boom = pygame.mixer.Sound("img/Sounds/booom.mp3")
        boom.set_volume(0.2)
        boom.play()
        t = time.time()
        for wa in hits:
            
           
            
            wa.hp -= player_tank.r_dmg
           
            bullet.kill()
            if wa.hp <= 0:
             
             bullet.kill()
             wa.kill()
            
    for bullet in rockets:    
     hits = pygame.sprite.spritecollide(bullet,walls,False)
     if hits: 
        boom = pygame.mixer.Sound("img/Sounds/booom.mp3")
        boom.set_volume(0.2)
        boom.play()
        t = time.time()
        for wa in hits:
           
            
            wa.hp -= player_tank.r_dmg
           
            bullet.kill()
            if wa.hp <= 0:
             rtyp = random.choice(typ_list)
             bullet.kill()
             wa.kill()
             if rtyp == "wall":
              

              m = wall(wall_img)
              all_sprites.add(m)
              walls.add(m)
             elif rtyp == "barrel": 
              m = barrel(barrel_img)
              all_sprites.add(m)
              walls.add(m) 
    for bullet in bullets:    
     hits = pygame.sprite.spritecollide(bullet,players,False)
     if hits: 
        boom = pygame.mixer.Sound("img/Sounds/booom.mp3")
        boom.set_volume(0.09)
        boom.play()
        t = time.time()
        for wa in hits:
           
           
            
            wa.hp -= player_tank.b_dmg
            
            bullet.kill()
            if wa.hp <= 0:
                bullet.kill()
                wa.kill()
            
             

    for bullet in bullets:    
     hits = pygame.sprite.spritecollide(bullet,walls,False)
     if hits: 
        boom = pygame.mixer.Sound("img/Sounds/booom.mp3")
        boom.set_volume(0.09)
        boom.play()
        t = time.time()
        for wa in hits:
          
           
           
            
            wa.hp -= player_tank.b_dmg
            
            bullet.kill()
            if wa.hp <= 0:
             rtyp = random.choice(typ_list)
             bullet.kill()
             wa.kill()
             if rtyp == "wall":
              

              m = wall(wall_img)
              all_sprites.add(m)
              walls.add(m)
             elif rtyp == "barrel": 
              m = barrel(barrel_img)
              all_sprites.add(m)
              walls.add(m)
           


    if exiting:
        pygame.quit()
        sys.exit()
    if playing:
        

        
       
        if players.has(player_tank) == False or players.has(enemy_tank) == False  :
         player_tank = Tank2(0,player_img)
         enemy_tank = Tank(1200,enemy_img)
         
         
         all_sprites.add(player_tank)
         all_sprites.add(enemy_tank)
         

         players.add(player_tank)
         players.add(enemy_tank)

        screen.blit(bg, [0, 0])
       
      
        if enemy_tank.hp == enemy_tank.max_hp:
            HP_color = GEAN
        if enemy_tank.hp <= enemy_tank.max_hp / 1.05263157894:
            HP_color = GEAN
        if enemy_tank.hp <= enemy_tank.max_hp / 1.25:
            HP_color = LIME
        if enemy_tank.hp <= enemy_tank.max_hp / 1.6666:
           HP_color = YELLOW
        if enemy_tank.hp <= enemy_tank.max_hp / 2.5:
            HP_color = ORANGE
        if enemy_tank.hp <= enemy_tank.max_hp / 4:
            HP_color = RED
            

        if player_tank.hp == player_tank.max_hp:
            HP_BAR_COLOR = GEAN
        if player_tank.hp <= player_tank.max_hp / 1.05263157894:
            HP_BAR_COLOR = GEAN
        if player_tank.hp <= player_tank.max_hp / 1.25:
            HP_BAR_COLOR = LIME
        if player_tank.hp <= player_tank.max_hp / 1.6666:
           HP_BAR_COLOR = YELLOW
        if player_tank.hp <= player_tank.max_hp / 2.5:
            HP_BAR_COLOR = ORANGE
        if player_tank.hp <= player_tank.max_hp / 4:
            HP_BAR_COLOR = RED
            

        all_sprites.draw(screen)
         
        draw_hp(screen,0+15 , 0  + 60 , player_tank.hp,HP_BAR_COLOR)
        draw_text(screen,15,20,str("TANK 1"),BLUE)
        draw_text(screen,65,55,str(player_tank.hp)+"/"+str(player_tank.max_hp),WHITE)
        draw_text(screen,115,20,str(player_tank.bullets)+ " Bullets",YELLOW)
        draw_text(screen,250,20,str(player_tank.rockets)+ " Rockets",RED)
        
        draw_hp(screen,980 ,  60 , enemy_tank.hp,HP_color)
        draw_text(screen,1105,20,str("TANK 1"),RED)
        draw_text(screen,1035,55,str(enemy_tank.hp)+"/"+str(enemy_tank.max_hp),WHITE)
        draw_text(screen,965,20,str(enemy_tank.bullets)+ " Bullets",YELLOW)
        draw_text(screen,830,20,str(enemy_tank.rockets)+ " Rockets",RED)
        
        if player_tank.hp < player_tank.max_hp / 2 and enemy_tank.hp < enemy_tank.max_hp / 2:
           
            if time.time() - med_cd >= 2:
             er = medkit(med)
             all_sprites.add(er)
             medkits.add(er)
             med_cd = time.time()
        if player_tank.hp <= 0:
            result_text = font.render("You Lose!", True, RED)
            result_rect = result_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(result_text, result_rect)
            pygame.display.flip()
            pygame.time.wait(2000)
            playing = False
            players.remove(player_tank)
            players.remove(enemy_tank)
            player_tank.kill()
            enemy_tank.kill()
        if enemy_tank.hp <= 0 :
            result_text = font.render("You Win!", True, BLUE)
            result_rect = result_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(result_text, result_rect)
            pygame.display.flip()
            pygame.time.wait(2000)
            playing = False
            player_tank.kill()
            enemy_tank.kill()
            players.remove(player_tank)
            players.remove(enemy_tank)
    else:
        screen.blit(play_button, play_rect)
        screen.blit(exit_button, exit_rect)
    
    clock.tick(FPS)
    pygame.display.update()
    