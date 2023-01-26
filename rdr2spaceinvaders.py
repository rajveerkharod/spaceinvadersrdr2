#Rajveer Kharod APCSP 3
import pygame #Imports the necessary modules
from pygame import mixer
from pygame.locals import *
import random

shield = ''
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()


#define fps
clock = pygame.time.Clock()
fps = 60

#defines the size of the screen
screen_width = 600
screen_height = 800
#Sets up the screen and puts the caption
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invanders')


#define fonts for ingame text
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)


#load sounds such as the explosion
soundFile = "img/explosion.wav"
explosion_fx = pygame.mixer.Sound(soundFile)
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound("img/explosion2.wav")
explosion2_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound("img/laser.wav")
laser_fx.set_volume(0.25)


#define game variables
rows = 5
cols = 5
alien_cooldown = 1000#bullet cooldown which is in milliseconds
last_alien_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0#0 is no game over, 1 means player has won, -1 means player has lost
collision_count = 0


#defines the colours for the health bar
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)



#load image which will be the background
bg = pygame.image.load("img/bg.png")
#draws the background
def draw_bg():
	screen.blit(bg, (0, 0))


#this defines the function that lets you put text on the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))



#create spaceship class, spaceship is the main player which shoots at the aliens
class Spaceship(pygame.sprite.Sprite):
	def __init__(self, x, y, health):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/dutchnew2.png")#gets the image
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.health_start = health#creates health for the class
		self.health_remaining = health
		self.last_shot = pygame.time.get_ticks()

	# Gives dynamic functionality to the spaceship
	def update(self):
		#set movement speed
		speed = 8
		#set a cooldown variable
		cooldown = 500 #milliseconds
		game_over = 0


		#get key press so the spaceship can move left and right
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left > 0:
			self.rect.x -= speed
		if key[pygame.K_RIGHT] and self.rect.right < screen_width:
			self.rect.x += speed

		#record current time
		time_now = pygame.time.get_ticks()
		#allows the player to shoot at the aliens
		if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
			laser_fx.play()
			bullet = Bullets(self.rect.centerx, self.rect.top)
			bullet_group.add(bullet)
			self.last_shot = time_now


		#update mask
		self.mask = pygame.mask.from_surface(self.image)


		#draw health bar for the spaceship, lets it take 3 hits
		pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
		if self.health_remaining > 0:
			pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))

		# If the player dies, the game is over and player explodes
		elif self.health_remaining <= 0:
			explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
			explosion_group.add(explosion)
			self.kill()
			game_over = -1
		return game_over



#create Bullets class
class Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y):#creates the sprite for bullet
		pygame.sprite.Sprite.__init__(self)#makes the bullet a sprite
		self.image = pygame.image.load("img/bullet.png")#loads the image for the bullet
		self.rect = self.image.get_rect()#gives the images and the center, makes it a rectangle
		self.rect.center = [x, y]
#defines actions which the bulet does
	def update(self):
		self.rect.y -= 5
		if self.rect.bottom < 0:
			self.kill()
		if pygame.sprite.spritecollide(self, alien_group, True):#if the bullet collides with any of the aliens, it dies
			self.kill()
			explosion_fx.play()#plays explosion and shows it if the sprite is killed
			explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
			explosion_group.add(explosion)




#create Aliens class
class Aliens(pygame.sprite.Sprite):
	def __init__(self, x, y):#makes it a sprite
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/alien" + str(random.randint(1, 5)) + ".png")#loads the images 1 to 5 for the aliens
		self.rect = self.image.get_rect()#creates the image on the screen
		self.rect.center = [x, y]
		self.move_counter = 0
		self.move_direction = 1

	def update(self):#it allows the aliens to do different functions like moving across the screen
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 75:
			self.move_direction *= -1
			self.move_counter *= self.move_direction

#create shields class
class Shield(pygame.sprite.Sprite):
	def __init__(self, x, y, health, image):#makes the shield a sprite
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/" + image)#loads the image for the shield class
		self.rect = self.image.get_rect()#creates the image
		self.rect.center = [x,y]
		self.health_start = health #gives health to the shield
		self.health_remaining = health

	def update(self):
		#update mask
		self.mask = pygame.mask.from_surface(self.image)

		if self.health_remaining <= 0:#if the health goes to 0, the shield dies
			self.kill()
			explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
			explosion_group.add(explosion)

class John(pygame.sprite.Sprite):
	def __init__(self, x, y):#makes a John class a sprite
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/john.png")#loads image
		self.rect = self.image.get_rect()#puts image on screen and picks where on screen
		self.rect.center = [500, 600]
		
	def update(self):
		self.rect.x += john.rect.x#allows john to move
		self.move_counter += 1
		if abs(self.move_counter) > 75:
			self.move_direction *= -1
			self.move_counter *= self.move_direction

