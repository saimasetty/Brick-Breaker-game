import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Brick Breaker Game')

# Colors
WHITE = (255, 255, 255)
LUXURIOUS_METALLIC_BLUE_GREEN = (87, 108, 67)  # Lusous metallic blue-green
LIGHT_SKY_BLUE = (135, 206, 250)
DARK_BACKGROUND = (48, 62, 79)  # #303E4F
BRICK_COLOR = (244, 159, 28)  # #F49F1C

# Fonts
font = pygame.font.Font(pygame.font.match_font("bree serif"), 32)
large_font = pygame.font.Font(pygame.font.match_font("bree serif"), 50)

# Paddle, ball, and brick settings
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10

# Game state variables
difficulty = "Medium"  # Default difficulty
paddle_speed = 10
ball_x_speed = 4
ball_y_speed = -4
score = 0
level = 1
lives = 3
paused = False  # Pause state

# Initialize positions
paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2

# Load background image
home_background_image = pygame.image.load(r"C:\Users\sai_kumar\Downloads\pythonprojectimage.png")
home_background_image = pygame.transform.scale(home_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Brick grid
def create_bricks():
    bricks = []
    rows, cols = 5, 8
    brick_width, brick_height = 70, 30
    for row in range(rows):
        brick_row = []
        for col in range(cols):
            x = col * (brick_width + 10) + 50
            y = row * (brick_height + 10) + 50
            brick_row.append(pygame.Rect(x, y, brick_width, brick_height))
        bricks.append(brick_row)
    return bricks

bricks = create_bricks()

# Set difficulty settings
def set_difficulty(level):
    global paddle_speed, ball_x_speed, ball_y_speed, PADDLE_WIDTH, PADDLE_HEIGHT
    if level == "Easy":
        paddle_speed, ball_x_speed, ball_y_speed = 12, 3, -3
        PADDLE_WIDTH = 120  # Larger paddle for easy difficulty
        PADDLE_HEIGHT = 30
    elif level == "Medium":
        paddle_speed, ball_x_speed, ball_y_speed = 10, 4, -4
        PADDLE_WIDTH = 100  # Default size for medium difficulty
        PADDLE_HEIGHT = 20
    elif level == "Hard":
        paddle_speed, ball_x_speed, ball_y_speed = 8, 5, -5
        PADDLE_WIDTH = 80  # Smaller paddle for hard difficulty
        PADDLE_HEIGHT = 15

# Start menu
def start_menu():
    global difficulty
    while True:
        screen.blit(home_background_image, (0, 0))  # Set the home page background
        title_text = large_font.render("Brick Breaker", True, LUXURIOUS_METALLIC_BLUE_GREEN)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))

        options = [
            ("Press Space to Start", 0),
            ("Press P for Pause ", 50),
            ("Press 1 for Easy", 100),
            ("Press 2 for Medium", 150),
            ("Press 3 for Hard", 200),
            ("Press P for Pause during Gameplay", 300)
        ]
        for text, offset in options:
            rendered_text = font.render(text, True, LUXURIOUS_METALLIC_BLUE_GREEN)
            screen.blit(rendered_text, (SCREEN_WIDTH // 2 - rendered_text.get_width() // 2, SCREEN_HEIGHT // 2 + offset))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True  # Start the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_1:
                    difficulty = "Easy"
                    set_difficulty(difficulty)
                    return True  # Start the game
                elif event.key == pygame.K_2:
                    difficulty = "Medium"
                    set_difficulty(difficulty)
                    return True  # Start the game
                elif event.key == pygame.K_3:
                    difficulty = "Hard"
                    set_difficulty(difficulty)
                    return True  # Start the game

# Reset game state
def reset_game():
    global paddle_x, paddle_y, ball_x, ball_y, ball_x_speed, ball_y_speed, score, level, lives, bricks
    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
    paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    score = 0
    level = 1
    lives = 3
    bricks = create_bricks()
    set_difficulty(difficulty)

# Ball-brick collision detection and destruction
def check_ball_brick_collision():
    global score
    for row in bricks:
        for brick in row:
            ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, 2 * BALL_RADIUS, 2 * BALL_RADIUS)
            if brick.colliderect(ball_rect):
                row.remove(brick)
                global ball_y_speed
                ball_y_speed = -ball_y_speed
                score += 10
                return

# Ball-paddle collision detection
def check_ball_paddle_collision():
    global ball_x_speed, ball_y_speed
    ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, 2 * BALL_RADIUS, 2 * BALL_RADIUS)
    paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)

    if ball_rect.colliderect(paddle_rect):
        ball_y_speed = -ball_y_speed
        ball_center = ball_x
        paddle_center = paddle_x + PADDLE_WIDTH // 2
        distance_from_center = (ball_center - paddle_center) / (PADDLE_WIDTH // 2)
        ball_x_speed += distance_from_center * 3

#pause game
def pause_menu():
    global paused
    while paused:
        screen.fill(DARK_BACKGROUND)
        pause_text = large_font.render("Game Paused", True, WHITE)
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 3))

        options = [
            ("Press R to Resume", 50),
            ("Press Q to Quit", 100)
        ]
        for text, offset in options:
            rendered_text = font.render(text, True, WHITE)
            screen.blit(rendered_text, (SCREEN_WIDTH // 2 - rendered_text.get_width() // 2, SCREEN_HEIGHT // 2 + offset))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Resume the game
                    paused = False
                elif event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    quit()

# Game loop
# Game loop
def game_loop():
    global paddle_x, paddle_y, ball_x, ball_y, ball_x_speed, ball_y_speed, lives, score, level, bricks, paused
    while True:
        if paused:
            pause_menu()  # Corrected from pause_game() to pause_menu()

        screen.fill(DARK_BACKGROUND)  # Set the gameplay background color

        if not any(bricks):
            level += 1
            bricks = create_bricks()
            set_difficulty(difficulty)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Toggle pause
                    paused = not paused

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT]:
            paddle_x += paddle_speed

        if paddle_x < 0:
            paddle_x = 0
        if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
            paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

        ball_x += ball_x_speed
        ball_y += ball_y_speed

        if ball_x <= BALL_RADIUS or ball_x >= SCREEN_WIDTH - BALL_RADIUS:
            ball_x_speed = -ball_x_speed
        if ball_y <= BALL_RADIUS:
            ball_y_speed = -ball_y_speed
        elif ball_y >= SCREEN_HEIGHT - BALL_RADIUS:
            lives -= 1
            if lives == 0:
                game_over()
                reset_game()
                start_menu()
                return
            else:
                ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                ball_x_speed = 4
                ball_y_speed = -4

        check_ball_paddle_collision()
        check_ball_brick_collision()

        pygame.draw.rect(screen, LIGHT_SKY_BLUE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.circle(screen, LIGHT_SKY_BLUE, (ball_x, ball_y), BALL_RADIUS)

        for row in bricks:
            for brick in row:
                pygame.draw.rect(screen, BRICK_COLOR, brick)

        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

        pygame.display.update()
        pygame.time.Clock().tick(60)

    

# Start the game
start_menu()
game_loop()

pygame.quit()
quit()
