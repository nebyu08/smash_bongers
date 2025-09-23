import pygame
import os
import math
import random
from pygame.locals import *


pygame.init()
pygame.mixer.init()

class Canon:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vel=10

    def draw(self,surface,width,height):
        pygame.draw.rect(surface,(255,0,0),(self.x,self.y,width,height))

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,target_x,target_y,speed):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x,y))

        # lets calculate velocity
        dx=target_x-x
        dy=target_y-y
        distance=(dx**2 + dy**2)
        distance=math.sqrt(distance)
        if distance>0:
            self.vel_x=(dx/distance)*speed
            self.vel_y=(dy/distance)*speed
        else:
            self.vel_x=0
            self.vel_y=0
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

        # speed
        self.speed=speed

        self.radius = radius
        self.color = color
        self.y_velocity = speed

    def update(self):
        self.rect.x+=self.speed
        self.rect.y+=self.speed

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

    screen_width=800
    screen_height=600
    screen=pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("moving balls and banons ")

    # setup for canon
    height=20
    width=20
    canon=Canon(screen_width//2 -width//2,screen_height-height-10)

     # setup for ball
    speed=0.5
    all_balls =pygame.sprite.Group(
        Ball(100, 50, 20, (255, 0, 0)),
        Ball(200, 60, 30, (0, 255, 0)),
        Ball(300, 40, 25, (0, 0, 255)),
    )

    clock=pygame.time.Clock()

    # setup groups for bullets
    all_bullets = pygame.sprite.Group()
    all_particles = pygame.sprite.Group()

    # play the audio now
    # pygame.mixer.music.load("components/audio/mixkit-arcade-video-game-machine-alert-2821.wav")
    # pygame.mixer.music.play(-1)

    while True:
        # pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Left click
                if event.button == 1:
                    mouse_x,mouse_y=pygame.mouse.get_pos()
                    bullet = Bullet(canon.x+width//2,canon.y, mouse_x, mouse_y, 10)
                    all_bullets.add(bullet)
        keys= pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and canon.x>0:
            canon.x-=canon.vel
        if keys[pygame.K_RIGHT] and canon.x<500-width:
            canon.x+=canon.vel
        if keys[pygame.K_UP] and canon.y>0:
            canon.y-=canon.vel
        if keys[pygame.K_DOWN] and canon.y<500-height:
            canon.y+=canon.vel

        # lets update the bullets
        all_bullets.update()
        all_balls.update()

        hits=pygame.sprite.groupcollide(all_bullets,all_balls,True,True)
        if hits:
            hit_sound.play()
            for bullet,hit_balls in hits.items():
                for ball in hit_balls:
                    for _ in range(15):
                        all_particles.add(Particle(ball.rect.centerx,ball.rect.centery,ball.color))
        all_particles.update()
            # print("hit!!!")

        # lets draw
        screen.fill((0,0,0))
        canon.draw(screen,width,height)
        all_bullets.draw(screen)
        all_balls.draw(screen)
        all_particles.draw(screen)
        pygame.display.flip()
        clock.tick(35)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
