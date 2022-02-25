import pygame
from settings import *
import sched, time
from support import import_folder




class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack):
        super().__init__(groups)
        self.image = pygame.image.load('images/obstacles/gold1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -26)
    
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15 
    
        self.direction = pygame.math.Vector2()
        self.speed = 5  
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.create_attack = create_attack
 
        self.obstacle_sprites = obstacle_sprites
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        print(self.weapon)

    def import_player_assets(self):
        character_path = 'graphics/graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 
        'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [], 
        'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        
        for animation in self.animations.keys():
             full_path = character_path + animation
             self.animations[animation] = import_folder(full_path)


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
            self.image = pygame.image.load('images/obstacles/gold16.png').convert_alpha()
        elif keys[pygame.K_DOWN]:
            self.status = 'down'

            self.direction.y = 1
            self.image = pygame.image.load('images/obstacles/gold3.png').convert_alpha()


        else:
            self.direction.y = 0


        if keys[pygame.K_RIGHT]:
            self.status = 'right'
            self.direction.x = 1
            self.image = pygame.image.load('images/obstacles/gold5.png').convert_alpha()

        elif keys[pygame.K_LEFT]:
            self.status = 'left'
            self.direction.x = -1
            self.image = pygame.image.load('images/obstacles/gold4.png').convert_alpha()
        else: 
            self.direction.x = 0

        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack

        if keys[pygame.K_LCTRL] and not  self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')



    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('verticle')
        self.rect.center = self.hitbox.center

        #self.rect.center += self.direction * speed

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'verticle':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)


    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)

