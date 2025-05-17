#Создай собственный Шутер!
from pygame import *
from random import randint
from time import sleep
import random
font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 120)
text_win = font2.render('Победа', 1, (255, 255, 255))
text_unwin = font2.render('Поражение', 1, (255, 255, 255))
lost = 0
kill = 0
window = display.set_mode((700, 500))
display.set_caption('Звездные воины')
window.fill((81, 0, 139))
clock = time.Clock()
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
game_run = True
window.blit(background, (0, 0))
speed = randint(2, 6)
bullet_speed = 10
random_x = randint(65, 635)
class Game_sprite_class(sprite.Sprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__()
        self.image = transform.scale(image.load(filename), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_parrying = False
        self.parry_duration = 30  # Длительность парирования в кадрах
        self.parry_timer = 0
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player_class(Game_sprite_class):
    def __init__(self, filename, w, h, speed, x, y, health=100):
        super().__init__(filename, w, h, speed, x, y)
        self.health = health
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= 8
        if keys_pressed[K_d] and self.rect.x < 630:
            self.rect.x += 8
        if self.is_parrying:
            self.parry_timer -= 1
            if self.parry_timer <= 0:
                self.is_parrying = False
    def parry(self):
        if not self.is_parrying:
            self.is_parrying = True
            self.parry_timer = self.parry_duration
    def fire(self):
        bullet = Bullet_class('bullet.png', 10, 20, 10, self.rect.centerx, self.rect.top)
        bullets.add(bullet)
    def apply_buff(self, buff):
        if buff.type == "health":
            self.health += buff.value
        elif buff.type == "bullet_boost":
            bullet_boost = True
    def remove_buff(self, buff):
        if buff.type == "health":
            self.speed -= buff.value
        elif buff.type == "bullet_boost":
            bullet_boost = False



class Enemy_class(Game_sprite_class):
    def __init__(self, filename, w, h, speed, x, y, damage=25):
        super().__init__(filename, w, h, speed, x, y)
        self.last_shot_time = time.get_ticks()
        self.shoot_interval = 3000
        self.damage = damage
    def shoot(self):
        current_time = time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_interval:
            self.last_shot_time = current_time
            bullet_enemy = Bullet_enemys_class('bullet.png', 10, 20, bullet_speed, self.rect.centerx, self.rect.bottom)
            bullets_enemy.add(bullet_enemy)
    def update(self):
        global random_x
        global lost
        global pr
        self.rect.y += self.speed
        if self.rect.y >= 500:
            lost += 1
            self.rect.y = -50
            self.rect.x = random_x
            self.speed = randint(2, 6)
            random_x = randint(65, 635)
class Bullet_class(Game_sprite_class):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
class Bullet_enemys_class(Game_sprite_class):
    def __init__(self, filename, w, h, speed, x, y, dmg=25):
        super().__init__(filename, w, h, speed, x, y)
        self.damage = dmg
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 510:
            self.kill()
#class Buff(Game_sprite_class):
#    def __init__(self, x, y, duration, filename, w, h, speed, typee):
#        super().__init__(filename, w, h, speed, x, y)
#        self.duration = duration
#        self.start_time = time.get_ticks()
#        self.active = True
#        self.typee = typee
#    def update(self):
#        if time.get_ticks() - self.start_time > self.duration:
#            self.active = False
#            self.kill()
buffs = sprite.Group()
bullets = sprite.Group()
bullets_enemy = sprite.Group()
enemy1 = Enemy_class('ufo.png', 65, 35, speed, random_x, -50)
random_x = randint(65, 635)
enemy2 = Enemy_class('ufo.png', 65, 35, speed, random_x, -50)
random_x = randint(65, 635)
enemy3 = Enemy_class('ufo.png', 65, 35, speed, random_x, -50)
random_x = randint(65, 635)
enemy4 = Enemy_class('ufo.png', 65, 35, speed, random_x, -50)
random_x = randint(65, 635)
enemy5 = Enemy_class('ufo.png', 65, 35, speed, random_x, -50)
random_x = randint(65, 635)
enemies = sprite.Group()
enemies.add(enemy1, enemy2, enemy3, enemy4, enemy5)
player = Player_class('rocket.png', 65, 65, 10, 320, 400)
button = Game_sprite_class('йцукенгшщ.png', 200, 60, 0, 250, 150)
menu = True
game_finish = False
while game_run:
    if menu:
        background = transform.scale(image.load('images (5).jfif'), (700, 500))
        window.blit(background, (0, 0))
        button.reset()
        for e in event.get():
            if e.type == QUIT:
                game_run = False
            if e.type == MOUSEBUTTONDOWN:
                x, y = e.pos
                if button.rect.collidepoint(x, y):
                    #нарисовать кнопки выбора сложности
                if eazy_button.rect.collidepoint(x, y):
                    speed = randint(1, 2)
                    player.health = 200
                    bullet_speed = 4
                    menu = False
                    background = transform.scale(image.load('galaxy.jpg'), (700, 500))
                if medium_button.rect.collidepoint(x, y):
                    speed = randint(2, 4)
                    player.health = 100
                    bullet_speed = 7
                    menu = False
                    background = transform.scale(image.load('galaxy.jpg'), (700, 500))
                if hard_buttom.rect.collidepoint(x, y):
                    speed = randint(4, 7)
                    player.health = 100
                    bullet_speed = 10
                    menu = False
                    background = transform.scale(image.load('galaxy.jpg'), (700, 500))
    if not game_finish and not menu:
        window.blit(background, (0, 0))
        player.reset()
        player.update()
        enemies.draw(window)
        enemies.update()
        bullets.draw(window)
        bullets.update()
        bullets_enemy.draw(window)
        bullets_enemy.update()
        buffs.update()
        buffs.draw(window)
        sprites_list_for_bullets = sprite.groupcollide(enemies, bullets, True, True)
        for i in sprites_list_for_bullets:
            kill += 1
            #if random.randint(0, 1) < 0.70:  # Случайное условие для создания баффа
            #    if random.randint(1, 2) <= 1:
            #        typee = 'health'
            #    if random.randint(1, 2) > 1:
            #        typee = 'bullet_boost'
            #    buffs.add(Buff(random.randint(0, 780), random.randint(0, 580), 5000, 'buff_health.png', 200, 60, 10, typee))  
            #    print(f'Создан {typee}')
            random_x = randint(65, 635)
            enemy1 = Enemy_class('ufo.png', 65, 35, speed, random_x, -50)
            enemies.add(enemy1)
        for i in enemies:
            i.shoot()
        sprites_list_ship = sprite.spritecollide(player, enemies, False)
        sprites_list_ship__ = sprite.spritecollide(player, bullets_enemy, True)
        for i in sprites_list_ship__:
            #парирование пуль
            if not player.is_parrying:
                player.health -= i.damage  # Игрок получает урон
                print(f"Player Health: {player.health}")
                bullet_enemy = Bullet_enemys_class('bullet.png', 10, 20, bullet_speed, enemy1.rect.centerx, enemy1.rect.bottom)
                bullets_enemy.add(bullet_enemy)
            else:
                print("Attack parried!")
                #if time.get_ticks() - time_text_parry < 1000:
                bullet_enemy = Bullet_enemys_class('bullet.png', 10, 20, bullet_speed, enemy1.rect.centerx, enemy1.rect.bottom)
                bullets_enemy.add(bullet_enemy)
                player.health = 100
                player.fire()
        if kill >= 20:
            game_finish = True
            window.blit(text_win, (190, 120))
        if lost >= 10:
            game_finish = True
            window.blit(text_unwin, (140, 120))
        if player.health <= 0:
            game_finish = True
            window.blit(text_unwin, (140, 120))
        text_lose = font1.render('Пропущенно: ' + str(lost), 1, (255, 255, 255))
        text_kill = font1.render('Счет:' + str(kill), 1, (255, 255, 255))
        text_health = font1.render('Здоровье:' + str(player.health), 1, (255, 255, 255))
        window.blit(text_lose, (50, 50))
        window.blit(text_kill, (50, 20))
        window.blit(text_health, (50, 80))
        for e in event.get():
            if e.type == QUIT:
                game_run = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    player.fire()
                if e.key == K_f:
                    player.parry()

        player.update()
        #проверка парирования
        if sprite.spritecollide(player, enemies, True):#парирование кораблей
            if not player.is_parrying:
                player.health -= enemy1.damage  # Игрок получает урон
                print(f"Player Health: {player.health}")
                enemy1 = Enemy_class('ufo.png', 65, 35, speed, random_x, -50)
                enemies.add(enemy1)
            else:
                print("Attack parried!")
                #text_parry = font1.render('+ parry', 1, (225, 255, 255))
                #window.blit(text_parry, (600, 50))
                #print('закреплено')
                #time_text_parry = time.get_ticks()
                enemy1 = Enemy_class('ufo.png', 65, 35, speed, random_x, -50)
                enemies.add(enemy1)
                player.health = 100
                kill += 1
        #скорее всего не пригодится
        #if sprite.spritecollide(player, bullets_enemy, True):#парирование пуль
            #if not player.is_parrying:
                #player.health -= bullet.damage  # Игрок получает урон
                #print(f"Player Health: {player.health}")
                #bullet_enemy = Bullet_enemys_class('bullet.png', 10, 20, 10, enemy1.rect.centerx, enemy1.rect.bottom)
                #bullets_enemy.add(bullet_enemy)
            #else:
                #print("Attack parried!")
                #bullet_enemy = Bullet_enemys_class('bullet.png', 10, 20, 10, enemy1.rect.centerx, enemy1.rect.bottom)
                ##bullets_enemy.add(bullet_enemy)
    if game_finish == True and menu == False:
        for e in event.get():
            if e.type == QUIT:
                game_run = False
    clock.tick(60)
    display.update()