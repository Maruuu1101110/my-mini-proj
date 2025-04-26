import pygame as pg
from pygame.locals import *
import random
import json

# Window setup and objects initials
WIDTH, HEIGHT = 600, 900
basket_size = int((WIDTH * 0.09) + (HEIGHT * 0.09 ))
fruit_size, fruit_speed = int((WIDTH * 0.04) + (HEIGHT * 0.04)), 4

# Colors
red = pg.Color(255,0,0)
green = pg.Color(0,255,0)
blue = pg.Color(0,0,255)
black = pg.Color(0,0,0)
white = pg.Color(242,242,242)
yellow = pg.Color(255,255,0)
overlay = pg.Surface((WIDTH,HEIGHT), pg.SRCALPHA)
overlay.fill((0,0,0,128))

# Object Initializer
class GameObject:
    def __init__(self, x, y, image=None):
        self.x = x
        self.y = y
        self.image = image
        self.rect = (pg.Rect(x, y, image.get_width(), 50) if image else None)

    # places objects on screen
    def draw(self, window):
        if self.image:
            window.blit(self.image, (self.x, self.y))
        elif self.rect:
            pg.draw.rect(window, red, self.rect)

    # updates ofcourse
    def update_rect(self):
        if self.rect:
            self.rect.topleft = (self.x, self.y)

# Objects Movement Handling
class Movable(GameObject):
    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy
        self.update_rect()

# Basket Object
class Basket(Movable):
    def __init__(self, x, y, speed, image):
        super().__init__(x, y, image)
        self.speed = speed

    # key press for basket movement
    def handle_input(self):
        keys = pg.key.get_pressed()
        if (keys[K_RIGHT] or keys[K_d]) and self.x < WIDTH - basket_size:
            self.move(dx=self.speed)
        if (keys[K_LEFT] or keys[K_a]) and self.x > 0:
            self.move(dx=-self.speed)

# Falling Fruits Object
class Fruit(Movable):
    def __init__(self, x, y):
        super().__init__(x, y)
        fruits_choices = [
                            "assets/fruits/apple.png",
                            "assets/fruits/orange.png",
                            "assets/fruits/cherry.png",
                            "assets/fruits/mango.png",
                            "assets/fruits/strawberry.png"
        ]
        self.image = pg.transform.scale(pg.image.load(random.choice(fruits_choices)),(fruit_size, fruit_size))
        self.rect = self.image.get_rect(topleft =(100,200))

    # upadte fruit falling / enable fall
    def update(self):
        self.move(dy=fruit_speed)

    # resets the falling fruits position
    def reset(self):
        self.x = random.randint(0, WIDTH - fruit_size)
        self.y = random.randint(-1700, -50)
        self.update_rect()

