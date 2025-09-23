import pygame
import os
import math
from pygame.locals import *

pygame.init()

class Canon:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vel=10
        # self.width=width
        # self.height=height
    def draw(self,surface,width,height):
        # pygame.draw.rect(surface,(255,0,0),(self.x,self.y,self.width,self.height))
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

class Ball:
    def __init__(self,x,y,radius,color,y_velocity=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.y_velocity = y_velocity



    def draw(self,surface):
        pygame.draw.circle(surface,self.color,(int(self.x),int(self.y)),self.radius)



def main():
    screen_width=800
    screen_height=600
    screen=pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("moving balls and banons ")

    # setup for canon
    canon=Canon(200,200)
    height=20
    width=20

     # setup for ball
    gravity=0.5
    balls=[Ball(100,50,20,(255,0,0)), Ball(200,200,30,(0,255,0)), Ball(300,300,30,(0,0,255)), Ball(400,400,30,(255,255,0)), Ball(500,500,30,(255,0,255)), Ball(600,600,30,(255,255,255)), Ball(700,700,30,(0,255,255))]
    # balls=[Ball(100,50,20,(255,0,0)),Ball(100,60,20,(255,0,0)),Ball(100,50,20,(255,0,0)),Ball(100,50,20,(255,0,0)),Ball(100,50,20,(255,0,0))]
    clock=pygame.time.Clock()

    while True:
        # pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys= pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and canon.x>0:
            canon.x-=canon.vel
        if keys[pygame.K_RIGHT] and canon.x<500-width:
            canon.x+=canon.vel
        if keys[pygame.K_UP] and canon.y>0:
            canon.y-=canon.vel
        if keys[pygame.K_DOWN] and canon.y<500-height:
            canon.y+=canon.vel

        for ball in balls:
            ball.y_velocity +=gravity
            ball.y+=ball.y_velocity

            # lets make it bounce back the wall eski
            if ball.y+ball.radius>screen_height:
                ball.y=screen_height-ball.radius
                ball.y_velocity *=-0.8
        # lets draw
        screen.fill((0,0,0))
        # pygame.draw.rect(screen,(255,140,10),(canon.x,canon.y,width,height))
        canon.draw(screen,width,height)
        for ball in balls:
            ball.draw(screen)
        pygame.display.flip()
        # pygame.time.delay(40)
        clock.tick(35)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()


def load_image(img):
    fullname=os.path.join('data', img)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    return image, image.get_rect()
