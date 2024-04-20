import pygame as pg
import sys
from settings import *
from engine.sprites import Player, Mob
from engine.assets import ASSETS_DICT
from engine.tilemap import Tilemap

class Game:
    def __init__(self):
        self.load_data()
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        self.clock = pg.time.Clock()
        self.mob_num = -1
        self.player_bullets_num = -1
        self.player_bullet_trash = []
        self.mob_trash = []
        self.scroll = [0,0]
        

    def load_data(self):
        self.assets = ASSETS_DICT
        print(self.assets)
        self.font_name = pg.font.match_font('Copyduck')

    def lvl_one(self):
        self.tilemap = Tilemap(self, tile_size=32)
        self.mobs = {}
        self.player_bullets = {}
        self.player = Player(self, (15,5))
        self.mob = Mob(self, (15,10))
        self.mobs.update({'i' + str(self.mob_num): self.mob})
        self.run()

    def run(self):
        while True:
            self.dt = self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.player.shoot()
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    sys.exit()
                if event.key == pg.K_a:
                    self.player.move_left = True
                if event.key == pg.K_d:
                    self.player.move_right = True
                if event.key == pg.K_w:
                    self.player.move_up = True
                if event.key == pg.K_s:
                    self.player.move_down = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_a:
                    self.player.move_left = False
                if event.key == pg.K_d:
                    self.player.move_right = False
                if event.key == pg.K_w:
                    self.player.move_up = False
                if event.key == pg.K_s:
                    self.player.move_down = False
    
    def update(self):
        self.scroll[0] += (self.player.collide_rect.centerx - self.screen.get_width() / 2 - self.scroll[0]) / 15
        self.scroll[1] += (self.player.collide_rect.centery - self.screen.get_height() / 2 - self.scroll[1]) / 15
        self.mpos = list(pg.mouse.get_pos())
        self.mpos[0] += self.scroll[0]
        self.mpos[1] += self.scroll[1]
        self.player.update(self.tilemap)
        self.update_objects(self.player_bullets, self.player_bullet_trash)
        self.update_objects(self.mobs, self.mob_trash)

    def update_objects(self, objects, trash):
        for object in objects.values():
            object.update()
        for key, value in objects.items():
            if value.life <= 0:
                trash.append(key)
        if trash:
            for object in trash:
                if object in objects.keys():
                    del objects[object]
            del trash[:]    

    def draw(self):
        self.screen.fill(('black'))
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.tilemap.render(self.screen, offset=self.scroll)
        for mob in self.mobs.values():
            mob.render(self.screen, offset=self.scroll)
        self.player.render(self.screen, offset=self.scroll)
        for bullet in self.player_bullets.values():
            bullet.render(self.screen, offset=self.scroll)
        pg.display.flip()

    def draw_text(self, surf, text, size, color, pos):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = pos
        surf.blit(text_surface, text_rect)

    def main_menu(self):
        waiting = True
        while waiting:
            self.dt = self.clock.tick(FPS)
            self.screen.fill(('grey'))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        sys.exit()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        waiting = False
            self.draw_text(self.screen, "Main Menu", 88, ('white'), (WIDTH/2, HEIGHT * 0.10))
            pg.display.flip()


if __name__ == '__main__':
    game = Game()
    game.main_menu()
    game.lvl_one()
            