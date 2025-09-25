import pygame

pygame.init()
screen_width=800
screen_height=600

screen=pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Spider Game")


object_color=(30,0,0)
object_width=50
object_height=50
object_x=0
object_y=screen_height//2 - object_height//2
object_rec=pygame.Rect(object_x, object_y, object_width, object_height)
object_speed=5

clock=pygame.time.Clock()

running=True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    object_rec.x += object_speed

    if object_rec.right>screen_width or object_rec.left<0:
        object_speed *= -1


    screen.fill((0,0,0))
    pygame.draw.rect(screen, object_color, object_rec)
    pygame.display.flip

    clock.tick(60)
