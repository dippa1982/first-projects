import time
import pygame
import sys
import random
from Player import player_obj
from Enemy import enemy_obj,Extra
from laser import Laser
import  Obstacle

class Game:
    def __init__(self):
        #player setup
        player_sprite = player_obj((screen_width / 2,screen_height),5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        #health & score
        self.lives = 3
        self.live_surf = pygame.image.load('Sprites/player.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.Level = 1
        self.font = pygame.font.SysFont('Ariel',24)


        #obstacle setup
        self.shape = Obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_position = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstancles(*self.obstacle_x_position,x_start = screen_width / 15 ,y_start = 480)

        #Alien setup
        self.enemy = pygame.sprite.Group()
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = random.randint(40,80)
        self.enemy_setup(rows = 2, cols = 3)
        self.enemy_direction = 1
        self.enemy_laser = pygame.sprite.Group()


    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index,row in enumerate(self.shape):
            for col_index,col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = Obstacle.Block(self.block_size,(255,0,0),x,y)
                    self.blocks.add(block)

    def create_multiple_obstancles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def enemy_setup(self,rows,cols,x_distance = 60, y_distance = 48, x_offset= 70 ,y_offset = 100):
        for row_index,row in enumerate(range(rows)):
            for col_index,col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                if row_index == 0:
                    enemy_sprite = enemy_obj('red',x,y,300)
                elif 1 <= row_index <= 2:
                    enemy_sprite = enemy_obj('green', x, y,200)
                else:
                    enemy_sprite = enemy_obj('yellow', x, y,100)
                self.enemy.add(enemy_sprite)

    def enemy_position_checker(self):
        all_enemys = self.enemy.sprites()
        for enemy in all_enemys:
            if enemy.rect.x >= screen_width - 40:
                self.enemy_direction = -1
                self.enemy_move_down(2)
            elif enemy.rect.x <= 0:
                self.enemy_direction = 1
                self.enemy_move_down(2)

    def enemy_move_down(self,distance):
        if self.enemy:
            for enemy in self.enemy.sprites():
                enemy.rect.y += distance

    def enemy_shoot(self):
        if self.enemy.sprites():
            random_enemy = random.choice(self.enemy.sprites())
            laser_sprite = Laser(random_enemy.rect.center,6,screen_height)
            self.enemy_laser.add(laser_sprite)

    def extra_enemy_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(random.choice(['right','left']),screen_width))
            self.extra_spawn_time = random.randint(400,800)

    def collison_checks(self):
        #player laser
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                #block check
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                #enemy check
                enemy_hit = pygame.sprite.spritecollide(laser,self.enemy,True)
                if enemy_hit:
                    for enemy in enemy_hit:
                        self.score += enemy.value
                    laser.kill()
                #extra check
                if pygame.sprite.spritecollide(laser,self.extra,True):
                    laser.kill()
                    self.score += 500

        if self.enemy_laser:
            for laser in self.enemy_laser:
                #block check
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                #player check
                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over()

        if self.enemy:
            for enemy in self.enemy:
                pygame.sprite.spritecollide(enemy,self.blocks,True)

                if pygame.sprite.spritecollide(enemy,self.player,False):
                    self.game_over()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf,(x,8))

    def display_score(self):
        level_surf = self.font.render(f'Level: {self.Level}', False, 'white')
        score_surf = self.font.render(f'Score: {self.score}', False, 'white')
        level_rect = score_surf.get_rect(topleft= (0, 20))
        score_rect = score_surf.get_rect(topleft = (0,0))
        screen.blit(score_surf,score_rect)
        screen.blit(level_surf, level_rect)

    def victory_message(self):
        if not self.enemy.sprites():
            victory_surf = self.font.render('You Won',False, 'white')
            victory_rect = victory_surf.get_rect(center = (screen_width / 2, screen_height / 2))
            screen.blit(victory_surf,victory_rect)
            self.level_up()

    def game_over(self):
        game_over_surf = self.font.render('GAME OVER', False, 'white')
        game_over_rect = game_over_surf.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(game_over_surf, game_over_rect)
        pygame.quit()
        sys.exit()

    def level_up(self):
        self.Level += 1
        if self.Level == 2:
            self.enemy_setup(rows= 3,cols=4)
            self.enemy
        if self.Level == 3:
            self.enemy_setup(rows=4, cols=5)
        if self.Level == 4:
            self.enemy_setup(rows=5, cols=6)
        if self.Level == 5:
            self.enemy_setup(rows=6, cols=7)
        if self.Level == 6:
            self.enemy_setup(rows=7, cols=8)


    def run(self):
        self.player.update()
        self.enemy.update(self.enemy_direction)
        self.extra.update()
        self.enemy_position_checker()
        self.collison_checks()
        self.enemy_laser.update()
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.extra_enemy_timer()
        self.blocks.draw(screen)
        self.enemy.draw(screen)
        self.extra.draw(screen)
        self.enemy_laser.draw(screen)
        self.display_lives()
        self.display_score()
        self.victory_message()

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Space invaders')
    running = True
    game = Game()
    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running == False
            if event.type == ALIENLASER:
                game.enemy_shoot()

        clock.tick(60)
        screen.fill((30, 30, 30))
        game.run()
        pygame.display.flip()

#sprites


for row in range(1, 6):
    for col in range (1,11):
        enemy = enemy_obj(screen_width / 2, 50, 5)
        enemy.rect.x = 20 + (50 * col)
        enemy.rect.y = 25 + (50 * row)
        enemy_list.add(enemy)


