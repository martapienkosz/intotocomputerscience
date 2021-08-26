# Intro to CS | Final Project | Marta Pienkosz and Shyngys Karishev
# AMONG SPACE

add_library('minim')
player = Minim(this)

import random, os, copy
path = os.getcwd()
WIDTH = 1280
HEIGHT = 720

shipbullets = []
enemybullets = []
bossbullets = []

score = 0



class Spaceship:
    
  def __init__(self, x, y, r):
    # x and y possitions, radius, x and y velocities, direction of movement (RIGHT for main spaceship, LEFT for enemies)
    self.x = x
    self.y = y
    self.r = r
    self.vy = 0
    self.vx = 0


  def update(self):
    # updating horizonal and vertical possition of the spaceship
    self.x += self.vx
    self.y += self.vy


  def display(self):
    self.update()
    image(self.img, self.x - (self.r/2), self.y - (self.r/2), self.r, self.r)
    
    
  def distance(self, other):
    # pythagorean theorem it is used to calculate the distance (and collisions) between two objects
    return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5




class Mainship(Spaceship):

  def __init__(self, x, y, r, img):
    Spaceship.__init__(self, x, y, r)
    self.img = loadImage(path + "/images/" + img)
    self.alive = True
    self.key_handler = {DOWN:False, UP:False, RIGHT: False}
    self.healthpoint = player.loadFile(path + "/SOUNDS/healthpoint.wav")
    self.hit = player.loadFile(path + "/SOUNDS/hit.wav")

    # hp represents the health of the spaceship, it decreases when the ship is hit
    self.hp = 100
    # Shield is either on = 1 or off = 0. The ship gains 20 protection points (sp) that reset when hit
    self.shield = 0
    self.sp = 0


  def update(self):
    if game.pause == False:
    # when key up or down is pressed the main spaceship moves vertically
      if self.key_handler[UP] == True and self.y - self.r > 0:
        self.vy = -10

      elif self.key_handler[DOWN] == True and self.y + self.r < HEIGHT:
        self.vy = 10

      else:
        self.vy = 0

      self.x += self.vx
      self.y += self.vy
      
    # creating an impresion of moving background
      if self.x >= 0:
        game.x_shift += 5


    for e in game.enemies:
      # checking for a collistion. When enemyship 'leaves the screen' it is removed and the next one is being initialized a little further.
      if e.x < 0 and game.yourScore < 1000:
            game.enemies.remove(e)
            game.enemies.append(Enemyship(1280 + random.randint(0, 800), random.randint(30, 700), 60, "enemy1.png"))
          
      if self.distance(e) <= self.r + e.r:
        if self.shield == 0:
            self.hit.rewind()
            self.hit.play()
            self.hp -= 10
        # When the shield is off, the spaceship loses health points. When the shield is on it loses protection points (sp)
        if self.shield == 1:
            self.hit.rewind()
            self.hit.play()
            self.sp -= 10
        

    for b in enemybullets:
      # similarly, checking for collision with enemy bullets
      if self.distance(b) <= self.r + b.r:
        if self.shield == 0:
            self.hit.rewind()
            self.hit.play()
            self.hp -= 5
        if self.shield == 1:
            self.hit.rewind()
            self.hit.play()
            self.sp -= 5
        enemybullets.remove(b)


    for b in bossbullets:
      if self.distance(b) <= self.r + b.r:
        if self.shield == 0:
            self.hit.rewind()
            self.hit.play()
            self.hp -= 5
        if self.shield == 1:
            self.hit.rewind()
            self.hit.play()
            self.sp -= 5
        bossbullets.remove(b)


    for a in game.asteroids:
      # checking for a collision with asteroids
      if self.distance(a) <= self.r + a.r:
        if self.shield == 0:
            self.hit.rewind()
            self.hit.play()
            self.hp -= 10
        if self.shield == 1:
            self.hit.rewind()
            self.hit.play()
            self.sp -= 10
        game.asteroids.remove(a)
        
        
    for s in game.shields:
      # shield initiation, assigns an additional 20 sp
      if self.distance(s) <= self.r + s.r:
        self.healthpoint.rewind()
        self.healthpoint.play()
        self.shield = 1
        self.sp = 20
        game.shields.remove(s)
        
        
    for h in game.healthpoints:
      # collecting health points increases the health of the main spaceship
      if self.distance(h) <= self.r + h.r:
        if self.hp < 91:
            self.healthpoint.rewind()
            self.healthpoint.play()
            self.hp += 10
        game.healthpoints.remove(h)
         
               
    if self.hp == 0 or self.hp<0:  
      self.alive = False

      
    # turning off the shield
    if self.sp == 0 or self.sp < 0:
        self.shield = 0
    
           
  def display(self):
    self.update()
    # displaying main spaceship and the shield
    image(self.img, self.x - (self.r/2), self.y - (self.r/2), self.r, self.r)
    if self.shield == 1:
      # the fourth fill variable corresponds to opacity
      fill(118, 139, 248, 100)
      ellipse(self.x, self.y, self.r+15, self.r+15)




