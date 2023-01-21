import os
import sys
import pygame

INTERVAL = 50

def load_image(name, colorkey=None):
    fullname = os.path.join('data/sprites/', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class ShipChoice:
    def __init__(self, all_sprites):
        self.current_ship = None
        self.all_sprites = all_sprites
        self.listShip = {load_image("FourDeckShip.png"): 1,
                         load_image("ThreeDeckShip.png"): 2,
                         load_image("TwoDeckShip.png"): 3,
                         load_image("OneDeckShip.png"): 4}
        self.motionFlag = False
        self.start_coords = [100, 470]
        self.end_coords = [100, 600]
        self.shipView = pygame.sprite.Group()
        self.moved_item = pygame.sprite.Group()
        for img in self.listShip.keys():
            sprite = pygame.sprite.Sprite()
            sprite.image = pygame.transform.scale(img, (50, img.get_height() // 4))
            sprite.id = img
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = self.end_coords[0]
            sprite.rect.y = self.start_coords[1]
            self.all_sprites.add(sprite)
            self.shipView.add(sprite)
            self.end_coords[0] += sprite.rect.width + INTERVAL

    def get_motion_flag(self):
        return self.motionFlag

    def create_sprite(self, img):
        sprite = pygame.sprite.Sprite()
        sprite.image = img
        sprite.rect = sprite.image.get_rect()
        self.all_sprites.add(sprite)
        return sprite

    def start_motion(self, sp):
        for sprite in self.shipView.sprites():
            if sprite.rect.collidepoint(sp):
                self.motionFlag = True
                self.current_ship = self.create_sprite(sprite.image)
                self.current_ship.rect.x = sp[0] - 25
                self.current_ship.rect.y = sp[1]
                self.listShip[sprite.id] -= 1
                if self.listShip[sprite.id] <= 0:
                    self.shipView.remove(sprite)
                    self.all_sprites.remove(sprite)
                    self.update_position()
                break
        for sprite in self.moved_item.sprites():
            if sprite.rect.collidepoint(sp):
                self.moved_item.remove(self.current_ship)
                self.motionFlag = True
                self.current_ship = sprite
                self.current_ship.rect.x = sp[0] - 25
                self.current_ship.rect.y = sp[1]

    def motion(self, pos):
        self.current_ship.rect = self.current_ship.rect.move(pos)

    def stop_motion(self, sp, check_strike, set_ship):
        self.moved_item.add(self.current_ship)
        self.motionFlag = False
        if check_strike(sp[0], sp[1]):
            self.current_ship.rect.x, self.current_ship.rect.y = set_ship(sp[0], sp[1])

    def update_position(self):
        x = 100
        for sprite in self.shipView.sprites():
            sprite.rect.x = x
            sprite.rect.y = self.y
            x += sprite.rect.width + INTERVAL
        self.end_coords[0] = x
