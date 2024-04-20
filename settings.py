import pygame as pg
import os
pg.init()

# SCREEN
os.environ["SDL_VIDEO_CENTERED"] = '1'
screen_info = pg.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
WIDTH_S, HEIGHT_S = 700,900
FPS = 60

# ASSETS
BASE_IMG_DIR = 'images/'

#PLAYER

#PLAYERBULLET
PLAYER_BULLET_SPEED = 1
PLAYER_BULLET_LIFETIME = 10
PLAYER_BULLET_RATE = 150