class Mainshipbullet():
    
  def __init__(self):
    # initializing bullet at the right edge of main spaceship (instead of the centre)
    self.x = game.ship.x + game.ship.r
    self.y = game.ship.y
    self.m1 = loadImage(path + "/IMAGES/m1.png")
    self.r = 10
    self.vx = 10
    self.vy = 0



  def display(self):
    # making up for the difference in how the ellipse and the picture are displayed
    image(self.m1,  self.x - (self.r/2), self.y - (self.r/2), self.r, self.r)
    self.x += self.vx

    if game.pause == False:
      self.x += self.vx




class Enemyship(Spaceship):
  def __init__(self, x, y, r, img):
    Spaceship.__init__(self, x, y, r)

    self.vx = 3
    self.img = loadImage(path + "/IMAGES/" + img)
    self.alive = True
    self.kill = player.loadFile(path + "/SOUNDS/kill.wav")


  def update(self):
    if game.pause == True:
      self.vx = 0

    elif game.pause == False:
      self.vx = 3

    # negative speed stands for the move to the left
    self.x -= self.vx


    for b in shipbullets:
      # checking for a collision between main spaceship's bullets and enemyship
      if self.distance(b) <= self.r + b.r:
        shipbullets.remove(b)
        self.kill.rewind()
        self.kill.play()
        # increasing the score when main spaceship hits enemy
        global score 
        score += 10
        self.alive = False
    
    
    
    
class Enemyship2(Spaceship):
  def __init__(self, x, y, r, img):
    Spaceship.__init__(self, x, y, r)


    self.vx = 3
    self.img = loadImage(path + "/IMAGES/" + img)
    self.alive = True
    self.kill = player.loadFile(path + "/SOUNDS/kill.wav")
    self.hp = 20



  def update(self):
    if game.pause == True:
      self.vx = 0

    elif game.pause == False:
      self.vx = 3

    # negative speed stands for the move to the left
    self.x -= self.vx


    for b in shipbullets:
      # checking for a collision between main spaceship's bullets and enemyship
      if self.distance(b) <= self.r + b.r:
        shipbullets.remove(b)
        # this spaceship needs to be hit two times to be eliminated
        self.kill.rewind()
        self.kill.play()
        self.hp -= 10
        # increasing the score when main spaceship hits enemy
        if self.hp == 0:
            global score 
            score += 30
            self.alive = False



class Enemyship3(Spaceship):
  def __init__(self, x, y, r, img):
    Spaceship.__init__(self, x, y, r)

    self.vx = 2
    self.img = loadImage(path + "/IMAGES/" + img)
    self.alive = True
    self.kill = player.loadFile(path + "/SOUNDS/kill.wav")
    self.hp = 30


  def update(self):
    if game.pause == True:
      self.vx = 0

    elif game.pause == False:
      self.vx = 2

    # negative speed stands for the move to the left
    self.x -= self.vx


    for b in shipbullets:
      # checking for a collision between main spaceship's bullets and enemyship
      if self.distance(b) <= self.r + b.r:
        shipbullets.remove(b)
        # this spaceship has there lifes
        self.kill.rewind()
        self.kill.play()
        self.hp -=10
        # increasing the score when main spaceship hits enemy
        if self.hp == 0:
            global score 
            score += 50
            self.alive = False
            


