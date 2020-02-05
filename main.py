import pygame as pg
import random
import time
from numpy import exp, array, random, dot

class YapaySinirAglariCKA():
    
    def __init__(self):
        # rastgele sayı
        random.seed(1)

        # 3 giriş 1 çıkıþlı YSA
        # -1'den 1'e rastgele ağırlık değerleri
        self.agirliklar = 2 * random.random((2, 1)) - 1

    # Sigmoid aktivasyon fonksiyonu
    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))

    # Sigmoid aktivasyon fonksiyonunun türevi
    def __sigmoid_turev(self, x):
        return x * (1 - x)

    # Eğitim - training aşaması
    def egit_beni(self, egitim_girisler, egitim_cikislar, toplam_iterasyon):
        for iterasyon in range(toplam_iterasyon):
            cikis = self.besle(egitim_girisler)
            print(" iterasyon (döngü, eğitim) = ",iterasyon)
            # Hata hesabı...
            hata = egitim_cikislar - cikis

            # Ağırlık ayar değeri
            ayar = dot(egitim_girisler.T, hata * self.__sigmoid_turev(cikis))

            # Ağırlıkları ayarlama...
            self.agirliklar += ayar

    # İleri besleme/test/uyg.
    def besle(self, giris):
        return self.__sigmoid(dot(giris, self.agirliklar))



if __name__ == "__main__":

    #YSA kurulumu...
    ysa = YapaySinirAglariCKA()

    # Eğitim seti...
    egitim_girisler = array([[1,0.95],[0.2,0.3],[0.5,0.5],[0.30,0.50],[0.60,0.80],[0.1,0.1],[0.9,0.5],[0.4,0.8],[1,0.3],[0.9,0.5]])
    egitim_cikislar = array([[1, 0.22, 0.48, 0.38, 0.68, 0.08, 0.6, 0.54, 0.44,0.65]]).T

    # İlgili iterasyon değeri kadar eğitim
    ysa.egit_beni(egitim_girisler, egitim_cikislar, 300000)


    # Test aşaması

def beslee(can,mermi):
    print((ysa.besle(array([can, mermi])))*100)
    return ysa.besle(array([can, mermi]))


kontrol = 3
sa = 0

pg.init()
a = pg.mixer.music.load("Game/Bullet ricochet 01.mp3")
font = pg.font.SysFont("Helvetica",30)
screenX = 1008
screenY = 689
win = pg.display.set_mode((screenX, screenY))
win.blit(pg.image.load('Game/as.jpg'), (0, 88))
pg.display.update()
while True:
    pressed = False
    for event in pg.event.get():
        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                pressed = True
                break
    if pressed == True:
        break

bg = pg.image.load('Game/bg1.jpg')
pg.display.set_caption('Test Game')
clock = pg.time.Clock()


class Base(pg.sprite.Sprite):

    def __init__(self, image, speed, location: tuple):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.x, self.y = location


