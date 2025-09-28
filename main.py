import pygame
import os
import math
import random
import time
from pygame.locals import *




pygame.init()
pygame.mixer.init()
pygame.font.init()

font=pygame.font.SysFont("Arial",30)

class Canon(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,color=(255,0,0)):
        self.x = x
        self.y = y
        self.vel=10
        self.color=color
        self.height=height
        self.width=width

        # setting it as image loaded
        original_img=pygame.image.load('components/images/main_space_craft.png').convert_alpha()
        self.image=pygame.transform.scale(original_img,(width,height))
        self.rect=self.image.get_rect(center=(x,y))

        #life specs
        self.base_y=y
        self.amplitude=1
        self.frequency=10
        self.time_offset=random.uniform(0,2*math.pi)

    def move(self,keys,screen_width,screen_height):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.vel
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width-self.width:
            self.rect.x += self.vel
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.vel
        if keys[pygame.K_DOWN] and self.rect.bottom < screen_height-self.height:
            self.rect.y += self.vel

    def update(self,offset_x=0,offset_y=0):
        self.rect.x+=offset_x
        self.rect.y+=offset_y

    def life_move(self):
        t=time.time()
        offset=self.amplitude*math.sin(self.frequency*t+self.time_offset)
        self.rect.y=self.base_y+offset

    def draw(self,surface):
        surface.blit(self.image,self.rect)
        # pygame.draw.rect(surface,self.color,(self.x+offset_x,self.y+offset_y,width,height))

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,target_x,target_y,speed=10):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x,y))

        # we only shoot straight
        self.vel_x=0
        self.vel_y=-speed
        # lets calculate velocity
        # dx=target_x-x
        # dy=target_y-y
        # distance=(dx**2 + dy**2)
        # distance=math.sqrt(distance)
        # if distance>0:
        #     self.vel_x=(dx/distance)*speed
        #     self.vel_y=(dy/distance)*speed
        # else:
        #     self.vel_x=0
        #     self.vel_y=0
    def update(self):
        self.rect.x+=self.vel_x
        self.rect.y+=self.vel_y

class Ball(pygame.sprite.Sprite):
    def __init__(self,x,y,radius,color,speed=0):
        super().__init__()

        # create the surface
        self.image = pygame.Surface((radius*2, radius*2),pygame.SRCALPHA)
        pygame.draw.circle(self.image,color,(radius,radius),radius)
        self.rect = self.image.get_rect(center=(x,y))
        self.rect.x=x
        self.rect.y=y

        self.hit_floor=False

        self.radius = radius
        self.color = color
        self.y_velocity = speed
        self.gravity=0.1

        # hit count
        self.hit_count=0

    def update(self):
        # self.rect.x+=self.y_velocity
        self.y_velocity+=0.5
        self.rect.y+=int(self.y_velocity)
        if self.rect.bottom>600:
            self.rect.bottom=600
            self.y_velocity=0
            if not self.hit_floor:
                self.hit_floor=True
            # self.kill()
            # self.hit_floor=True