class Enemybullets():
  def __init__(self, enemy):
    # initializing bullet at the left edge of enemy spaceship (instead of the centre)
    self.x = enemy.x - enemy.r
    self.y = enemy.y
    self.b1 = loadImage(path + "/IMAGES/b1.png")
    self.r = 10
    self.vx = -10


  def display(self):
    fill(210)
    image(self.b1, self.x - (self.r/2), self.y - (self.r/2), self.r, self.r)

    if game.pause == False:
      self.x += self.vx




class Boss(Spaceship):

  def __init__(self, x, y, r, img):
    Spaceship.__init__(self, x, y, r)
    self.alive = True

    # boss spaceships have 7 lifes and thus increase the difficulty of game
    self.hp = 70
    self.img = loadImage(path + "/IMAGES/" + img)
    self.kill = player.loadFile(path + "/SOUNDS/kill.wav")
    self.vx = 5
    self.vy = 0



  def update(self):
    if game.pause == True:
      self.vx = 0
      self.vy = 0

    elif game.pause == False:

      if self.x > 950 and frameCount%20 == 0:
        self.vx = - 5
        
    # they move vertically at the 3/4 width of the screen
      if self.x <= 950 and self.vy == 0:
        self.vx = 0
        self.vy = 5

      if self.y > random.randint(580, 670):
        self.vy = -5
        self.vx = 0

      elif self.y < random.randint(50, 150):
        self.vy = 5
        self.vx = 0


    self.x += self.vx
    self.y += self.vy


    for b in shipbullets:
      if self.distance(b) <= self.r:
        shipbullets.remove(b)
        self.kill.rewind()
        self.kill.play()
        self.hp -= 10
        if self.hp == 0:
            global score 
            score += 120
            self.alive = False
        


class Bossbullettttt():
    
  def __init__(self, boss, shot):
    self.x = boss.x
    self.y = boss.y

    self.type = boss
    self.shot = int(shot)
    self.b2 = loadImage(path + "/IMAGES/b2.png")
    self.r = 10
    self.vx = -10
    self.vy = 0



  def display(self):
    fill(210)
    image(self.b2, self.x - (self.r/2), self.y - (self.r/2), self.r, self.r)


    # displaying up to 9 bullets; due to different vy they spread put over time across the screen
    if self.shot == 1:
      self.vy = 0

    elif self.shot == 2:
      self.vy = -0.75

    elif self.shot == 3:
      self.vy = -1.5

    elif self.shot == 4:
      self.vy = 0.75

    elif self.shot == 5:
      self.vy = 1.5
      
    elif self.shot == 6:
      self.vy = 2.25
    
    elif self.shot == 7:
      self.vy = -2.25
      
    elif self.shot == 8:
      self.vy = 3
      
    elif self.shot == 9:
      self.vy = -3
    


    if game.pause == False:
      self.x += self.vx
      self.y +=self.vy




class Asteroid:
  def __init__(self, x, y, r, img):
    # assigning necessary variables, loading an image
    self.x = x
    self.y = y
    self.r = r
    self.vx = 2
    self.img = loadImage(path + "/images/" + img)


  def display(self):
    if game.pause == True:
      self.vx = 0

    elif game.pause == False:
      self.vx = 2
      
    self.x -= self.vx
    image(self.img, self.x - (self.r/2), self.y - (self.r/2), self.r, self.r)
    
    
    

