import pygame as pg 
from pygame.locals import *
import random
import json
pg.init()

# main window and others
width = 1200
height = 700
window = pg.display.set_mode((width,height))
pg.display.set_caption("Jump!!!")
clock = pg.time.Clock()
fps = 100
font = pg.font.SysFont("Lucida Console",25)
score = 0

# Colors and color management(transition)
white = pg.Color(255,255,255)
black = pg.Color(0,0,0)
gray = pg.Color(41,41,41)
yellow = pg.Color(255,255,0)
red = pg.Color(255,0,0)
green = pg.Color(0,255,0)
transition_score = 650
t_time = 0
overlay = pg.Surface((width,height), pg.SRCALPHA)
overlay_w = pg.Color(255,255,255,128)
overlay_b = pg.Color(0,0,0,128)
overlay.fill(overlay_b.lerp(overlay_w, t_time))
 
# Rawr
dino_w, dino_h = 25,50
dino_x, dino_y = 50, height - (dino_h - 25)
dino = pg.Rect(dino_x, dino_y,dino_w,dino_h)

# Land
land_h = 2
land_y = height - 25
land = pg.Rect(0, land_y, width + 250, land_h)

# cactus
cac_w, cac_h = 25, 50
cac_frequency = 6
cactus = [pg.Rect(random.randint(width,width + 1000), land_y - 50, cac_w, cac_h) for _ in range(1, cac_frequency, 2)]
flying_cactus = [pg.Rect(random.randint(width,width + 2500), land_y - 85, cac_w, cac_h) for _ in range(1, cac_frequency, 2)]

# gravity stuff
velocity = 0
gravity_str = 0.2
jump_strength = -7
ground_y = land_y - 50

# highscore handling
def load_hs():
    with open("leaderboards.json","r") as loadfile:
        return json.load(loadfile)
def save_hs(score):
    with open("leaderboards.json","w") as savefile:
        json.dump(score,savefile)
highscore = load_hs()

# reset data after game over
def rewrite():
    global dino, dino_color, cactus, flying_cactus, cactus_speed, cac_frequency, score, t_time, ground_y
    dino_color = white.lerp(black, t_time)
    dino.w, dino.h = dino_w, dino_h
    dino.x, dino.y = dino_x, dino_y
    ground_y = land_y - 50
    score = 0
    t_time = 0
    cactus_speed = 3
    cac_frequency = 6
    cactus.clear()
    flying_cactus.clear()
    for _ in range(1, cac_frequency, 2):
        cactus.append(pg.Rect(random.randint(width, width + 1000), land_y - 50, cac_w, cac_h))
        flying_cactus.append(pg.Rect(random.randint(width, width + 2500), land_y - 85, cac_w, cac_h))

# Game Over
def game_over():
    pg.event.clear()
    pause = True
    window.blit(overlay, (0,0))
    window.blit(font.render("Game Over!",True,white.lerp(black, t_time)), (width // 2 - 75, height // 2 - 50))
    window.blit(font.render(f"Your Score: {int(score)}",True, white.lerp(black, t_time)), (width // 2 - 125, height // 2 - 10))
    window.blit(font.render("Press SPACE to try again",True,white.lerp(black, t_time)), (width // 2 - 175, height // 2 + 30))   
    while pause:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                pause = False
                pg.time.delay(1000)
                rewrite()

        pg.display.update()

# Main Menu  Screen
def menu():
    menu = True
    window.fill(gray)
    window.blit(font.render("DINO GAME", True, white), (width // 2 - 75, height // 2 - 50))
    window.blit(font.render("Press SPACE to Start",True, white), (width // 2 - 150, height // 2 + 30))
    while menu:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                menu = False
        pg.display.update()

# main program
run = True
menu()
while run:
    clock.tick(fps)   
    if score >= transition_score:
        t_time = min(t_time + 0.02, 1.0)

    window.fill(gray.lerp(white, t_time))   
    cactus_speed = 3 + (score / 500)
    score += 0.15
    
    # quit
    for event in pg.event.get():
        if event.type == QUIT:
            run = False

    # controls
    keys = pg.key.get_pressed()
    if keys[pg.K_d] and dino.x < width:
        dino.x += 3
    if keys[pg.K_a] and dino.x > 0:
        dino.x -= 3
    if keys[pg.K_SPACE] and dino.y >= ground_y:
        velocity = jump_strength 
    if keys[K_s]:
        dino.h = 25
        ground_y = height - 50
    else:
        dino.h = 50
        ground_y = height - 75           

    #gravity check
    velocity += gravity_str
    dino.y += velocity
    
    # ground collision
    if dino.y >= ground_y:
        dino.y = ground_y
        velocity = 0
    
    # move cactus..or player dunno ..also dispose cac for memory optimization
    for cac in cactus[:]:
        cac.x -= cactus_speed
        if cac.right < 0:
            cactus.remove(cac)
            cactus.append(pg.Rect(random.randint(width, width + 1000), land_y - 50, cac_w, cac_h))
            
    # flying cactus appear
    if score >= 250:
        for fcac in flying_cactus[:]:
            fcac.x -= cactus_speed
            if fcac.right < 0:
                flying_cactus.remove(fcac)
                flying_cactus.append(pg.Rect(random.randint(width, width + 2500), land_y - 85, cac_w, cac_h))

    # cactus draw
    for cac in cactus:
        pg.draw.rect(window, yellow.lerp(green, t_time), (cac[0],cac[1],cac_w,cac_h))
    for fcac in flying_cactus:
        pg.draw.rect(window, yellow.lerp(green, t_time), (fcac[0],fcac[1],cac_w,cac_h)) 
        
    # scoring system
    if score > highscore["highscore"]:
        highscore["highscore"] = int(score)
        save_hs(highscore)
    score_text = font.render(f"Score: {int(score)}",True,white.lerp(black, t_time))
    hs_text = font.render(f"HI: {highscore['highscore']}",True,white.lerp(black, t_time))
    
    #other info
    controls_info_txt = font.render("= [A] [S] [D] to move =",1, white.lerp(black, t_time))
    jump_info_txt = font.render("= [SPACE] to jump =", 1, white.lerp(black, t_time))

    # land draw
    pg.draw.rect(window,white.lerp(gray, t_time),land)

    # dino draw
    pg.draw.rect(window,white.lerp(gray, t_time),dino)

    # draw txt
    window.blit(score_text,(50, 20))
    window.blit(hs_text,(50, 50))
    window.blit(controls_info_txt, controls_info_txt.get_rect(center=(width // 2 , 50)))
    window.blit(jump_info_txt, jump_info_txt.get_rect(center=(width // 2, 80)))

    # debugger
    window.blit(font.render(f"FPS: {int(clock.get_fps())}",True,white.lerp(black, t_time)),(width - 175, 20))

    # dino collision w/ cactus
    for cac in cactus:
        if dino.colliderect(cac):
            pg.draw.rect(window,red,dino)
            pg.display.update()
            pg.time.delay(1000)
            game_over()
    for fcac in flying_cactus:
        if dino.colliderect(fcac):
            pg.draw.rect(window,red,dino)
            pg.display.update()
            pg.time.delay(1000)
            game_over()

    pg.display.flip()
    
pg.quit()
