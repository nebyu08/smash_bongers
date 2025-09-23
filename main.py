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
    screen_width=500
    screen_height=500
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
    # clock=pygame.time.Clock()

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
        # screen.fill((0,0,0))
        # pygame.draw.rect(screen,(255,0,0),(canon.x,canon.y,width,heigh))
        # pygame.display.update()
        # pygame.time.delay(10)



        for ball in balls:
            ball.y_velocity +=gravity
            ball.y+=ball.y_velocity

            # lets make it bounce back the wall eski
            if ball.y+ball.radius>screen_height:
                ball.y=screen_height-ball.radius
                ball.y_velocity *=-0.8
        # lets draw
        screen.fill((0,0,0))
        pygame.draw.rect(screen,(255,0,0),(canon.x,canon.y,width,height))
        # canon.draw(screen,)
        for ball in balls:
            ball.draw(screen)
        pygame.display.update()
        pygame.time.delay(60)


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
