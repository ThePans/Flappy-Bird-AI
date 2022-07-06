import numpy
import pygame as py, sys

py.init()

class Pillar:
    def __init__(self):
        self.x = 500
        self.y1 = 0
        self.place = numpy.random.randint(25, 250)
        self.y2 = self.place + 105
        self.rect2 = py.Rect(self.x, self.y2, 75, abs(500 - self.y2))
        self.rect1 = py.Rect(self.x, self.y1, 75, self.place)
    def update(self):
        self.x -= 1
    def rects(self):
        return [py.Rect(self.x, self.y1, 50, self.place), py.Rect(self.x, self.y2, 50, abs(500 - self.y2)), 
        self.x, self.y1, self.y2, self.place]
class Floor:
    def __init__(self):
        self.x, self.x2 = 0, 285
    def update(self):
        self.x -= 1
        self.x2 -= 1
        if self.x <= -285:
            self.x = 285
        if self.x2 <= -285:
            self.x2 = 285
        return self.x, self.x2
class Game:
    def __init__(self):
        self.screen = py.display.set_mode((285, 500))
        self.clock = py.time.Clock()
        self.y = 250
        self.y_change = 0
        self.gravity = .1
        self.pillars = [Pillar()]
        self.score = 0
        self.pillar_wait = 190
        self.floor = Floor()
        py.display.set_caption('Flappy Bird')
        self.playerimages = 0
    def play_frame(self, action):
        background = py.image.load('images/background-day.png').convert()
        floor = py.image.load('images/base.png').convert()
        player_images = [py.image.load('images/redbird-downflap.png').convert(), 
        py.image.load('images/redbird-midflap.png').convert(),
        py.image.load('images/redbird-upflap.png').convert()]
        pillar_image_bottom = py.image.load('images/pipe-green.png').convert()
        pillar_image_top = py.transform.rotate(pillar_image_bottom, 180)
        my_font = py.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render('Score: {}'.format(str(self.score)), False, (0, 0, 0))
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    self.move(1)
        
        self.move(action)

        self.playerimages += .05
        if int(self.playerimages) == 3:
            self.playerimages = 0

        self.y_change += self.gravity
        self.y += self.y_change
        if self.y > 500:
            self.restart()

        player_rect = py.Rect(75, self.y, 25, 25)

        self.screen.fill((0, 0, 255))
        self.screen.blit(background, (0, 0))
        self.screen.blit(player_images[int(self.playerimages)], (73, self.y))

        self.pillar_wait -= 1
        if self.pillar_wait == 0:
            self.add_pillar()

        for pillar in self.pillars:
            pillar.update()

            pillar_list = pillar.rects()
            
            if player_rect.colliderect(pillar_list[0]):
                self.restart()
            if player_rect.colliderect(pillar_list[1]):
                self.restart()
            if 75 == pillar_list[2]:
                self.score += 1
            if pillar_list[2] < 0:
                self.pillars.remove(pillar)
        for pillars in self.pillars:
            pillar_lists = pillars.rects()
            self.screen.blit(pillar_image_bottom, (pillar_lists[2], pillar_lists[4]))
            self.screen.blit(pillar_image_top, (pillar_lists[2], pillar_lists[5] - 320))


        x, x2 = self.floor.update()

        self.screen.blit(floor, (x, 400))
        self.screen.blit(floor, (x2, 400))


        self.screen.blit(text_surface, (75,0))

        py.display.update()
        self.clock.tick(120)


    def move(self, action): 
        if action == 1:
            self.y_change = -3.5
    def add_pillar(self):
        self.pillars.append(Pillar())
        self.pillar_wait = 200
    def restart(self):
        print(self.score)
        self.pillars.clear()
        self.pillars.append(Pillar())
        self.pillar_wait = 190
        self.score = 0
        self.y = 250
        self.y_change = 0
    def ys(self):
        return self.y, self.y_change
    def close_pillar(self):
        new_pillar = []
        for pillar in self.pillars:
            p = pillar.rects()
            if p[2] >= 0:
                new_pillar.append(pillar)
        return new_pillar[0]