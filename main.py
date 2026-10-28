'''
Flappy Bird Game 
Python + Pygame
'''
import random
import pygame

# 1. Game Settings

WIDTH = 480
HEIGHT = 640
GROUND_HEIGHT = 80
FPS = 60

SKY_BLUE = (135, 206, 235)
WHITE = (225, 225, 225)
BLACK = (25, 25, 25)
GREEN = (50, 180, 75)
DARK_GREEN = (25,125, 55)
YELLOW = (255, 220, 60)
ORANGE = (245, 145, 35)
BROWN = (180, 130, 75)

BIRD_X = 110
BIRD_RADIUS = 16
GRAVITY = 0.42
FLAP_STRENGTH = -7.5

PIPE_WIDTH = 72
PIPE_GAP = 175
PIPE_SPEED = 3
PIPE_SPWAN_DISTANCE = 245


# 2. Initilising Pygame

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Python Project")

clock = pygame.time.Clock()

font = pygame.font.Font(None, 38)
small_font = pygame.font.Font(None, 25)
large_font = pygame.font.Font(None, 54)


# 3. Draw text

def draw_text(surface, text, font_object, color, center):
    image = font_object.render(text, True, color)
    rectangle = image.get_rect(center=center)
    surface.blit(image, rectangle)


# 4. Create a Pipe bar

def make_pipe(x):
    minimun_gap_center = 150
    maximum_gap_center = HEIGHT - GROUND_HEIGHT - 150

    gap_center = random.randint(
        minimun_gap_center,
        maximum_gap_center
    )

    return {
        "x": x,
        "gap_center": gap_center, 
        "scored": False
    }


# 5. Pipe Rectangles

def get_pipe_rectangles(pipe):
    x = pipe["x"]
    gap_center = pipe["gap_center"]

    gap_top = gap_center - PIPE_GAP // 2
    gap_bottom = gap_center + PIPE_GAP // 2

    top_rect = pygame.Rect(
        x,
        0,
        PIPE_WIDTH,
        gap_top
    )

    bottom_rect = pygame.Rect(
        x,
        gap_bottom,
        PIPE_WIDTH,
        HEIGHT - GROUND_HEIGHT - gap_bottom 
    )
    
    return top_rect, bottom_rect


# 6. Draw the pipe 

def draw_pipe(surface, rectangle):
    pygame.draw.rect(surface, GREEN, rectangle)
    pygame.draw.rect(surface, DARK_GREEN, rectangle, 13)

    lip_height = 18

    if rectangle.top == 0:
        lip = pygame.Rect(
            rectangle.x - 5,
            rectangle.bottom - lip_height,
            PIPE_WIDTH + 10,
            lip_height       
        )
    else:
        lip = pygame.Rect(
            rectangle.x - 5,
            rectangle.top,
            PIPE_WIDTH + 10,
            lip_height
        )

    pygame.draw.rect(surface, GREEN, lip)
    pygame.draw.rect(surface, DARK_GREEN, lip, 3)

    
# 7. Draw Bird 

def draw_bird(surface, x, y):
    center = (int(x), int(y))

    pygame.draw.circle(
        surface,
        YELLOW, 
        center,
        BIRD_RADIUS
    )
    pygame.draw.circle(
        surface,
        BLACK,
        center,
        BIRD_RADIUS,
        2
    )

    # Wing
    pygame.draw.ellipse(
        surface,
        ORANGE,
        pygame.Rect(int(x - 12), int(y + 1), 17, 10)
    )
    
    # Eye
    pygame.draw.circle(
        surface,
        WHITE,
        (int(x + 6), int(y -5)),
        2
    )
    
    # beak
    beak_point = [
        (int(x + 13), int(y)),
        (int(x + 25), int(y + 4)),
        (int(x + 13), int(y + 8))
    ]

    pygame.draw.polygon(
        surface,
        ORANGE,
        beak_point
    )


# 8. Draw background

def draw_background(surface):
    surface.fill(SKY_BLUE)

    # cloud
    pygame.draw.circle(surface, WHITE, (80, 100,), 20)
    pygame.draw.circle(surface, WHITE, (103, 92,), 25)
    pygame.draw.circle(surface, WHITE, (80, 102,), 18)
    
    pygame.draw.circle(surface, WHITE, (315, 115,), 18)
    pygame.draw.circle(surface, WHITE, (337, 145,), 24)
    pygame.draw.circle(surface, WHITE, (360, 156,), 17)

    # Ground 
    ground_y = HEIGHT - GROUND_HEIGHT

    pygame.draw.rect(
        surface, BROWN,
        (0,ground_y, WIDTH, GROUND_HEIGHT)
    )

    pygame.draw.rect(
        surface, GREEN,
        (0, ground_y, WIDTH, 12)
    )