class HealthPoint(Asteroid):
  def __init__(self, x, y, r, img):
    Asteroid.__init__(self, x, y, r, img)
    # health points and asteroids are similarly randomly placed objects, they differ in speed and loaded image
    self.img = loadImage(path + "/images/" + img)
    self.vx = 4
        
  def display(self):
    if game.pause == True:
      self.vx = 0

    elif game.pause == False:
      self.vx = 4
      
    self.x -= self.vx
    image(self.img, self.x - (self.r/2), self.y - (self.r/2), self.r, self.r)
        



class Shield(Asteroid):
  def __init__(self, x, y, r, img):
    Asteroid.__init__(self, x, y, r, img)
    self.img = loadImage(path + "/images/" + img)
    self.vx = 5
        

  def display(self):
    if game.pause == True:
      self.vx = 0

    elif game.pause == False:
      self.vx = 5
      
    self.x -= self.vx
    image(self.img, self.x - (self.r/2), self.y - (self.r/2), self.r, self.r)



class Game:
  def __init__(self, w, h):
    self.pause = True
    self.h = h
    self.w = w
    # yourScore represents the total amount of time spent playing and enemy ships eliminated
    self.yourScore = 0
    self.scr = 0
    
    self.background_sound = player.loadFile(path + "/SOUNDS/backsong.mp3")
    self.background_sound.rewind()
    self.background_sound.loop()
    
    self.pause_song = player.loadFile(path + "/SOUNDS/pause.wav")
    
    self.instructions = loadImage(path + "/images/start.png")
    self.layer = loadImage(path + "/IMAGES/Layer.jpg")
    self.healthbar = loadImage(path + "/IMAGES/healthbar.png")
    self.gameover = loadImage(path + "/IMAGES/gameover.png")
    self.start = loadImage(path + "/IMAGES/start.png")
    self.info = loadImage(path + "/IMAGES/key.png")
    

    self.x_shift = 10
    self.ship = Mainship(100, 360, 50, "mainship.png")


    self.asteroids = []
    # initializing three asteroids for every 1000 pixels
    for i in range(1, 100):
        self.asteroids.append(Asteroid(i*1000 + random.randint(0, 1000), random.randint(30, 700), 30, "asteroid.png"))
        self.asteroids.append(Asteroid(i*1000 + random.randint(0, 1000), random.randint(30, 700), 25, "asteroid.png"))
    
    self.shields = []
    # initializing shield for every 5000 pixels
    for i in range(1, 100):
        self.shields.append(Shield(i*5000 + random.randint(0, 5000), random.randint(30, 700), 40, "shield.png"))
   
    self.enemies = []
    # initialization of three series of enemy spaceships, their number increases over the game
    # additional spaceships are initial after each previous enemy elimination, if we were to initiate everything at the very beginning, the game would lag and crash
    for i in range(2):
        for e in range(i*3-i*2):
            self.enemies.append(Enemyship(1000 + random.randint(0, 800), random.randint(30, 700), 60, "enemy1.png"))
            self.enemies.append(Enemyship(1000 + random.randint(0, 800), random.randint(30, 700), 60, "enemy1.png"))
            self.enemies.append(Enemyship(1000 + random.randint(0, 800), random.randint(30, 700), 60, "enemy1.png"))
    
    self.bosses = []
    # appending one boss spaceship
    self.bosses.append(Boss(7000, 360, 70, "boss.png"))
    
    self.healthpoints = []
    # initializing one health point for every 2000 pixels
    for h in range(0, 100):
        self.healthpoints.append(HealthPoint(h*2000 + random.randint(0, 2000), random.randint(30, 700), 40, "healthpoint.png"))



  def display(self):
      
    if self.ship.alive == False:
    # displaying score and game over message
      image(self.gameover, 0, 0, 1280, 720)
      fill(252,224,99)
      textSize(63)
      text(self.yourScore, 630, 410)
      return



    # creating an allusion of continously scrolling background
    x = 0
    cnt = 0
    if cnt == 0:
        x_shift = self.x_shift//4
    elif cnt == 1:
        x_shift = self.x_shift//3
    elif cnt == 2:
        x_shift = self.x_shift//2
    else:
        x_shift = self.x_shift

    width_right = x_shift % self.w
    width_left = self.w - width_right

    image(self.layer, 0, 0, width_left, self.h, width_right, 0, self.w, self.h)
    image(self.layer, width_left, 0, width_right, self.h, 0, 0, width_right, self.h)
    cnt += 1



    for b in shipbullets:
    # removing main spaceship bullets that left the screen
      if b.x < 1280:
          if self.ship.alive == True:
            b.display()
      else:
        shipbullets.remove(b)


    for e in self.enemies:
      if e.alive == True:
        e.display()

      else:
        # removing enemy spaceships that have been eliminated and initializing new ones a little further
        self.enemies.remove(e)
        # making sure that when bosses are displayed other enemies are not
        for e in game.bosses:
            if e.x > 2200 and game.pause == False:
                # appending enemies when othetougher enemies as the user progresses
                if self.yourScore < 400:
                    self.enemies.append(Enemyship(1280 + random.randint(0, 800), random.randint(30, 700), 60, "enemy1.png"))
                if self.yourScore > 400 and self.yourScore < 600:
                    self.enemies.append(Enemyship2(1280 + random.randint(0, 700), random.randint(30, 700), 60, "enemy2.png"))
                if self.yourScore > 600 and self.yourScore < 800:
                    self.enemies.append(Enemyship3(1280 + random.randint(0, 700), random.randint(30, 700), 60, "enemy3.png"))
                if self.yourScore > 800 and self.yourScore < 1000:
                    self.enemies.append(Enemyship(1280 + random.randint(0, 2200), random.randint(30, 700), 60, "enemy1.png"))
                    self.enemies.append(Enemyship2(1280 + random.randint(0, 2200), random.randint(30, 700), 60, "enemy2.png"))
                if self.yourScore > 1000 and self.yourScore < 1200:
                    self.enemies.append(Enemyship(1280 + random.randint(0, 2200), random.randint(30, 700), 60, "enemy1.png"))
                    self.enemies.append(Enemyship3(1280 + random.randint(0, 2200), random.randint(30, 700), 60, "enemy3.png"))
                if self.yourScore > 1200 and self.yourScore < 1200:
                    self.enemies.append(Enemyship2(1280 + random.randint(0, 1200), random.randint(30, 700), 60, "enemy2.png"))
                    self.enemies.append(Enemyship2(1280 + random.randint(0, 1200), random.randint(30, 700), 60, "enemy2.png"))
                if self.yourScore > 1200  and self.yourScore < 1800:
                    self.enemies.append(Enemyship2(1280 + random.randint(0, 2000), random.randint(30, 700), 60, "enemy2.png"))
                    self.enemies.append(Enemyship3(1280 + random.randint(0, 2000), random.randint(30, 700), 60, "enemy3.png"))
                if self.yourScore > 1800:
                    self.enemies.append(Enemyship3(1280 + random.randint(0, 1800), random.randint(30, 700), 60, "enemy3.png"))
                    self.enemies.append(Enemyship3(1280 + random.randint(0, 1800), random.randint(30, 700), 60, "enemy3.png"))
                    


    for a in self.asteroids:
        a.display()

            
    for h in self.healthpoints:
        h.display()

    
    for s in self.shields:
        s.display()
            
            
    for b in bossbullets:
      b.display()


    for b in enemybullets:   
    # displaying enemy bullets, removing enemy bullets after they 'left' the screen
      if b.x > 0:
          if self.ship.alive == True:
            b.display()
      else:
        enemybullets.remove(b)
        
    
    # displaying healthbar rectangle with width corresponding to health points
    noStroke()
    fill(29,200,200)
    rect(1020,30,200,30)
    fill(252,224,99)
    rect(1020,30,self.ship.hp*2,30)
    image(self.healthbar,1000,23,240,50)
    image(self.info, 1235, 20, 50, 50)
    
    # increasing score with every second
    if game.pause == False and self.ship.alive == True:
        if frameCount%60 == 0:
            self.scr +=1

    
    # displaying score, time spent and enemies eliminated
    textSize(20)
    self.yourScore = self.scr + score
    text(self.yourScore, 30, 50)
    
      
    self.ship.display()


    # if self.enemies == []:
    for e in self.bosses:
        if e.alive == True:
            e.display()
        else:
            self.bosses.remove(e)
            self.bosses.append(Boss(5000, 360, 70, "boss.png"))
            # appending three enemies spaceships once  boss in being eliminated, it starts the above loop 'for e in game.bosses'
            self.enemies.append(Enemyship(1300 + random.randint(0, 200), random.randint(30, 700), 60,  "enemy1.png"))
            self.enemies.append(Enemyship(1300 + random.randint(0, 400), random.randint(30, 700), 60, "enemy1.png"))
            self.enemies.append(Enemyship2(1300 + random.randint(0, 600), random.randint(30, 700), 60, "enemy2.png"))
         
               
    # displayin instructions when the game is being paused
    if game.pause == True:
        image(self.start, 0, 0, 1280, 720)
        self.pause_song.play()
    else: 
        self.background_sound.play()
    


