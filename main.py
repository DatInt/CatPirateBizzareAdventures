import pygame
import os
import random

pygame.init()
pygame.mixer.init()

WIDTH = 500
HEIGHT = 700
FPS = 60
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

gamewindow = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Cat Pirate vs. Zombies adventure')
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
running = True
score = 0
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
background_img = pygame.image.load(os.path.join(img_folder, 'background.png')).convert()
background_rect = background_img.get_rect()
player_img = pygame.image.load(os.path.join(img_folder, 'cat.png')).convert()
player_img = pygame.transform.scale(player_img, (95, 70))
zombie_img = pygame.image.load(os.path.join(img_folder, 'zombie.png')).convert()
zombie_img = pygame.transform.scale(zombie_img, (85, 110))
fish_img = pygame.image.load(os.path.join(img_folder, 'fish.png')).convert()
fish_img = pygame.transform.scale(fish_img, (65, 20))
spriteWidth, spriteHeight = player_img.get_rect().size

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = player_img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 35
		# pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius)
		self.rect.center = (WIDTH / 2, HEIGHT / 2)
		self.orientation = 'right'

	def update(self):
		self.rect.x = min(max(self.rect.x, 0), WIDTH - spriteWidth)
		self.rect.y = min(max(self.rect.y, 0), HEIGHT - spriteHeight)
		keystate = pygame.key.get_pressed()
		self.speedx = 0
		self.speedy = 0
		if keystate[pygame.K_LEFT]:
			self.speedx = -7
			self.image = pygame.transform.flip(player_img, True, False)
			self.orientation = 'left'
		if keystate[pygame.K_RIGHT]:
			self.speedx = 7
			self.image = pygame.transform.flip(player_img, False, False)
			self.orientation = 'right'
		if keystate[pygame.K_UP]:
			self.speedy = -7
		if keystate[pygame.K_DOWN]:
			self.speedy = 7
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def shoot(self):
		if player.orientation == 'left':
			fish_left = FishLeft(self.rect.centerx, self.rect.centery)
			all_sprites.add(fish_left)
			fishes.add(fish_left)
		else:
			fish_right = FishRight(self.rect.centerx, self.rect.centery)
			all_sprites.add(fish_right)
			fishes.add(fish_right)


player = Player()


class Mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = zombie_img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 43
		# pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius)
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.choice([random.randrange(-300, -200), random.randrange(HEIGHT + 100, HEIGHT + 200)])
		self.speed = random.randrange(2, 5)

	def update(self):
		dirvect = pygame.math.Vector2(player.rect.x - self.rect.x,
																	player.rect.y - self.rect.y)
		try:
			dirvect.normalize()
			dirvect.scale_to_length(self.speed)
			self.rect.move_ip(dirvect)
		except:
			pass



fishes = pygame.sprite.Group()

all_sprites.add(player)
for i in range(3):
	m = Mob()
	all_sprites.add(m)
	mobs.add(m)


class Fish(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = fish_img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedx = 9


class FishRight(Fish):
	def update(self):
		self.rect.x += self.speedx
		if self.rect.x > WIDTH:
			self.kill()


class FishLeft(Fish):
	def update(self):
		self.image = pygame.transform.flip(fish_img, True, False)
		self.rect.x -= self.speedx
		if self.rect.x < -100:
			self.kill()


while running:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()

	all_sprites.update()
	hits = pygame.sprite.groupcollide(mobs, fishes, True, False)
	hits_player = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
	if hits_player:
		running = False
	for hit in hits:
		m = Mob()
		all_sprites.add(m)
		mobs.add(m)
		score += 1
	gamewindow.blit(background_img, background_rect)
	all_sprites.draw(gamewindow)
	draw_text(gamewindow, str(score), 50, 50, 20)
	pygame.display.flip()
