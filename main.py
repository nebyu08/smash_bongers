import pygame
import os
import math
import random
from pygame.locals import *


pygame.init()
pygame.mixer.init()
pygame.font.init()

font=pygame.font.SysFont("Arial",30)

class Canon:
    def __init__(self,x,y,color=(255,0,0)):
        self.x = x
        self.y = y
        self.vel=10
        self.color=color

    def draw(self,surface,width,height,offset_x=0,offset_y=0):
        pygame.draw.rect(surface,self.color,(self.x+offset_x,self.y+offset_y,width,height))

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

    # background image
    try:
        background_image = pygame.image.load('components/images/background.png').convert()
        background_image= pygame.transform.scale(background_image,(screen_width,screen_height))
    except FileNotFoundError:
        print("Background image not found")
        pygame.quit()
        # sys.exit()

    # setup for canon
    height=20
    width=20
    color=(255,0,0)
    canon=Canon(screen_width//2 -width//2,screen_height-height-10)

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
            if event.type == pygame.MOUSEBUTTONDOWN:  # Left click
                if event.button == 1:
                    mouse_x,mouse_y=pygame.mouse.get_pos()
                    bullet = Bullet(canon.x+width//2,canon.y, mouse_x, mouse_y, 10)
                    all_bullets.add(bullet)
        # generate balls
        if currnt_time - last_time_spawn>spawn_interval:
            last_time_spawn=currnt_time
            new_balls=random.randint(1,20)
            for _ in range(new_balls):
                x = random.randint(20, 780)
                new_ball=Ball(x, 0, 20, (0, 0, 255), speed=0)
                # new_ball=Ball(random.randint(0,500),random.randint(0,500),random.randint(5,10),random.randint(5,10))
                all_balls.add(new_ball)

        keys= pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and canon.x>0:
            canon.x-=canon.vel
        if keys[pygame.K_RIGHT] and canon.x<screen_width-width:
            canon.x+=canon.vel
        if keys[pygame.K_UP] and canon.y>0:
            canon.y-=canon.vel
        if keys[pygame.K_DOWN] and canon.y<screen_height-height:
            canon.y+=canon.vel

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
        canon.draw(screen,width,height,shake_x,shake_y)
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

if __name__ == "__main__":
    main()
