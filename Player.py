import pygame
from laser import Laser

class player_obj(pygame.sprite.Sprite):
    def __init__(self,pos,speed):
        super().__init__()
        self.image = pygame.image.load('Sprites/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.ready = True
        self.max_x_constraint = 600
        self.laser_cooldown = 800
        self.lasers = pygame.sprite.Group()

    def draw(self,screen):
        screen.blit(self.image,self.rect)

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center,-8,self.rect.bottom))

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()