game = Game(WIDTH, HEIGHT)


def setup():
  size(WIDTH, HEIGHT)



def draw():
  game.display()

  if frameCount%90 == 0 and game.pause == False:
    # initializing new bullets every 1.5 sec
    for e in game.enemies:
      if e.x < 1280 and e.x > 0:
        enemybullets.append(Enemybullets(e))

  if frameCount%100 == 0 and game.pause == False:
    for b in game.bosses:

      if b.x <= 950:
        bossbullets.append(Bossbullettttt(b,1))
        bossbullets.append(Bossbullettttt(b,2))
        bossbullets.append(Bossbullettttt(b,3))  
        bossbullets.append(Bossbullettttt(b,4))
        bossbullets.append(Bossbullettttt(b,5))
        
        if game.yourScore > 800:
            # increasing difficulty: boss now shots 7 bullets
            bossbullets.append(Bossbullettttt(b,6))
            bossbullets.append(Bossbullettttt(b,7))
            
            if game.yourScore > 800:
                # increasing difficulty: boss now shots 9 bullets
                bossbullets.append(Bossbullettttt(b,8))
                bossbullets.append(Bossbullettttt(b,9))

    

def keyPressed():
  if keyCode == UP or key == 'W' or key == 'w':
    game.ship.key_handler[UP] = True

  elif keyCode == DOWN or key == 'S' or key == 's':
    game.ship.key_handler[DOWN] = True

  if key == 'E' or key == 'e':
    # initializing main spaceships bullets
    game.ship.key_handler[RIGHT] = True
    shipbullets.append(Mainshipbullet())

  if key == 'Q' or key == 'q' and game.pause == False:
    game.pause = True
    game.pause_song.play()
    game.pause_song.rewind()

  elif key == 'Q' or key == 'q' and game.pause == True:
    game.pause = False
    game.pause_song.play()
    game.pause_song.rewind()



def keyReleased():

  if keyCode == UP or key == 'W' or key == 'w':
    game.ship.key_handler[UP] = False

  elif keyCode == DOWN or key == 'S' or key == 's':
    game.ship.key_handler[DOWN] = False

  if key == 'E' or key == 'e':
    game.ship.key_handler[RIGHT] = False


def mouseClicked():
    # resting the game, clearing all the lists and setting variables to 0
    global game
    
    if mouseX > 1240 and mouseX < 1280 and mouseY > 23 and mouseY < 73 and game.pause == False:
        game.pause = True
        game.pause_song.play()
        game.pause_song.rewind()
    
    if game.ship.alive == False:
        game.bosses = []
        game.enemies = []
            
        game.asteroids = []
        game.shields = []
        game.healthpoints = []
        
        global shipbullets
        shipbullets = []
        
        global enemybullets
        enemybullets = []
        
        global bossbullets
        bossbullets = []
        
        game.yourScore = 0
        game.scr = 0
        global score
        score = 0
        
        game.ship.hp = 100
        game = Game(WIDTH, HEIGHT)
