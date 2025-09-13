import pygame
import sys
import random
import os
import time

# initialize pygame
pygame.init()

# window
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# snake setup
snake_block = 40

# colors
LIGHT_GRASS = (170, 215, 81)   # light green grass
DARK_GRASS = (162, 209, 73)    # dark green grass
SNAKE_HEAD = (106, 90, 205)   # darker purple (head)
SNAKE_BODY = (176, 196, 222)  # lighter purple (body)
BUTTON_COLOR = (100, 149, 237) # cornflower blue
BUTTON_HOVER = (65, 105, 225)  # royal blue
GOLD = (255, 215, 0)           # special food (golden)
POISON = (138, 43, 226)        # poison food (purple)
TIMER_COLOR = (220, 20, 60)    # timer food (red)

# fonts
font = pygame.font.SysFont("arial", 35, bold=True)
big_font = pygame.font.SysFont("arial", 70, bold=True)

# -------- HIGH SCORE SYSTEM --------
def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

high_score = load_high_score()

def draw_score(score):
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text, (20, 20))
    hs_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(hs_text, (20, 60))

# -------- BACKGROUND (checkerboard grass) --------
def draw_background():
    for row in range(0, HEIGHT // snake_block):
        for col in range(0, WIDTH // snake_block):
            if (row + col) % 2 == 0:
                color = LIGHT_GRASS
            else:
                color = DARK_GRASS
            pygame.draw.rect(screen, color,
                             (col * snake_block, row * snake_block, snake_block, snake_block))

# -------- DRAW SNAKE --------
def snake_shape(snake):
    for i, block in enumerate(snake):
        x, y = block
        if i == 0:  # Head
            pygame.draw.rect(screen, SNAKE_HEAD, (x, y, snake_block, snake_block), border_radius=12)
            # eyes
            eye_size = 6
            eye_offset = 10
            pygame.draw.circle(screen, (255, 255, 255), (x + eye_offset, y + 10), eye_size)
            pygame.draw.circle(screen, (255, 255, 255), (x + snake_block - eye_offset, y + 10), eye_size)
            pygame.draw.circle(screen, (0, 0, 0), (x + eye_offset, y + 10), 3)
            pygame.draw.circle(screen, (0, 0, 0), (x + snake_block - eye_offset, y + 10), 3)
        else:
            pygame.draw.rect(screen, SNAKE_BODY, (x, y, snake_block, snake_block), border_radius=8)

# -------- FOOD SYSTEM --------
def random_food():
    x = random.randrange(0, WIDTH, snake_block)
    y = random.randrange(0, HEIGHT, snake_block)
    while True:
        r = random.randint(50, 255)
        g = random.randint(50, 255)
        b = random.randint(50, 255)
        color = (r, g, b)
        if color not in [LIGHT_GRASS, DARK_GRASS, SNAKE_HEAD, SNAKE_BODY]:
            break
    return {"pos": (x, y), "color": color, "type": "normal", "spawn_time": time.time()}

def random_special_food():
    x = random.randrange(0, WIDTH, snake_block)
    y = random.randrange(0, HEIGHT, snake_block)
    return {"pos": (x, y), "color": GOLD, "type": "gold", "spawn_time": time.time()}

def random_poison_food():
    x = random.randrange(0, WIDTH, snake_block)
    y = random.randrange(0, HEIGHT, snake_block)
    return {"pos": (x, y), "color": POISON, "type": "poison", "spawn_time": time.time()}

def random_timer_food():
    x = random.randrange(0, WIDTH, snake_block)
    y = random.randrange(0, HEIGHT, snake_block)
    return {"pos": (x, y), "color": TIMER_COLOR, "type": "timer", "spawn_time": time.time()}

def generate_food():
    chance = random.random()
    if chance < 0.05:
        return random_timer_food()
    elif chance < 0.15:
        return random_special_food()
    elif chance < 0.25:
        return random_poison_food()
    else:
        return random_food()

# -------- START SCREEN --------
def start_screen():
    button_width, button_height = 300, 100
    button_x = WIDTH//2 - button_width//2
    button_y = HEIGHT//2 - button_height//2

    while True:
        draw_background()
        title = big_font.render("SNAKE GAME", True, (0, 100, 0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
        hs_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
        screen.blit(hs_text, (WIDTH//2 - hs_text.get_width()//2, HEIGHT//4 + 80))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if button_x <= mouse_x <= button_x+button_width and button_y <= mouse_y <= button_y+button_height:
            color = BUTTON_HOVER
        else:
            color = BUTTON_COLOR

        pygame.draw.rect(screen, color, (button_x, button_y, button_width, button_height), border_radius=15)
        text = font.render("START GAME", True, (255, 255, 255))
        screen.blit(text, (button_x + button_width//2 - text.get_width()//2,
                           button_y + button_height//2 - text.get_height()//2))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_x <= mouse_x <= button_x+button_width and button_y <= button_y+button_height:
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

# -------- GAME OVER SCREEN --------
def game_over_screen(score):
    global high_score
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    draw_background()
    over_text = big_font.render("GAME OVER", True, (200, 0, 0))
    score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
    hs_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    restart_text = font.render("Press R to Restart or Q to Quit", True, (0, 0, 0))

    screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//3))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(hs_text, (WIDTH//2 - hs_text.get_width()//2, HEIGHT//2 + 40))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 80))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# -------- GAME LOOP --------
def game_loop():
    snake = [(200, 200), (160, 200), (120, 200)]
    dx, dy = snake_block, 0
    foods = [generate_food()]
    score = 0
    speed = 5
    clock = pygame.time.Clock()
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -snake_block
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, snake_block
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -snake_block, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = snake_block, 0
                elif event.key == pygame.K_p:
                    paused = not paused

        if not paused:
            head_x, head_y = snake[0]
            new_head = (head_x + dx, head_y + dy)

            # wrapping
            if new_head[0] < 0:
                new_head = (WIDTH - snake_block, new_head[1])
            elif new_head[0] >= WIDTH:
                new_head = (0, new_head[1])
            elif new_head[1] < 0:
                new_head = (new_head[0], HEIGHT - snake_block)
            elif new_head[1] >= HEIGHT:
                new_head = (new_head[0], 0)

            snake.insert(0, new_head)

            # check food collision
            ate = False
            for f in foods[:]:
                if new_head == f["pos"]:
                    if f["type"] == "gold":
                        score += 5
                        speed += 1.5
                        for _ in range(3):
                            snake.append(snake[-1])
                    elif f["type"] == "poison":
                        score = max(0, score - 3)
                        if len(snake) > 5:
                            snake = snake[:-3]
                    elif f["type"] == "timer":
                        score += 3
                        speed += 1
                    else:
                        score += 1
                        speed += 0.5
                    foods.remove(f)
                    ate = True

            if not ate:
                snake.pop()

            # spawn new foods (max 2)
            if len(foods) < 2 and random.random() < 0.05:
                foods.append(generate_food())

            # remove expired foods
            now = time.time()
            foods = [f for f in foods if now - f["spawn_time"] <= 7]

            # self collision
            if new_head in snake[1:]:
                if game_over_screen(score):
                    return game_loop()

        # draw
        draw_background()
        snake_shape(snake)
        for f in foods:
            pygame.draw.rect(screen, f["color"], (f["pos"][0], f["pos"][1], snake_block, snake_block), border_radius=12)
            if f["type"] == "poison":
                x, y = f["pos"]
                pygame.draw.line(screen, (255, 255, 255), (x+8, y+8), (x+snake_block-8, y+snake_block-8), 4)
                pygame.draw.line(screen, (255, 255, 255), (x+snake_block-8, y+8), (x+8, y+snake_block-8), 4)
        draw_score(score)

        if paused:
            pause_text = big_font.render("PAUSED", True, (0, 0, 150))
            screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2))

        pygame.display.flip()
        clock.tick(int(speed))

# run game
start_screen()
game_loop()
