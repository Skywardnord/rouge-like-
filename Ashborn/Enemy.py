from Util import load_and_crop
import pygame    
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_and_crop('graphics/Slime.xcf', scale_factor=2.5)
        self.rect = self.image.get_rect()
        # place enemy on-screen (was off-screen at 1900,1100)
        self.rect.center = (600, 350)
        self.x = self.rect.x
        self.y = self.rect.y
        print(f"Slime spawned at position: x={self.x}, y={self.y}")

        slime_hp = 100
        self.hp = slime_hp
        if slime_hp <= 0:
            print(">>> SLIME DEFEATED <<<")
            self.kill()
            self.rect
    def update(self):
        # Update position tracking if slime moves
        if self.x != self.rect.x or self.y != self.rect.y:
            self.x = self.rect.x
            self.y = self.rect.y
            print(f"Slime moved to: x={self.x}, y={self.y}")