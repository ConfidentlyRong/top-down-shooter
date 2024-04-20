import pygame as pg
import os
from settings import *

pg.init()
fake_screen = pg.display.set_mode((WIDTH,HEIGHT))

def load_image(path):
    img = pg.image.load(BASE_IMG_DIR + path).convert()
    img.set_colorkey(('white'))
    return img

def load_images(path):
    images = []
    for img_name in os.listdir(BASE_IMG_DIR + path):
        images.append(load_image(path + '/' + img_name))
    return images

ASSETS_DICT = {
    'player_ship': load_image('player/player_ship.png'),
    'stone': load_images('tiles/stone'),
    'grass': load_images('tiles/grass'),
}