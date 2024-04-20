import pygame as pg
import os
from settings import *
vec = pg.math.Vector2

class Player:
    def __init__(self, game, pos):
        self.game = game
        self.image_orig = self.game.assets['player_ship']
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.collide_rect = pg.Rect(0,0,16,16)
        self.collide_rect.center = self.rect.center
        self.pos = vec(pos) * 32
        self.acc = vec(0,0)
        self.vel = vec(0,0)
        self.rect.center = self.pos
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.rot = 0
    
    def load_data(self):
        pass

    def check_events(self):
        self.rot = (self.game.mpos - self.pos).angle_to(vec(1,0))
        new_image = pg.transform.rotate(self.image_orig,self.rot)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.acc = vec(0,0)
        if self.move_right:
            self.acc.x = 0.002
        if self.move_left:
            self.acc.x = -0.002
        if self.move_up:
            self.acc.y = -0.002
        if self.move_down:
            self.acc.y = 0.002
        self.acc += self.vel * -0.006
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt

    def shoot(self):
        dir = vec(1,0).rotate(-self.rot)
        bullet = PlayerBullet(self.game, self.rect.center, dir)
        self.game.player_bullets.update({'b' + str(self.game.player_bullets_num): bullet})
        self.game.player_bullets_num += 1

    def collide_with_tiles(self, dir, tilemap):
        if dir == 'x':
            for rect in tilemap.physics_rects_around(self.pos):
                if self.collide_rect.colliderect(rect):
                    if self.vel.x > 0:
                        self.collide_rect.right = rect.left
                    if self.vel.x < 0:
                        self.collide_rect.left = rect.right
                    self.pos.x = self.collide_rect.x
        if dir == 'y':
            for rect in tilemap.physics_rects_around(self.pos):
                if self.collide_rect.colliderect(rect):
                    if self.vel.y > 0:
                        self.collide_rect.bottom = rect.top
                    if self.vel.y < 0:
                        self.collide_rect.top = rect.bottom
                    self.pos.y = self.collide_rect.y

    def update(self, tilemap):
        self.check_events()
        self.collide_rect.x = self.pos.x
        self.collide_with_tiles('x', tilemap)
        self.collide_rect.y = self.pos.y
        self.collide_with_tiles('y', tilemap)
        self.rect.center = self.collide_rect.center

    def render(self, surf, offset=(0,0)):
        surf.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))

class PlayerBullet:
    def __init__(self, game, pos, dir):
        self.game = game
        self.image = pg.Surface((4,4))
        self.image.fill(('red'))
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.vel = dir * PLAYER_BULLET_SPEED
        self.life = 80

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        self.life -= 1

    def render(self, surf, offset=(0,0)):
        surf.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))


class Mob:
    def __init__(self, game, pos):
        self.game = game
        self.image = pg.Surface((40,40))
        self.image.fill(('red'))
        self.rect = self.image.get_rect()
        self.pos = vec(pos) * 32
        self.rect.center = self.pos
        self.life = 100

    def collide_player_bullet(self):
        for bullet in self.game.player_bullets.values():
            if self.rect.colliderect(bullet.rect):
                self.life -= 20

    def update(self):
        self.collide_player_bullet()

    def render(self, surf, offset=(0,0)):
        surf.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))