import math
import pygame


pygame.init()


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Super Pong")

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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect(center=(800,600))
        self.vel_x=0
        self.vel_y=0
    def update(self):
        self.rect.x+=self.vel_x
        self.rect.y+=self.vel_y

def main():
    all_sprites = pygame.sprite.Group()
    bullets=pygame.sprite.Group()

    player=Player()
    clock=pygame.time.Clock()
    running=True


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left click
                            mouse_pos = pygame.mouse.get_pos()
                            bullet = Bullet(player.rect.centerx, player.rect.centery, mouse_pos[0], mouse_pos[1], 10)
                            all_sprites.add(bullet)
                            bullets.add(bullet)
        all_sprites.update()

        # lets remove the bullets when they leave the screen
        for bullet in bullets:
            if not screen.get_rect().colliderect(bullet.rect):
                bullet.kill()

        screen.fill((0,0,0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__=="__main__":
    main()