# 9. Reset The Game

def reset_game():
    bird_y = HEIGHT // 2
    bird_velocity = 0

    pipes = [make_pipe(WIDTH + 50)]
    score = 0

    return bird_y, bird_velocity, pipes, score


# 10. Starting values

bird_y,  bird_velocity, pipes, score = reset_game()

game_state = "start"
running = True

# 11. Main game loop

while running:
    clock.tick(FPS)

    # read player and Window event
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False
            
            elif event.key == pygame.K_SPACE:

                if game_state == "start":
                    game_state = "playing"
                    bird_velocity = FLAP_STRENGTH

                elif game_state == "playing":
                    bird_velocity = FLAP_STRENGTH

                elif game_state == "game_over":
                    bird_y, bird_velocity, pipes, score = reset_game()
                    game_state = "playing"
                    bird_velocity = FLAP_STRENGTH

            elif event.key == pygame.K_r and game_state == "game_over":
                bird_y, bird_velocity, pipes, score = reset_game()
                game_state = "start"

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if game_state == "start":
                game_state = "playing"
                bird_velocity = FLAP_STRENGTH

            elif game_state == "playing":
                bird_velocity = FLAP_STRENGTH

            elif game_state == "game_over":
                bird_y, bird_velocity, pipes, score = reset_game()
                game_state = "playing"
                bird_velocity = FLAP_STRENGTH


# 12. Update physics and game Objects

    if game_state == "playing":

        # Gravity increase downward velocity
        bird_velocity += GRAVITY
        bird_y += bird_velocity

        # move pipes left 
        for pipe in pipes:
            pipe["x"] -= PIPE_SPEED

        # Create the next pipe 
        rightmost_x = max(pipe["x"] for pipe in pipes)

        if rightmost_x < WIDTH - PIPE_SPWAN_DISTANCE:
            pipes.append(make_pipe(WIDTH + 10))

        # Delete pipes that leave the screen 
        pipes = [
            pipe for pipe in pipes
            if pipe["x"] + PIPE_WIDTH + 10 > 0
        ]

        # Bird collioson rectangle 
        bird_rect = pygame.Rect(
            BIRD_X - BIRD_RADIUS,
            int(bird_y) - BIRD_RADIUS,
            BIRD_RADIUS * 2,
             BIRD_RADIUS * 2 
        )

        # Check pipes and awards points
        for pipe in pipes:
            top_rect, bottom_rect = get_pipe_rectangles(pipe)

            if (
                bird_rect.colliderect(top_rect)
                or bird_rect.colliderect(bottom_rect)
            ):
                game_state = "game_over"
        
            if (
                not pipe["scored"]
                and pipe["x"] + PIPE_WIDTH < BIRD_X
            ):
                score += 1
                pipe["scored"] = True
        
        # Check celling And ground
        if bird_y - BIRD_RADIUS <= 0:
            game_state = "game_over"
    
        if bird_y + BIRD_RADIUS >= HEIGHT - GROUND_HEIGHT:
            game_state = "game_over"


    # 13. Draw the frame

    draw_background(screen)
    
    for pipe in pipes:
        top_rect, bottom_rect = get_pipe_rectangles(pipe)
        draw_pipe(screen, top_rect)
        draw_pipe(screen, bottom_rect)

    draw_bird(screen, BIRD_X, bird_y)

    draw_text(
        screen, str(score), large_font,
        WHITE, (WIDTH // 2, 48)
    )
    # Start screen 
    if game_state =="start":
        draw_text(
            screen, "FLAPPY BIRD", large_font,
            BLACK, (WIDTH // 2, HEIGHT // 2 - 65)
        )

        draw_text(
            screen, "Press SPACE or click to start",
            small_font, BLACK,
            (WIDTH // 2, HEIGHT // 2 - 20)
        )

    # Game over screen
    elif game_state == "game_over":
        draw_text(
            screen, "GAME OVER", large_font,
            BLACK, (WIDTH // 2, HEIGHT // 2 - 45)
        )

    draw_text(
        screen, f"Score: {score}", font, 
        BLACK, (WIDTH // 2,  HEIGHT // 2 + 5)
    )

    draw_text(
        screen, "SPACE/click: retry  R: title ",
        small_font, BLACK,
        (WIDTH // 2, HEIGHT // 2 + 50)
    )

    # Display the finished frame
    pygame.display.flip()  


# 14. Clean exit

pygame.quit()