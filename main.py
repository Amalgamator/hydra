import pygame
import random
import math

"""
TO DO:
- add worlds
- add enemies
- fix GAME_OVER by doing a 180° too fast
"""


pygame.init()
pygame.display.set_caption('HYDRA - beta')
clock = pygame.time.Clock()
FPS = 20

display_w = 800
display_h = 600
g_display = pygame.display.set_mode((display_w, display_h))

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
    
def pickfont(name, size):
    font = pygame.font.SysFont(name, size, bold=False)
    return font

def txt_obj(msg, color):
    txt_surf = pickfont("Verdana", 20).render(msg, True, color)
    return txt_surf, txt_surf.get_rect()

def disp_msg(msg, color, align_x=0, align_y=0):
    txt_surf, txt_rec = txt_obj(msg, color)
    txt_rec.center = (display_w / 2) + align_x, (display_h / 2) + align_y
    g_display.blit(txt_surf, txt_rec)

def snake(boxel, snake_list):
    for xny in snake_list:
        g_display.fill(green, rect=[xny[0], xny[1], boxel, boxel])

def game_loop():
    game_exit = False
    game_over = False
    
    # start position
    head_x = display_w / 2
    head_y = display_h / 2

    # increments
    x_step = 0
    y_step = 0
    speed_mod = 1
    
    # segments
    snake_list = []
    snake_length = 1
    lvl = 1
    apple_c = 0
    apples_needed = 1
    
    boxel = 5       
    collision_state = True
    
    # apple
    apple_s = 10
    apple_x = round(random.randrange(0, display_w - apple_s))
    apple_y = round(random.randrange(0, display_h - apple_s))

    while not game_exit:

        while game_over is True:

            # g_display.fill(black)
            disp_msg("GAME OVER!", red, 0, -50)
            disp_msg("[R]etry", black, -100)
            disp_msg("[Q]uit", black, 100)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    game_exit = True
                if event.type == pygame.KEYDOWN:
                    uni = event.dict['unicode']
                    if uni == 'q':
                        game_over = False
                        game_exit = True
                    elif uni == 'r':
                        game_loop()

        # controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                uni = event.dict['unicode']
                if event.key == pygame.K_LEFT or uni == 's' or uni == 'S':
                    if x_step == boxel:
                        break
                    elif x_step != boxel:
                        x_step = -boxel
                        y_step = 0
                elif event.key == pygame.K_RIGHT or uni == 'f' or uni == 'F':
                    if x_step == -boxel:
                        break
                    elif x_step != -boxel:
                        x_step = boxel
                        y_step = 0
                elif event.key == pygame.K_UP or uni == 'e' or uni == 'E':
                    if y_step == boxel:
                        break
                    elif y_step != boxel:
                        x_step = 0
                        y_step = -boxel
                elif event.key == pygame.K_DOWN or uni == 'd' or uni == 'D':
                    if y_step == -boxel:
                        break
                    elif y_step != -boxel:
                        x_step = 0
                        y_step = boxel
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                # FOR TESTING PURPOSES ONLY
                elif uni == '+':
                    speed_mod += 5         
                elif uni == '-':
                    speed_mod -= 5
                elif uni == 'a':
                    snake_length += 1
                    apple_c += 1
        
        # borders
        if lvl < 10:
            border = False
        elif lvl >= 10 and lvl < 20:
            border = True
        else:
            border = False
    

        if border == True:
            g_display.fill(black, rect=[0,0,800,600])
            g_display.fill(white, rect=[6,6,788,588])
        else:
            g_display.fill(white)

        if head_x <= 0:
            if border is False:
                head_x = display_w - boxel
            elif border is True:
                game_over = True
        elif head_x >= display_w:
            if border is False:
                head_x = 0
            elif border is True:
                game_over = True
        elif head_y <= 0:
            if border is False:
                head_y = display_h - boxel
            elif border is True:
                game_over = True
        elif head_y >= display_h:
            if border is False:
                head_y = 0
            elif border is True:
                game_over = True

        head_x += x_step
        head_y += y_step

        # draw the apple
        g_display.fill(red, rect=[apple_x, apple_y, apple_s, apple_s])

        # how do you level them apples!!
        if apple_c > apples_needed:
            lvl += 1
            apple_c = 0
        apples_needed = (1+(lvl**3)/262144)

        disp_msg("Snake: " + str(snake_length), black, -320, -260)
        disp_msg("needed: " + str(int(apples_needed - apple_c)), black, -320, -220)
        disp_msg("Lvl: " + str(lvl), black, -320, -240)

        # redraw snake
        snake_head = []
        snake_head.append(head_x)
        snake_head.append(head_y)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # collision detection
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over = True 

        snake(boxel, snake_list)

        # eating the apples
        if head_x + boxel > apple_x and head_x < apple_x + apple_s:
            if head_y + boxel > apple_y and head_y < apple_y + apple_s:
                apple_x = round(random.randrange(0, display_w - apple_s))
                apple_y = round(random.randrange(0, display_h - apple_s))
                snake_length += 1
                apple_c += 1

        # update screen
        pygame.display.update()
        clock.tick(FPS + speed_mod)

    pygame.quit()
    quit()
    
game_loop()