class Charles(pygame.sprite.Sprite):
	def __init__(self, x,y):#makes Charles class a sprite
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/charles.png")#loads image
		self.rect = self.image.get_rect()#puts image on screen
		self.rect.center = [100,600]
	
	def update(self):#allows charles to move
		self.rect.x += charles.rect.x
		self.move_counter += 1
		if abs(self.move_counter) > 75:
			self.move_direction *= -1
			self.move_counter *= self.move_direction

#create Alien Bullets class
class Alien_Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y):#makes alien bullets a class
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/alien_bullet.png")#loads image
		self.rect = self.image.get_rect()#puts image on screen
		self.rect.center = [x, y]
		#self.hits=0
		#self.oneshot = True
#the bullet dies if it hits the space ship, and it reduces the health of the spaceship and the arthur shield if it ends up hitting that, 
	def update(self):
		self.rect.y += 2
		if self.rect.top > screen_height:
			self.kill()
		if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
			self.kill()
			explosion2_fx.play()
			#reduce spaceship health
			spaceship.health_remaining -= 1
			explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
			explosion_group.add(explosion)
		if pygame.sprite.spritecollide(self, shield_group, False, pygame.sprite.collide_mask):
			explosion2_fx.play()
			explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
			explosion_group.add(explosion)
			arthur.health_remaining -= 1#lowers health of shield class
			self.kill()
		if pygame.sprite.spritecollide(self,john_group,True,pygame.sprite.collide_mask):
			explosion2_fx.play()
			explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
			explosion_group.add(explosion)
			self.kill()
		if pygame.sprite.spritecollide(self,charles_group,True,pygame.sprite.collide_mask):
			explosion2_fx.play()
			explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
			explosion_group.add(explosion)
			self.kill()
		print(arthur.health_remaining)

#create Explosion class
class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, size):#makes the explosion a sprite
		pygame.sprite.Sprite.__init__(self)
		self.images = []#loads image based on the size and adds images
		for num in range(1, 6):
			img = pygame.image.load(f"img/exp{num}.png")
			if size == 1:
				img = pygame.transform.scale(img, (20, 20))
			if size == 2:
				img = pygame.transform.scale(img, (40, 40))
			if size == 3:
				img = pygame.transform.scale(img, (160, 160))
			#add the image to the list
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0


	def update(self):
		explosion_speed = 3
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#when the animation is done, it deletes explosion
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()




#create sprite groups for each of the classes
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
shield_group = pygame.sprite.Group()
john_group = pygame.sprite.Group()
charles_group = pygame.sprite.Group()

def create_aliens():#it creates the aliens for each of the rows
	#generate aliens
	for row in range(rows):
		for item in range(cols):
			alien = Aliens(100 + item * 100, 100 + row * 70)
			alien_group.add(alien)

create_aliens()


#creates the spaceship,arthur,charles, and john on the screen so we can see them
spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
spaceship_group.add(spaceship)
arthur = Shield(int(screen_width / 2),int(screen_height - 200),3,"arthur.png")
shield_group.add(arthur)
john = John(int(screen_width / 2), "john.png")
john_group.add(john)
charles = Charles(int(screen_width / 2), "charles.png")
charles_group.add(charles)

# Start of game loop
run = True
while run:
#if the game is running, it draws the background on the screen
	clock.tick(fps)

	#draw background
	draw_bg()


	if countdown == 0:
		#create random alien bullets
		#record current time
		time_now = pygame.time.get_ticks()
		#shoot
		if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
			attacking_alien = random.choice(alien_group.sprites())
			alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
			alien_bullet_group.add(alien_bullet)
			last_alien_shot = time_now

		#checks if all the aliens are dead
		if len(alien_group) == 0:
			game_over = 1

		if game_over == 0:
			#update spaceship
			game_over = spaceship.update()

			#update sprite groups
			bullet_group.update()
			alien_group.update()
			alien_bullet_group.update()
			shield_group.update()
		
		else:#displays text on the screen if the game is over, supporting if you win, not supporting if you lose
			if game_over == -1:
				draw_text('You Lost Haha', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
			if game_over == 1:
				draw_text('I could have done better', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))

	if countdown > 0:# While the countdown is not zero, it puts the text on the screen
		draw_text('GET READY!', font40, white, int(screen_width / 2 - 110), int(screen_height / 2 + 50))
		draw_text(str(countdown), font40, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
		count_timer = pygame.time.get_ticks()
		if count_timer - last_count > 1000:
			countdown -= 1
			last_count = count_timer


	# this updates the explosion group
	explosion_group.update()


	#draws the different sprites on to the screen
	spaceship_group.draw(screen)
	bullet_group.draw(screen)
	alien_group.draw(screen)
	alien_bullet_group.draw(screen)
	explosion_group.draw(screen)
	shield_group.draw(screen)
	john_group.draw(screen)
	charles_group.draw(screen)
	
	#if the player quits, it stops running the game
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	# Updates the screen after each iteration of the game loop
	pygame.display.update()

pygame.quit()#quits the game
