import pygame as pg
from pygame.locals import *
import random
import json

#window setup
WIDTH, HEIGHT = 1200, 700
BEE_SIZE = 60
PIPE_WIDTH = 80
GAP_HEIGHT = 150
PIPE_SPEED = 7

#colors
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
overlay = pg.Surface((WIDTH,HEIGHT), pg.SRCALPHA)
overlay.fill((0,0,0,128))


class GameObject:
    def __init__(self, x, y, image=None):
        self.x = x
        self.y = y
        self.image = image
        self.rect = image.get_rect(topleft=(x, y)) if image else pg.Rect(x, y, 50, 50)

    def draw(self, window):
        if self.image:
            window.blit(self.image, (self.x, self.y))
        else:
            pg.draw.rect(window, (255, 0, 0), self.rect)

    def update_rect(self):
        self.rect.topleft = (self.x, self.y)

class Bee(GameObject):
    def __init__(self, x, y, images):
        super().__init__(x, y, images[0])
        self.images = images
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.5

        self.velocity = 0
        self.gravity = 2
        self.jump_strength = -15
        self.angle = 0

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        self.update_rect()

        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]

        self.angle = max(-30, min(90, self.velocity * 3))

    def draw(self, window):
        rotated_image = pg.transform.rotate(self.images[self.current_frame], -self.angle)
        new_rect = rotated_image.get_rect(center=(self.x + self.image.get_width() // 2, self.y + self.image.get_height() // 2))
        window.blit(rotated_image, new_rect.topleft)

    def jump(self):
        self.velocity = self.jump_strength

class Pipe(GameObject):
    def __init__(self, x, y, height, flipped, image):
        super().__init__(x, y, image)
        self.height = height
        self.flipped = flipped
        if self.flipped:
            self.image = pg.transform.flip(self.image, False, True)
        self.image = pg.transform.scale(self.image, (PIPE_WIDTH, self.height))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.x -= PIPE_SPEED
        self.update_rect()

class MainGame:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Flappyyy Beee!!!")
        self.clock = pg.time.Clock()
        self.fps = 240

        #assets
        self.background = pg.transform.scale(pg.image.load("assets/background.png"), (WIDTH, HEIGHT))
        self.bee_img = [
            pg.transform.scale(pg.image.load("assets/bee1.png"), (BEE_SIZE, BEE_SIZE-10)),
            pg.transform.scale(pg.image.load("assets/bee2.png"), (BEE_SIZE, BEE_SIZE-10)),
            pg.transform.scale(pg.image.load("assets/bee3.png"), (BEE_SIZE, BEE_SIZE-10))
        ]
        self.pipe_img = pg.image.load("assets/pipe.png")

        self.font = pg.font.Font("fonts/JungleAdventurer.ttf", 40)
        self.title_font = pg.font.Font("fonts/JungleAdventurer.ttf", 60)
        self.texts_font = pg.font.Font("fonts/JungleAdventurer.ttf", 25)

        # others
        self.bee = Bee(100, HEIGHT//2, self.bee_img)
        self.pipes = []
        self.spawn_pipe()
        self.score = 0
        self.highscore = json.load(open("scores.json", "r"))

    #obstacle spawner
    def spawn_pipe(self):
        gap_y = random.randint(150, HEIGHT-150)
        top_pipe = Pipe(WIDTH, 0, gap_y - GAP_HEIGHT//2, True, self.pipe_img)
        bottom_pipe = Pipe(WIDTH, gap_y + GAP_HEIGHT//2, HEIGHT - gap_y, False, self.pipe_img)
        self.pipes.append(top_pipe)
        self.pipes.append(bottom_pipe)

    def run(self):
        self.show_menu()
        running = True
        spawn_timer = 0
        while running:
            self.clock.tick(self.fps)
            spawn_timer += 1
            if spawn_timer > 90:
                self.spawn_pipe()
                spawn_timer = 0

            for event in pg.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.bee.jump()

            self.update()
            self.draw()

        pg.quit()

    def update(self):
        self.bee.update()

        for pipe in self.pipes:
            pipe.update()
        self.pipes = [pipe for pipe in self.pipes if pipe.x + PIPE_WIDTH > 0]

        #collision
        for pipe in self.pipes:
            if self.bee.rect.colliderect(pipe.rect):
                self.game_over()

        if self.bee.y > HEIGHT or self.bee.y < 0:
            self.game_over()

        #scorringg
        for pipe in self.pipes:
            if pipe.x + PIPE_WIDTH < self.bee.x and not hasattr(pipe, 'scored'):
                self.score += 0.5
                pipe.scored = True

        high = self.highscore
        if self.score >= high["highscore"]:
            high["highscore"] = self.score
        json.dump(high, open("scores.json","w"))

    def draw(self):
        self.window.blit(self.background, (0, 0))
        self.bee.draw(self.window)
        for pipe in self.pipes:
            pipe.draw(self.window)
        score_txt = self.font.render(f"Score: {int(self.score)}", True, BLACK)
        highscore_txt = self.font.render(f"High Score: {int(self.highscore['highscore'])}", True, BLACK)
        self.window.blit(score_txt, (20, 20))
        self.window.blit(highscore_txt, (20, 50))
        pg.display.update()

    def reset_game(self):
        self.bee = Bee(100, HEIGHT//2, self.bee_img)
        self.pipes.clear()
        self.score = 0

    def game_over(self):
        pg.event.clear()
        game_over = True
        self.window.blit(overlay, (0,0))
        game_over_txt = self.title_font.render("Game Over!", 1, RED)
        final_score = self.font.render(f"Score: {int(self.score)}", 1, GREEN)
        restart_txt = self.font.render("Press SPACE to RESTART game", 1, WHITE)
        exit_txt = self.font.render("ESC to exit", 1, WHITE)
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
                        self.reset_game()
                        game_over = False
                    elif event.key == K_ESCAPE:
                        pg.quit()
                        exit()
            pg.display.flip()
            self.clock.tick(self.fps)

    def show_menu(self):
        menu = True
        self.window.blit(self.background, (0, 0))
        self.window.blit(overlay, (0,0))
        title = self.title_font.render("Flappy Beee", 1, YELLOW)
        start_prmpt = self.font.render("Press SPACE to START", 1, WHITE)
        credit = self.texts_font.render("By: EJ Rosialda", 1, GREEN)
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

if __name__ == "__main__":
    MainGame().run()

#referenced from prev game (fruit catcher)