# Main Class, handles how the game runs, excuse myself for the arrangement... added other features randomly so it seems messy (too lazy to arrange)
class MainGame:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Fruit Catcher")
        self.clock = pg.time.Clock()
        self.fps = 60
        self.score = 0
        self.highscore = json.load(open("scores.json", "r"))
        self.lives = 3
        self.font = pg.font.Font("fonts/JungleAdventurer.ttf", 40)
        self.title_font = pg.font.Font("fonts/JungleAdventurer.ttf", 60)
        self.texts_font = pg.font.Font("fonts/JungleAdventurer.ttf", 25)
        self.timer = 0
        self.level = 1
        self.basket = Basket(WIDTH // 2 - basket_size // 2, 
                            HEIGHT - basket_size - 10, 
                            10, # speed
                            pg.transform.scale(pg.image.load("assets/basket/fruit_basket_0.png"), (basket_size, basket_size))
                            )
        self.background = pg.transform.scale(pg.image.load("assets/background.png"), (WIDTH, HEIGHT))
        self.fruits = [Fruit(random.randint(0, WIDTH - fruit_size), random.randint(-1700, -50)) for _ in range(3)]
        self.basket_fill = {
            50:pg.transform.scale(pg.image.load("assets/basket/fruit_basket_1.png"),(basket_size, basket_size)),
            100:pg.transform.scale(pg.image.load("assets/basket/fruit_basket_2.png"),(basket_size, basket_size))
        }

    # run...
    def run(self):
        self.show_menu()
        run = True
        while run:
            self.timer += 0.015
            self.update_game()
            self.handle_events()
            self.draw_game()
            pg.display.flip()
            self.clock.tick(self.fps)
        pg.quit()

    # Showing intro / game menu
    def show_menu(self):
        menu = True
        self.window.blit(self.background, (0, 0))
        self.window.blit(overlay, (0,0))
        title = self.title_font.render("Fruit Catcher", 1, yellow)
        start_prmpt = self.font.render("Press SPACE to START", 1, white)
        credit = self.texts_font.render("By: EJ Rosialda", 1, green)
        self.window.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70)))
        self.window.blit(start_prmpt, start_prmpt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        self.window.blit(credit, credit.get_rect(center=(WIDTH // 2, HEIGHT - 70)))
        while menu:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                if event.type == KEYDOWN and event.key == K_SPACE:
                    menu = False
            pg.display.flip()
            self.clock.tick(self.fps)

    def game_pause(self):
        pause = True
        self.window.blit(overlay, (0,0))
        pause_txt = self.font.render("GAME PAUSED", 1, green)
        instruction_txt = self.font.render("SPACE TO CONTINUE", 1, white)
        self.window.blit(pause_txt, pause_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
        self.window.blit(instruction_txt, instruction_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))
        while pause:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_ESCAPE):
                    pause = False
            pg.display.update()
            self.clock.tick(self.fps)

    # handles game updates
    def update_game(self):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_ESCAPE):
                self.game_pause()

        self.basket.handle_input()
        for fruit in self.fruits:
            fruit.update()
            if fruit.rect.colliderect(self.basket.rect):
                self.score += 5
                fruit.reset()
    
    # reset game data
    def rewrite(self):
        global fruit_speed
        self.lives = 3
        self.score = 0
        self.level = 1
        fruit_speed = 4
        self.fruits.clear()
        self.fruits = [Fruit(random.randint(0, WIDTH - fruit_size), random.randint(-700, -50)) for _ in range(3)]
        self.timer = 0
        self.basket.image = pg.transform.scale(pg.image.load("assets/basket/fruit_basket_0.png"), (basket_size, basket_size))

    # game over screen
    def game_over(self):
        pg.event.clear()
        game_over = True
        self.window.blit(overlay, (0,0))
        game_over_txt = self.title_font.render("Game Over!", 1, red)
        final_score = self.font.render(f"Score: {self.score}", 1, green)
        restart_txt = self.font.render("Press SPACE to RESTART game", 1, white)
        exit_txt = self.font.render("ESC to exit", 1, white)
        self.window.blit(game_over_txt, game_over_txt.get_rect(center=(WIDTH // 2, HEIGHT // 3)))
        self.window.blit(final_score, final_score.get_rect(center=(WIDTH // 2, HEIGHT // 2.5)))
        self.window.blit(restart_txt, restart_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        self.window.blit(exit_txt, exit_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))
        while game_over:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.rewrite()
                        game_over = False
                    elif event.key == K_ESCAPE:
                        pg.quit()
                        exit()
            pg.display.flip()
            self.clock.tick(self.fps)

    # function for saving highscore
    def save_high(self, score):
        with open("scores.json", "w") as sfile:
            return json.dump(score,sfile)

    # ...something something
    def handle_events(self):
        global fruit_speed
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()

        for fruit in self.fruits:
            if fruit.y >= HEIGHT:
                self.lives -= 1
                fruit.reset()

        if self.score in self.basket_fill:
            self.basket.image = self.basket_fill[self.score]        

        high = self.highscore
        if self.score > high["highscore"]:
            high["highscore"] = self.score
            self.save_high(high)

        if self.timer >= 20:
            self.level += 1
            fruit_speed += 1
            self.timer = 0

        if self.lives == 0:
            self.game_over()

    # Draw all game objects and etcc
    def draw_game(self):
        self.window.blit(self.background, (0,0))
        self.basket.draw(self.window)
        for fruit in self.fruits:
            fruit.draw(self.window)
        score_txt = self.font.render(f"Score: {self.score}", 1, white)
        lives_txt = self.font.render(f"Lives: {self.lives}", 1, white)
        speed_level_txt = self.font.render(f"Level: {self.level}",1 ,white)
        highscore_txt = self.font.render(f"High: {self.highscore['highscore']}", 1, white)
        if self.highscore:
            self.window.blit(highscore_txt, (WIDTH - 180, 20))
        self.window.blit(score_txt, (20,20))
        self.window.blit(lives_txt, (20,60))
        self.window.blit(speed_level_txt, (WIDTH - 180, 60))

        # Debug
        #self.window.blit(self.font.render(f"Fruit Speed: {fruit_speed} Seconds: {int(self.timer)}",1,white), (20,140))
        #self.window.blit(self.font.render(f"Timer: {int(self.timer)}", 1, white), (20, 100))

if __name__=="__main__":
    MainGame().run()