class Player(Base):

    def __init__(self, image, speed, location, jc):
        Base.__init__(self, image, speed, location)
        self.jumping = False
        self.JumpCounter = jc
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.rate = 27
        self.rateCounter = 0
        self.LastDirection = 0
        self.LastDirection2 = 0
        self.health = 100

    def move(self):
        global screenX
        global screenY
        global x
        global y
        if self.rateCounter + 1 >= 27:
            self.rateCounter = 0
        if self.right and self.rect.right + self.speed < screenX:
            self.x += self.speed
            self.image = pg.image.load(f'Game/R{(self.rateCounter // 3) + 1}.png')
            self.rateCounter += 1
        elif self.left and self.rect.left - self.speed > 0:
            self.x -= self.speed
            self.image = pg.image.load(f'Game/L{(self.rateCounter // 3) + 1}.png')
            self.rateCounter += 1
        elif self.up and self.rect.top - self.speed > 0:
            self.y -= self.speed
            self.image = pg.image.load('Game/standing.png')
            self.rateCounter += 1
        elif self.down and self.rect.bottom + self.speed < screenY:
            self.y += self.speed
            self.image = pg.image.load('Game/standing.png')
            self.rateCounter += 1
        else:
            if self.LastDirection == 1:
                self.image = pg.image.load('Game/R1.png')
            elif self.LastDirection == -1:
                self.image = pg.image.load('Game/L1.png')
            else:
                self.image = pg.image.load('Game/standing.png')
        if self.jumping:
            neg = 1
            if self.JumpCounter < 0:
                neg = -1
            if self.JumpCounter >= -7:
                self.y -= int(self.JumpCounter ** 2 * neg)
                self.JumpCounter -= 1
            else:
                self.JumpCounter = 7
                self.jumping = False

    def update(self):
        self.rect.x, self.rect.y = self.x, self.y
    def kill(self):
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.jumping = False
    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Enemy(pg.sprite.Sprite):
    def __init__(self, image, location, health, ammo, speed, bullets):
        Base.__init__(self, image, speed, location)
        self.rect = self.image.get_rect()
        self.x, self.y = location
        self.health = health
        self.ammo = ammo
        self.decision = beslee(self.health/100, self.ammo/100)
        self.decision *= 100
        self.rate = 27
        self.rateCounter = 0
        self.sayi = random.randint(100,400)
        self.uzaklik_x = 175+self.sayi
        self.counter = 0
        self.bullets = bullets
        self.LastDirection = 0
        self.firerate = 0
        self.oldtime = int(time.time())


    def update(self, playerpos, neg):
        if self.rateCounter +1 >= self.rate:
            self.rateCounter = 0
        global screenX
        global screenY
        
        if self.counter == self.firerate:
            self.counter = 0
        self.decision = beslee(self.health/100, self.ammo/100)
        self.decision *= 100 
        self.sayi = random.randint(100,400)
        
        if 80 <= self.decision <88 and self.counter == 0:
            self.uzaklik_x = 30+self.sayi
            self.firerate = 10
            self.asdd = 0
        if 72 <= self.decision <= 80 and self.counter == 0:
            self.uzaklik_x = 100+self.sayi
            self.firerate = 15
            self.asdd= 1
        if 64 <= self.decision <= 72 and self.counter == 0:
            self.uzaklik_x = 300+self.sayi
            self.firerate = 20
            self.asdd = 2
        if 1 <= self.decision <= 64 and self.counter == 0:
            self.uzaklik_x = 350+self.sayi
            self.firerate = 25
            self.asdd = 3

        if 50 <= self.decision <= 70:          
            self.speed = 4
        if 40 <= self.decision < 50:
            self.speed = 3
        if 1 <= self.decision < 40:
            self.speed = 2
            
        if abs(playerpos[0] - self.x) >= self.uzaklik_x: 

            if self.x<=952:

                if playerpos[0] >= self.x and self.x + self.speed < screenX:
                    self.x += self.speed
                    self.image = pg.image.load(f'Game/R{(self.rateCounter // 3) + 1}E.png')
                    self.rateCounter += 1
                    self.LastDirection = 1
            
            if self.x>=3:

                if playerpos[0] <= self.x and self.x - self.speed > 0:
                    self.x -= self.speed
                    self.LastDirection = -1
                    self.image = pg.image.load(f'Game/L{(self.rateCounter // 3) + 1}E.png')
                    self.rateCounter += 1
        
        elif abs(playerpos[0] - self.x) <= self.uzaklik_x and abs(playerpos[0] - self.x) <= self.uzaklik_x -50:

            if self.x>=3 and self.x<=952:

                if neg == -1 and self.x - self.speed > 0:
                    self.x += self.speed * neg
                    self.image = pg.image.load(f'Game/L{(self.rateCounter // 3) + 1}E.png')
                    self.LastDirection = 1
                    self.rateCounter +=1
           

                elif  neg == 1 and self.x + self.speed < screenX:
                    self.x += self.speed * neg
                    self.image = pg.image.load(f'Game/R{(self.rateCounter // 3) + 1}E.png')
                    self.LastDirection = -1
                    self.rateCounter += 1


        if abs(playerpos[1] - self.y) >= self.uzaklik_x:

            if self.y <= 620:

                if playerpos[1] >= self.y and self.y + self.speed < screenY:
                    self.y += self.speed

            if self.y >= 3:

                if playerpos[1] <= self.y and self.y - self.speed > 0:
                    self.y -= self.speed

        elif abs(playerpos[1] - self.y) <= self.uzaklik_x and abs(playerpos[1] - self.y) <= self.uzaklik_x -50:

            if self.y >=3 and self.y <= 620:

                if playerpos[1] >= self.y and self.y - self.speed > 0:
                    self.y -= self.speed
                if playerpos[1] <= self.y and self.y + self.speed < screenY:
                    self.y += self.speed
        if self.ammo >0:

            if self.asdd == 0:
                self.asd = 1

            elif self.asdd == 1:
                self.asd = 1.25

            elif self.asdd == 2:
                self.asd = 1.5

            elif self.asdd == 3:
                self.asd = 1.75

            if self.LastDirection != 0 and len([x for x in bullets if x.type != 1]) <  10 and time.time() - self.oldtime >= self.asd: 
                bullets.add(Bullet('Game/bullet.png', (self.x, self.y), 12, self.LastDirection, playerpos, 2))
                self.oldtime = time.time() 
                self.ammo -= 20

        self.counter += 1      
        self.rect.x, self.rect.y = self.x, self.y
        pg.draw.rect(win, (255,0,0), (self.rect.topleft[0]+10, self.rect.topleft[1] - 20, 50, 10))
        pg.draw.rect(win, (0,128,0), (self.rect.topleft[0]+10, self.rect.topleft[1] - 20, 50 - (0.25 * (200 - self.health)), 10))

    def draw(self, win):
        win.blit(self.image, self.rect)

