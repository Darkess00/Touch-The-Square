#imports
import pygame
from pygame.locals import *
import sys
import menu

#constantes
WIDTH = 640
HEIGHT = 480

#clases
class Square(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=load_image('images/square.png')
		self.rect=self.image.get_rect()
		self.rect.centerx=WIDTH/2
		self.rect.centery=HEIGHT/2
		self.speedx=1
		self.speedy=1
		
	def update(self,time):
		
		if self.rect.left<=0:
			self.speedx=1
		elif self.rect.right>=WIDTH:
			self.speedx=-1
		if self.rect.top<=0:
			self.speedy=1
		elif self.rect.bottom>=HEIGHT:
			self.speedy=-1
		
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

#--------------------------------------------------
def main():
	screen=pygame.display.set_mode((WIDTH,HEIGHT))
	pygame.display.set_caption('Square Game')
	background=load_image('images/black_background.png')
    
	menu.menu(background)
	
	square=Square()
	
	clock=pygame.time.Clock()
	
	contador=0
	handled=False
	
	while True:
		keys=pygame.key.get_pressed()
		clic=pygame.mouse.get_pressed()
		time=clock.tick(60)
		timer=pygame.time.get_ticks()
		restante,restante_rect=load_text(str(contador),WIDTH-30,30)
		pasado,pasado_rect=load_text(str(timer/float(1000)),50,30)
		
		for eventos in pygame.event.get():
			if eventos.type == QUIT:
				sys.exit(0)
			if eventos.type == MOUSEBUTTONUP:
				handled=False
			if eventos.type == MOUSEBUTTONDOWN:
				square.update(time)      
                
		square.update(time)
		
		if clic[0] and pygame.Rect.collidepoint(square.rect,pygame.mouse.get_pos()) and not handled:
			contador +=1
			handled=True
		
		if timer/float(1000)>=60:
			fin,fin_rect=load_text('You touched the square ' + str(contador) +' times',WIDTH/2,HEIGHT/2)
			while True:
				for events in pygame.event.get():
					if events.type==QUIT:
						sys.exit(0)
						break
					if events.type==KEYDOWN:
						sys.exit(0)
						break
						
				screen.blit(background,(0,0))
				screen.blit(fin,fin_rect)
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