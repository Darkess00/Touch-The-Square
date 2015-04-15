#imports
import pygame, random, sys, menu
from pygame.locals import *

try:
	import android
except ImportError:
	android = None

#constantes
WIDTH = 640
HEIGHT = 480
REWARDS = {'1': 20, '2': 30, '3': 40, '4': 50, '5': 60}

#clases
class Square(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=load_image('images/square.png')
		self.rect=self.image.get_rect()
		self.rect.centerx=WIDTH/2
		self.rect.centery=HEIGHT/2
		self.speedx=3
		self.speedy=3
		
	def update(self,time):
		
		if self.rect.left<=0:
			self.speedx=random.randint(5,10)*random.uniform(0.4,1)
			if(self.rect.centery<HEIGHT/2):
				self.speedy=random.randint(5,10)*random.uniform(0.4,1)
			elif(self.rect.centery>=HEIGHT/2):
				self.speedy=random.randint(-10,-5)*random.uniform(0.4,1)
		
		elif self.rect.right>=WIDTH:
			self.speedx=random.randint(-10,-5)*random.uniform(0.4,1)
			if(self.rect.centery<HEIGHT/2):
				self.speedy=random.randint(5,10)*random.uniform(0.4,1)
			elif(self.rect.centery>=HEIGHT/2):
				self.speedy=random.randint(-10,-5)*random.uniform(0.4,1)
				
		if self.rect.top<=0:
			self.speedy=random.randint(5,10)*random.uniform(0.4,1)
			if self.rect.centerx<WIDTH/2:
				self.speedx=random.randint(5,10)*random.uniform(0.4,1)
			elif(self.rect.centery>=HEIGHT/2):
				self.speedx=random.randint(-10,-5)*random.uniform(0.4,1)
		
		elif self.rect.bottom>=HEIGHT:
			self.speedy=random.randint(-10,-5)*random.uniform(0.4,1)
			if(self.rect.centerx<WIDTH/2):
				self.speedx=random.randint(5,10)*random.uniform(0.4,1)
			elif(self.rect.centerx>=WIDTH/2):
				self.speedx=random.randint(-10,-5)*random.uniform(0.4,1)
		
		self.rect.centerx+=self.speedx*time
		self.rect.centery+=self.speedy*time
		
class Texto(pygame.sprite.Sprite):
	text=''
	text_rect=''
	def __init__(self,cadena,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.text,self.text_rect=load_text(cadena,x,y)
		
#funciones
#--------------------------------------------------

def load_image(filename,transparent=False):
	try: image=pygame.image.load(filename)
	except pygame.error, message:
		raise SystemExit, message
	image = image.convert()
	if transparent:
		color=image.get_at((0,0))
		image.set_colorkey(color,RLEACCEL)
	return image
	
def load_text(texto,x,y,color=(255,255,255)):
	font=pygame.font.Font('fonts/fontx.ttf',25)
	salida=pygame.font.Font.render(font,texto,1,color)
	salida_rect=salida.get_rect()
	salida_rect.centerx=x
	salida_rect.centery=y
	return salida, salida_rect        

def check_rewards(contador):
		f=open('data/rewards','r')
		number=int(f.read())
		f.close()
		f=open('data/rewards','w')
		if number == 0 and contador==REWARDS['1']:
			f.write('1')
			f.close()
		elif number == 1 and contador==REWARDS['2']:
			f.write('2')
			f.close()
		elif number == 2 and contador==REWARDS['3']:
			f.write('3')
			f.close()
		elif number == 3 and contador==REWARDS['4']:
			f.write('4')
			f.close()
		elif number == 4 and contador==REWARDS['5']:
			f.write('5')
			f.close()
		else:
			f.write(str(number))
			f.close()

def your_top():
	f=open('data/max','r')
	max=int(f.read())
	f.close()
	return max

def write_top(top):
	f=open('data/max','r')
	ftop=int(f.read())
	f.close()
	if top>ftop:
		f=open('data/max','w')
		f.write(str(top))
		f.close()
	


#--------------------------------------------------
def main():
	intento=0
	screen=pygame.display.set_mode((WIDTH,HEIGHT))
	pygame.display.set_caption('Square Game')
	background=load_image('images/black_background.png')
	menos=menu.menu(background,your_top())
	square=Square()
	
	if menos=='quit':
		return None
	
	contador=0
	handled=False
	
	if android:
		android.init()
		android.map_key(android.KEYCODE_BACK, K_ESCAPE)
	
	while True:
		
		keys=pygame.key.get_pressed()
		clic=pygame.mouse.get_pressed()
		clock=pygame.time.Clock()
		time=clock.tick(144)
		timer=pygame.time.get_ticks()-intento
		
		restante,restante_rect=load_text(str(contador),WIDTH-30,30)
		pasado,pasado_rect=load_text(str((timer-menos)/float(1000)),50,30)
		
		for eventos in pygame.event.get():
			if eventos.type == QUIT:
				pygame.quit()
				break
			if eventos.type == MOUSEBUTTONUP:
				handled=False
			if eventos.type == MOUSEBUTTONDOWN:
				square.update(time)      
				
		if contador<your_top():
			top=your_top()
		else:
			top=contador
		
		write_top(top)
		                
		square.update(time)
		
		if pygame.Rect.collidepoint(square.rect,pygame.mouse.get_pos()) and not handled:
			contador +=1
			handled=True
			check_rewards(contador)
			
		if keys[K_ESCAPE]:
			break
		
		if (timer-menos)/float(1000)>=60:
			fin,fin_rect=load_text('You touched the square ' + str(contador) +' times',WIDTH/2,HEIGHT/3)
			max,max_rect=load_text('Your max touches: ' + str(top),WIDTH/2,HEIGHT*0.66)
			while True:
				for events in pygame.event.get():
					if events.type==QUIT:
						pygame.quit()
						break
					if events.type==KEYDOWN:
						pygame.quit()
						break
					if events.type==MOUSEBUTTONDOWN:
						main()
						
				screen.blit(background,(0,0))
				screen.blit(fin,fin_rect)
				screen.blit(max,max_rect)
				pygame.display.flip()				
		
		screen.blit(background,(0,0))
		screen.blit(restante,restante_rect)
		screen.blit(pasado,pasado_rect)
		screen.blit(square.image,square.rect)
		pygame.display.flip()
	return 0
	
if __name__ == '__main__':
	pygame.init()
	main()
	pygame.quit()