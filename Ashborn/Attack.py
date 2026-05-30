
import pygame
from Util import load_and_crop
from Enemy import Enemy
class Attack(pygame.sprite.Sprite):
    def __init__(self, pos, scale_factor=3, frames2=None, frames=None, owner=None, enemy_group=None, direction="down"):
        super().__init__()

        if frames is None:
            frames = [
                'graphics/Solider/Soldier.attack1.frame1.xcf',
                'graphics/Solider/Soldier.attack1.frame2.xcf',
                'graphics/Solider/Soldier.attack1.frame3.xcf',
                'graphics/Solider/Soldier.attack1.frame4.xcf',
                'graphics/Solider/Soldier.attack1.end.xcf',
            ]

        if frames2 is None:
            frames2 = [
                'graphics/Solider/frame1.right.png',
                'graphics/Solider/frame2.right.png',
                'graphics/Solider/frame3.right.png',
                'graphics/Solider/frame4.right.png',
                'graphics/Solider/frame5.right.png',
                'graphics/Solider/frame6.right.png',
            ]

        self.frames_down = [load_and_crop(p, scale_factor=scale_factor) for p in frames]
        self.frames_right = [load_and_crop(p, scale_factor=scale_factor) for p in frames2]

        if direction == "right":
            self.frames = self.frames_right
        else:
            self.frames = self.frames_down

        self.frame_index = 0
        self.frame_delay = 4
        self.frame_timer = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)
        self.frame_index = 0
        self.frame_delay = 4  # ticks per frame
        self.frame_timer = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)
        self.owner = owner
        # increment owner's attack counter so we know player is attacking
        if self.owner is not None:
            try:
                self.owner.attack_count += 1
            except Exception:
                self.owner.attack_count = 1
        # Track which enemies have already been hit by this attack
        self.hit_enemies = set()
        self.enemy_group = enemy_group

    def collide(self):
        if self.enemy_group is None:
            return
        hits = pygame.sprite.spritecollide(self, self.enemy_group, False)  # False = don't auto-kill
        for slime in hits:
            if slime not in self.hit_enemies:
                damage = 25  # You can adjust this value for how much damage per hit
                slime.hp -= damage
                print(f"slime hit! hp = {slime.hp}")
                self.hit_enemies.add(slime)
                if slime.hp <= 0:
                    print(">>> SLIME DEFEATED <<<")
                    slime.kill()   # ✅ THIS removes hitbox + sprite




    def update(self):
        self.collide()
        # Always follow the owner's position if owner exists
        if self.owner is not None:
            self.rect.center = self.owner.rect.center

        # advance animation based on frame_delay
        self.frame_timer += 1
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                # mark owner as no longer attacking
                if self.owner is not None:
                    try:
                        self.owner.attack_count -= 1
                    except Exception:
                        self.owner.attack_count = 0
                self.kill()
                return
            self.image = self.frames[self.frame_index]
            # keep rect centered on owner's position if owner exists
            if self.owner is not None:
                self.rect = self.image.get_rect(center=self.owner.rect.center)
            else:
                center = self.rect.center
                self.rect = self.image.get_rect(center=center)
