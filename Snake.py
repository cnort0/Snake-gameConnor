import pygame
import time
import random
from score import Score  # Import the Score class

pygame.init()

# Setting up colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Setting up display dimensions
width = 600
score_display_height = 50
height = 400 + score_display_height
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Game variables
snake_block = 10
snake_speed = 15

clock = pygame.time.Clock()

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = pygame.font.SysFont("bahnschrift", 25).render(msg, True, color)
    dis.blit(mesg, [width / 6, height / 3])

def gameLoop():  # Creating a function for the game loop
    game_over = False
    game_close = False

    # Initialize score
    score = Score()

    # Initialize snake position aligned to grid
    x1 = round((width / 2) / 10.0) * 10.0
    y1 = round((height / 2) / 10.0) * 10.0

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(score_display_height, height - snake_block) / 10.0) * 10.0
    recent_key = 5
    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            score.display(dis, width)  # Display final score
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and recent_key != 2:
                    x1_change = -snake_block
                    y1_change = 0
                    recent_key = 1
                elif event.key == pygame.K_RIGHT and recent_key != 1:
                    x1_change = snake_block
                    y1_change = 0
                    recent_key = 2
                elif event.key == pygame.K_UP and recent_key != 4:
                    y1_change = -snake_block
                    x1_change = 0
                    recent_key = 3
                elif event.key == pygame.K_DOWN and recent_key != 3:
                    y1_change = snake_block
                    x1_change = 0
                    recent_key = 4

        if x1 >= width or x1 < 0 or y1 >= height or y1 < score_display_height:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(black, rect=[0, 0, width, score_display_height])  # Fill score area with black background
        dis.fill(blue, rect=[0, score_display_height, width, height - score_display_height])
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(snake_block, snake_list)
        score.display(dis, width)  # Display score

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(score_display_height, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            score.increase()  # Increase score when food is eaten

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
