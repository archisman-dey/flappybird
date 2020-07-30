import os, sys
import random
from collections import deque
import pygame

pygame.init()

size = width, height = 640, 480
screen = pygame.display.set_mode(size, flags = pygame.NOFRAME)

def resource_path(relative_path):
    # for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# resources
bg = pygame.image.load(resource_path('resources/background.png')).convert()
piller_up_image = pygame.image.load(resource_path('resources/piller_up.png')).convert_alpha()
piller_down_image = pygame.image.load(resource_path('resources/piller_down.png')).convert_alpha()
bird_image = pygame.image.load(resource_path('resources/bird.png')).convert_alpha()
game_over = pygame.image.load(resource_path('resources/game_over.png')).convert_alpha()

piller_up_rect_global = piller_up_image.get_bounding_rect()
piller_down_rect_global = piller_down_image.get_bounding_rect()
bird_rect_global = bird_image.get_bounding_rect().inflate(-16, -16)
bg_rect_global = bg.get_rect()
play_again_rect = pygame.Rect(290, 340, 230, 50)
quit_rect = pygame.Rect(350 , 400 , 100 , 55)

font = pygame.font.SysFont('kristenitc,consolas', 24)
font_bigger = pygame.font.SysFont('kristenitc,consolas', 36)
font_color = (101, 0, 0)
hint_rendered = font_bigger.render("Press SPACE to start!", True, font_color)

try:
    with open('best_score.txt', 'r') as file:
        best_score = int(file.read())
except OSError:
    best_score = 0

class Piller:
    def __init__(self, xinit):
        self.height = 235
        self.width = 100

        self.x = xinit
        self.vel = -6

        # gap between up and down
        min_gap, max_gap = 100, 180
        self.gap = random.randint(min_gap, max_gap)
        
        # end of up piller
        min_gap_pos = height - min_gap - self.height
        max_gap_pos = self.height
        self.gap_position = random.randint(min_gap_pos, max_gap_pos)

    def move(self):
        self.x += self.vel

    def position_upper(self):
        return self.x, self.gap_position - self.height

    def position_lower(self):
        return self.x, self. gap_position + self.gap


class Bird:
    def __init__(self):
        self.size = 72

        self.alive = True
        self.moving = False

        self.x = 200
        self.y = (height - self.size) // 2

        self.vel = 0
        self.acc = 1 # pixel per frame

    def check_if_dead(self):
        def dead():
            self.alive = False
            self.moving = False

        bird_rect = bird_rect_global.move(self.x, self.y)

        if not bg_rect_global.contains(bird_rect):
            dead()

        for p in pillers:
            piller_up_rect = piller_up_rect_global.move(*p.position_upper())
            piller_down_rect = piller_down_rect_global.move(*p.position_lower())

            if bird_rect.colliderect(piller_up_rect) or bird_rect.colliderect(piller_down_rect):
                dead()

    def move_up(self):
        if not self.moving:
            self.moving = True
        self.vel = -10

    def position(self):
        if self.moving:
            self.y += self.vel
            self.vel += self.acc
            self.check_if_dead()

        return self.x, self.y

def exit():
    with open('best_score.txt', 'w') as file:
        file.write(str(best_score))
    sys.exit()

def play():
    global pillers, best_score

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    score = 0

    pillers = deque(maxlen=4)

    def append_piller():
        gap = random.randint(50, 200)
        xinit = pillers[-1].x + pillers[-1].width + gap
        piller = Piller(xinit)
        pillers.append(piller)

    pillers.append(Piller(width))
    for _ in range(3):
        append_piller()

    bird = Bird()

    while True:
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and bird.alive:
                bird.move_up()

            if (not bird.alive and event.type == pygame.MOUSEBUTTONDOWN and
                    play_again_rect.collidepoint(event.pos)):
                return
            
            if (not bird.alive and event.type == pygame.MOUSEBUTTONDOWN and
                    quit_rect.collidepoint(event.pos)):
                exit()

        for p in pillers:
            if bird.moving:
                p.move()

                if p.x + p.width < bird.x and p.x + p.width >= bird.x + p.vel:
                    score += 1
                    best_score = max(best_score, score)
            
            screen.blit(piller_up_image , p.position_upper())
            screen.blit(piller_down_image , p.position_lower())
        
        if pillers[0].x + pillers[0].width < 0:
            append_piller()
        
        screen.blit(bird_image, bird.position())

        if bird.alive and not bird.moving:
            screen.blit(hint_rendered, (111, 333))
        
        if bird.moving:
            time_now = (pygame.time.get_ticks() - start_time) // 1000
        else:
            start_time = pygame.time.get_ticks()
            if bird.alive:
                time_now = 0

        if bird.alive:
            score_rendered = font.render("SCORE : " + str(score), True, font_color)
            screen.blit(score_rendered, (5, 3))

            time_rendered = font.render("TIME : " + str(time_now), True, font_color)
            screen.blit(time_rendered, (5, 35))

        else:
            screen.blit(game_over, (0, 0))
            score_rendered = font_bigger.render(str(score), True, font_color)
            screen.blit(score_rendered, (480, 150))
            time_rendered = font_bigger.render(str(time_now) , True , font_color)
            screen.blit(time_rendered , (480 , 203))
            best_score_rendered = font_bigger.render(str(best_score), True, font_color)
            screen.blit(best_score_rendered, (480, 255))

        pygame.display.update()
        # capping framerate at 30 fps 
        clock.tick(30)

if __name__ == "__main__":
    while True:
        play()
