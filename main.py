import pygame
from pygame.locals import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Super Pong")

    # background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250
    ))

    # lets display some text
    font=pygame.font.Font(None, 36)
    text=font.render("Hello World!", True, (0, 0, 0))
    text_pos=text.get_rect()
    text_pos.centerx=background.get_rect().centerx
    background.blit(text,text_pos)

    screen.blit(background,(0,0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                # sys.exit()
        screen.blit(background,(0,0))
        pygame.display.flip()

if __name__ == "__main__":
    main()
