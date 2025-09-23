import re
import pygame
from pygame.cursors import ball

def main():

    pygame.init()

    width=1000
    height=600
    screen_res=(width,height)

    pygame.display.set_caption("Luffy bouncing ball")
    screen=pygame.display.set_mode(screen_res)

    red=(255,0,0)
    black=(0,0,0)

    speed=[1,1]

    # the ball object
    ball_obj=pygame.draw.circle(
        surface=screen,color=red,center=[100,100],radius=50
    )

    # game Lookup
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        screen.fill(black)
        ball_obj=ball_obj.move(speed)

        if ball_obj.left <=0 or ball_obj.right >= width:
            speed[0] = -speed[0]
        if ball_obj.top <=0 or ball_obj.bottom >= height:
            speed[1] = -speed[1]

        pygame.draw.circle(surface=screen,color=red,center=ball_obj.center,radius=50)

        pygame.display.flip()

if __name__=="__main__":
    main()