class Bullet(pg.sprite.Sprite):
    def __init__(self, image, location, speed, direction, distination, btype = 1):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load(image), (60, 60))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.x, self.y = self.rect.center = location
        self.direction = direction
        self.distination = distination
        if distination[0] - location[0] != 0:
            self.slope = (distination[1]-location[1]) / (distination[0] - location[0])
        else:
            self.slope = False
        self.type = btype
        pg.mixer.music.play()
    def update(self):
        if self.slope == False:
            self.rect.x += self.speed * self.direction
        elif self.slope == 0:
            self.rect.y += self.speed * self.direction
        else:
            self.rect.y = self.slope * (self.rect.x + self.speed * self.direction - self.rect.x) + self.rect.y        
            self.rect.x += self.speed * self.direction
            



class Obstacle(pg.sprite.Sprite):
    def __init__(self, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([200, 100])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location


bullets = pg.sprite.Group()
obstacles = pg.sprite.Group()
player = Player('Game/standing.png', 5, (50, 50), 7)
enemies = pg.sprite.Group()


playing = True

az = 0
counter = 4
finish = False
zaaa = 0
demira = font.render("Tesekkür ederiz, bizi kurtardınız :)",1,(255,0,0),(0,0,0))
allowed = []
allowed.append(pg.Rect(55, 85, 100, 85))
while playing:
    clock.tick(27)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            playing = False
        elif event.type == pg.KEYDOWN and player.health > 0:
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                player.right = True
                player.LastDirection = 1
            elif event.key == pg.K_LEFT or event.key == pg.K_a:
                player.left = True
                player.LastDirection = -1
            elif event.key == pg.K_SPACE and not player.jumping:
                player.jumping = True
            elif event.key == pg.K_UP or event.key == pg.K_w and not player.jumping:
                player.up = True
            elif event.key == pg.K_DOWN or event.key == pg.K_s and not player.jumping:
                player.down = True
        elif event.type == pg.KEYUP and player.health > 0:
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                player.right = False
            elif event.key == pg.K_LEFT or event.key == pg.K_a:
                player.left = False
            elif event.key == pg.K_UP or event.key == pg.K_w:
                player.up = False
            elif event.key == pg.K_DOWN or event.key == pg.K_s:
                player.down = False
        if event.type == pg.MOUSEBUTTONUP and player.health > 0 and player.LastDirection != 0 and len(bullets) < 5:
            position = pg.mouse.get_pos()
            if position[0] > player.rect.center[0]:
                player.LastDirection = 1
            else:
                player.LastDirection = -1

            
            bullets.add(Bullet('Game/bullet.png', player.rect.center, 8, player.LastDirection, position))

    #print("asd = ",len)
    for enemy in enemies:
        ebullets = pg.sprite.spritecollide(enemy, bullets, False)
        if len(ebullets) > 0:
            for ebullet in ebullets:
                if ebullet.type == 1:
                    bullets.remove(ebullet)
                    enemy.health -= 20
    
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        kontrol-=1

    pbullets = pg.sprite.spritecollide(player, bullets, False)
    if len(pbullets) > 0:
        for pbullet in pbullets:
            if pbullet.type != 1:
                player.health -= 1
    
                bullets.remove(pbullet)
    if player.health >=0:
        sna = str(player.health)
    else:
        sna = "0"
    demirr = font.render(sna,1,(255,0,0),(0,0,0))
    for bullet in bullets:
        if bullet.rect.x <= 0 or bullet.rect.x >= screenX or bullet.rect.y <= 0 or bullet.rect.y >= screenY:
            bullets.remove(bullet)

    snaa ="İnşaa ediliyor %"+str(az)
    demirrr = font.render(snaa,1,(255,0,0),(0,0,0))
    
    if (kontrol == 0 or sa == 0) and sa < counter:
        enemies.add(Enemy('Game/L1E.png', (1000, 500), 200, 400, 5, bullets))
        enemies.add(Enemy('Game/L1E.png', (500, 100), 200, 400, 5, bullets))
        enemies.add(Enemy('Game/L1E.png', (900, 0), 200, 400, 5, bullets))
        kontrol = 3
        sa += 1


    win.blit(bg, bg.get_rect())
    player.move()
    player.update()
    enemies.update((player.x, player.y), player.LastDirection)
    bullets.update()

    if player.health <= 0:
        for enemy in enemies:
            enemy.ammo = 0
        player.kill()

        sfd = font.render("ÖLDÜN",1,(255,0,0),(0,0,0))
        win.blit(sfd,(504,335))
    if len(enemies) == 0 and sa == counter and not finish:
        
        player.x = 660
        player.y = 470
        
        entered = True
        az+=1  
        
        
        if az >= 100:
            a = pg.mixer.music.load("Game/music.mp3")
            pg.mixer.music.play()
            zaaa = 5
            finish = True
    
    if zaaa==5:

        win.blit(demira,(275,344))
        obstacles.draw(win)
        player.draw(win)
        bullets.draw(win)
        enemies.draw(win)
        pg.display.flip()

    else:
        win.blit(demirrr,(740,4))
        win.blit(demirr,(0,0))
        obstacles.draw(win)
        player.draw(win)
        bullets.draw(win)
        enemies.draw(win)
        pg.display.flip()

    

        
