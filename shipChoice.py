import os
import sys
import pygame

INTERVAL = 50
MARGIN_LEFT = 100


def load_image(name, colorkey=None):
    fullname = os.path.join('data/sprites/', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class ShipChoice:
    def __init__(self, all_sprites, top):
        self.current_ship = None
        self.all_sprites = all_sprites
        self.listShip = {load_image("FourDeckShip2.png"): [1, 4],
                         load_image("ThreeDeckShip2.png"): [2, 3],
                         load_image("TwoDeckShip2.png"): [3, 2],
                         load_image("OneDeckShip2.png"): [4, 1]}
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.motionFlag = False
        self.start_coords = [MARGIN_LEFT, top]
        self.end_coords = [MARGIN_LEFT, top]
        self.shipView = pygame.sprite.Group()
        self.moved_item = pygame.sprite.Group()
        for img in self.listShip.keys():
            sprite = pygame.sprite.Sprite()
            sprite.image = img
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = self.end_coords[0]
            sprite.rect.y = self.start_coords[1]
            sprite.text = self.font.render(str(self.listShip[img][0]), True, (255, 0, 0))
            sprite.text_coord = (sprite.rect.x + 15, sprite.rect.y + sprite.image.get_height() + 5)
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

    def start_motion(self, sp, del_ship):
        for sprite in self.shipView.sprites():
            if sprite.rect.collidepoint(sp):
                self.motionFlag = True
                self.current_ship = self.create_sprite(sprite.image)
                self.current_ship.rect.x = sp[0] - 25
                self.current_ship.rect.y = sp[1]
                self.listShip[sprite.image][0] -= 1
                if self.listShip[sprite.image][0] <= 0:
                    self.shipView.remove(sprite)
                    self.all_sprites.remove(sprite)
                    self.update_position()
                break
        for sprite in self.moved_item.sprites():
            if sprite.rect.collidepoint(sp):
                self.moved_item.remove(self.current_ship)
                self.motionFlag = True
                self.current_ship = sprite
                del_ship(sp[0], sp[1], self.listShip[self.current_ship.image][1])
                self.current_ship.rect.x = sp[0] - 25
                self.current_ship.rect.y = sp[1]

    def motion(self, pos):
        self.current_ship.rect = self.current_ship.rect.move(pos)

    def stop_motion(self, sp, check_strike, set_ship, check_collision_ship):
        self.motionFlag = False
        if check_strike(sp[0], sp[1]) and check_collision_ship(sp[0], sp[1]):
            self.current_ship.rect.x, self.current_ship.rect.y = \
                set_ship(sp[0], sp[1], self.listShip[self.current_ship.image][1])
            self.moved_item.add(self.current_ship)
            self.update_position()
        else:
            if self.listShip[self.current_ship.image][0] <= 0:
                self.shipView.add(self.current_ship)
            else:
                self.current_ship.kill()
            self.listShip[self.current_ship.image][0] += 1
            self.update_position()

    def update_position(self):
        x = self.start_coords[0]
        for sprite in self.shipView.sprites():
            sprite.rect.x = x
            sprite.rect.y = self.start_coords[1]
            sprite.text_coord = (sprite.rect.x + 15, sprite.rect.y + sprite.image.get_height() + 5)
            sprite.text = self.font.render(str(self.listShip[sprite.image][0]), True, (255, 0, 0))
            x += sprite.rect.width + INTERVAL
        self.end_coords[0] = x

    def render(self, screen):
        for sprite in self.shipView.sprites():
            screen.blit(sprite.text, sprite.text_coord)
