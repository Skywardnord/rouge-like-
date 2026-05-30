import pygame
import time
import os
from Enemy import Enemy
from Util import load_and_crop
from Attack import Attack
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
# sprites 



last_attack_time = 0  # Global variable to track last attack time
def attack():
    global last_attack_time
    attk_speed = 0.5
    now = time.time()

    if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
        if now - last_attack_time >= attk_speed:
            atk = Attack(
                player_sprite.rect.center,
                scale_factor=4,
                owner=player_sprite,
                enemy_group=enemy,
                direction="down"
            )
            attack_group.add(atk)
            last_attack_time = now

    if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
        if now - last_attack_time >= attk_speed:
            atk = Attack(
                player_sprite.rect.center,
                scale_factor=4,
                owner=player_sprite,
                enemy_group=enemy,
                direction="right"
            )
            attack_group.add(atk)
            last_attack_time = now


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, scale_factor=4, frames2 =None,frames=None, owner=None, enemy_group=None):
        super().__init__()
        
     

        self.walk_down_sheet = 'graphics/Solider/Walk_Down.xcf'
        
        # Load idle image
        self.idle_image = load_and_crop('graphics/Solider/Soldier.xcf', scale_factor=4)

        # If frames are provided, use them for animation, else use idle image
        if frames:
            self.frames = [load_and_crop(p, scale_factor=scale_factor) for p in frames]
        else:
            self.frames = [self.idle_image]
        if frames2:
            self.frames2 = [load_and_crop(p, scale_factor=scale_factor) for p in frames2]
        else:
            self.frames2 = [self.idle_image]

        # For walking animation, use frames or fallback to idle
        self.walk_frames = self.frames if frames else [self.idle_image]
        self.frame2_index = 0
        self.frame_index = 0
        self.frame_delay = 4  # ticks per frame
        self.frame_timer = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)
        self.owner = owner
        self.enemy_group = enemy_group
        self.attack_count = 0

        self.rect = self.image.get_rect()
        self.rect.center = (640, 360)
        self.speed = 6.5
        self.x = self.rect.x
        self.y = self.rect.y
        self.is_walking = False
        self.hitbox = pygame.Rect(0, 0, 35, 60)  # Adjust width/height to your character's body
        self.hitbox.center = self.rect.center
        print(f"Player spawned at position: x={self.x}, y={self.y}")        
        print(f"Player image size: {self.image.get_size()}")
        print(f"Player rect: {self.rect}")
        print(f"Player hitbox: {self.hitbox}")
    
    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        return image
    def walk_down(self, sheet, frame, width, height, scale, color):
        image = load_and_crop(sheet, frame, width, height, scale, color)
        self.walk_down = pygame
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.y = self.rect.y
            
        
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.x = self.rect.x
           
        if keys[pygame.K_s]:
            self.frame_timer += 1
            
            self.rect.y += self.speed
            self.y = self.rect.y
            self.is_walking = True
        
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.x = self.rect.x
        
               # --- ANIMATION ---
        if keys[pygame.K_s]:

            if self.frame_timer >= self.frame_delay:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames)

            self.image = self.walk_frames[self.frame_index]

        else:
            # Reset when S is NOT pressed
            self.frame_index = 0
            self.frame_timer = 0
            self.image = self.idle_image


        self.hitbox.center = self.rect.center
        # Sync hitbox to player position after movement (offset up 15 pixels)
        self.hitbox.center = (self.rect.centerx, self.rect.centery - 0)

# functions

def collision_sprite():
    for slime in enemy:
        if player_sprite.hitbox.colliderect(slime.rect):
            print("COLLISION DETECTED! Player hit enemy")
            return True
    return False

# variables

player_sprite = Player((640, 360))
player = pygame.sprite.GroupSingle(player_sprite)

enemy_sprite = Enemy()

enemy = pygame.sprite.Group(enemy_sprite)


attack_group = pygame.sprite.Group()

player_hp = 100


tile = pygame.image.load('graphics/tile.png').convert_alpha()
tile = pygame.transform.scale(tile, (tile.get_width() * 16, tile.get_height() * 11))
# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        attack()
       
       
    
   
    screen.fill((0, 0, 0))
    screen.blit(tile, (-500, -400))
    player_sprite.update()
        
    # Check for collisions
    hit = collision_sprite()
    if hit:
        print(">>> COLLISION HIT PLAYER <<<")
        player_hp -= 0 # Example: reduce player HP by 10 on collision
        # You can add game over logic here, like stopping or taking damage
    if player_hp <= 0:
        print(">>> GAME OVER <<<")
        running = False  
   
    if getattr(player_sprite, 'attack_count', 0) == 0:
        screen.blit(player_sprite.image, player_sprite.rect)
    # Draw player hitbox outline (yellow) for visual adjustment
    #pygame.draw.rect(screen, (255, 255, 0), player_sprite.hitbox, 2)
    # update enemies, then draw them
    enemy.update()
    enemy.draw(screen)
    attack_group.update()
    attack_group.draw(screen)
    pygame.display.flip()
    clock.tick(60)