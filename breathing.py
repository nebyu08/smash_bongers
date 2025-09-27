import pygame

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Up and Down Motion")

# Object properties
object_y = screen_height // 2
object_speed = 2
object_direction = 1  # 1 for down, -1 for up
object_min_y = screen_height // 2 - 2
object_max_y = screen_height // 2 + 2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update object position
    object_y += object_speed * object_direction

    # Reverse direction if limits are reached
    if object_y <= object_min_y or object_y >= object_max_y:
        object_direction *= -1

    # Drawing
    screen.fill((0, 0, 0))  # Black background
    pygame.draw.circle(screen, (255, 255, 0), (screen_width // 2, int(object_y)), 20)  # Yellow circle

    pygame.display.flip()

pygame.quit()
