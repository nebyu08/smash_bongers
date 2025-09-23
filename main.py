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

def main():
    win=pygame.display.set_mode((500,500))
    pygame.display.set_caption("moving canon ball")
    canon=Canon(200,200)

    heigh=20
    width=20

    while True:
        pygame.time.delay(10)
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
        if keys[pygame.K_DOWN] and canon.y<500-heigh:
            canon.y+=canon.vel
        win.fill((0,0,0))
        pygame.draw.rect(win,(255,0,0),(canon.x,canon.y,width,heigh))
        pygame.display.update()
        pygame.time.delay(10)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