class Particle(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        super().__init__()
        self.radius=3
        self.image = pygame.Surface((self.radius*2, self.radius*2),pygame.SRCALPHA)
        pygame.draw.circle(self.image,color,(self.radius,self.radius),self.radius)
        self.rect = self.image.get_rect(center=(x,y))
        self.rect.x=x
        self.rect.y=y
        self.vel=[random.uniform(-3,3),random.uniform(-3,3)]
        self.lifetime=30
    def update(self):
        self.rect.x+=self.vel[0]
        self.rect.y+=self.vel[1]
        self.lifetime-=1
        if self.lifetime<=0:
            self.kill()

def main():
    # sounds
    hit_sound = pygame.mixer.Sound('components/audio/mixkit-winning-a-coin-video-game-2069.wav')

    # score
    score=0

    screen_width=800
    screen_height=600
    screen=pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("kill balls!!!")

    # hello to the use
    main_menu(screen,screen_width,screen_height)


    # background image
    try:
        background_image = pygame.image.load('components/images/background.png').convert()
        background_image= pygame.transform.scale(background_image,(screen_width,screen_height))
    except FileNotFoundError:
        print("Background image not found")
        pygame.quit()
        # pygame.quit()
        # sys.exit()

    # setup for canon
    height=30
    width=30
    color=(255,0,0)
    canon=Canon(screen_width//2 -width//2,screen_height-height-10,width,height)

    # speed=0.5
    spawn_interval=5000
    all_balls=pygame.sprite.Group()

    clock=pygame.time.Clock()

    # setup groups for bullets
    all_bullets = pygame.sprite.Group()
    all_particles = pygame.sprite.Group()

    last_time_spawn=pygame.time.get_ticks()


    # scren distortion
    screen_shake_duration=0
    screen_shake_intensity=5
    Border_color_danger=(255,0,0)
    border_thickness=5
    flash_interval=250
    flash_on=False
    last_time_set=pygame.time.get_ticks()

    while True:
        # pygame.time.delay(10)
        currnt_time=pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # screen.blit(background_image,(0,0))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :  # Left click
                mouse_x,mouse_y=pygame.mouse.get_pos()
                    # bullet = Bullet(canon.x+width//2,canon.y, mouse_x, mouse_y, 10)
                bullet=Bullet(canon.rect.centerx,canon.rect.centery,mouse_x,mouse_y,10)
                all_bullets.add(bullet)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # if event.key == pygame.K_SPACE:
                mouse_x,mouse_y=pygame.mouse.get_pos()
                bullet=Bullet(canon.rect.centerx,canon.rect.centery,mouse_x,mouse_y,10)
                all_bullets.add(bullet)
        # lets give life to canon
        canon.life_move()
        # generate balls
        if currnt_time - last_time_spawn>spawn_interval:
            last_time_spawn=currnt_time
            new_balls=random.randint(1,5)
            for _ in range(new_balls):
                x = random.randint(20, 780)
                new_ball=Ball(x, 0, 20, (0, 0, 255), speed=0)
                # new_ball=Ball(random.randint(0,500),random.randint(0,500),random.randint(5,10),random.randint(5,10))
                all_balls.add(new_ball)

        keys= pygame.key.get_pressed()
        canon.move(keys,screen_width,screen_height)


        hits=pygame.sprite.groupcollide(all_bullets,all_balls,True,True)
        if hits:
             hit_sound.play()
             score+=1
             for bullet,hit_balls in hits.items():
                 for ball in hit_balls:
                     for _ in range(15):
                         all_particles.add(Particle(ball.rect.centerx,ball.rect.centery,ball.color))
        all_particles.update()

        # lets update the bullets
        all_bullets.update()
        all_balls.update()

        balls_to_remove=[]
        for ball in all_balls:
            if ball.hit_floor:
                score-=1
                balls_to_remove.append(ball)
                screen_shake_duration=10
        for ball in balls_to_remove:
            ball.kill()

        if score<0:
            current_time=pygame.time.get_ticks()
            if current_time-last_time_set>flash_interval:
                flash_on=not flash_on
                last_time_set=current_time
            # screen_shake_duration=10
        else:
            flash_on=False

        shake_x,shake_y=0,0
        if screen_shake_duration>0:
            shake_x=random.randint(-screen_shake_intensity,screen_shake_intensity)
            shake_y=random.randint(-screen_shake_intensity,screen_shake_intensity)
            screen_shake_duration-=1

        if background_image:
            screen.blit(background_image,(0,0))
        else:
            screen.fill((0,0,0))

        # screen.fill((0,0,0))
        show_score(10,10,score,screen)
        canon.update(shake_x,shake_y)
        canon.draw(screen)
        # canon.draw(screen,width,height,shake_x,shake_y)
        all_bullets.draw(screen)
        all_balls.draw(screen)
        all_particles.draw(screen)


        if flash_on and score<0 :
            pygame.draw.rect(screen, Border_color_danger, (0, 0, screen_width, border_thickness))
            pygame.draw.rect(screen, Border_color_danger, (0, screen_height - border_thickness, screen_width, border_thickness))
            pygame.draw.rect(screen, Border_color_danger, (0, border_thickness, border_thickness, screen_height - 2 * border_thickness))
            pygame.draw.rect(screen, Border_color_danger, (screen_width - border_thickness, border_thickness, border_thickness, screen_height - 2 * border_thickness))


        pygame.display.flip()
        clock.tick(35)

    pygame.quit()
    quit()

def show_score(x,y,score,screen):
    score_text=font.render("Score: "+str(score),True,(28,12,247))
    screen.blit(score_text,(x,y))

def draw_gradient_background(screen,screen_width,screen_height):
    for y in range(screen_height):
        color=(
            int(50+(y/screen_height)*150),
            int(20+(y/screen_height)*50),
            int(100+(y/screen_height)*150)
        )
        pygame.draw.line(screen,color,(0,y),(screen_width,y))

def render_glow_text(text,font,color,glow_color):
    base=font.render(text,True,color)
    glow=font.render(text,True,glow_color)
    return base,glow


def main_menu(screen,screen_width,screen_height):
    menu_running=True
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x,mouse_y=pygame.mouse.get_pos()
                start_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
                if start_button_rect.collidepoint(mouse_x,mouse_y):
                    menu_running=False


        # screen.fill((0,0,0))
        draw_gradient_background(screen,screen_width,screen_height)
        hello_text=font.render("Welcome to my game",True,(255,255,255))
        screen.blit(hello_text,(screen_width // 2 - hello_text.get_width() // 2, screen_height // 4))
        # hello_text, hello_glow = render_glow_text("Welcome to my game", font, (255,255,255), (0,255,255))
        # screen.blit(hello_glow, (screen_width // 2 - hello_glow.get_width() // 2+2, screen_height // 4+2))
        # screen.blit(hello_text, (screen_width // 2 - hello_text.get_width() // 2, screen_height // 4))

        start_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
        pygame.draw.rect(screen, (0,0,255), start_button_rect)
        start_text = font.render("Start Game", True, (255,255,255))
        screen.blit(start_text, (start_button_rect.x + (start_button_rect.width - start_text.get_width()) // 2,
                                    start_button_rect.y + (start_button_rect.height - start_text.get_height()) // 2))

        pygame.display.flip() # Update the display

if __name__ == "__main__":
    main()
