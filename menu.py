import pygame, sys, rewards
from pygame.locals import *

WIDTH = 640
HEIGHT = 480

class Texto(pygame.sprite.Sprite):
	text=''
	text_rect=''
	def __init__(self,cadena,x,y,color=(255,255,255)):
		pygame.sprite.Sprite.__init__(self)
		self.text,self.text_rect=load_text(cadena,x,y,color)
		
def your_top():
	f=open('data/max','r')
	max=int(f.read())
	f.close()
	return max
		
def load_text(texto,x,y,color=(255,255,255)):
	font=pygame.font.Font('fonts/fontx.ttf',25)
	salida=pygame.font.Font.render(font,texto,1,color)
	salida_rect=salida.get_rect()
	salida_rect.centerx=x
	salida_rect.centery=y
	return salida, salida_rect     
 

def menu(background,top):
	pygame.init()
	screen=pygame.display.set_mode((WIDTH,HEIGHT))
	pygame.display.set_caption('Square Game')
	opcion1=Texto('New Game',WIDTH/2,HEIGHT/4)
	opcion2=Texto('Rewards',WIDTH/2,HEIGHT/2)
	opcion3=Texto('Rankings',WIDTH/2,HEIGHT*0.75)
	max=Texto('Max: ' + str(top),WIDTH*0.8,HEIGHT/2,(255,255,0))
	#clock=pygame.time.Clock()
	contador = 0
	while True:
		clic=pygame.mouse.get_pressed()
		contador += 1
		i=Texto(str(contador),50,50)
		#time=clock.tick(60)
	
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
				break
		
		if clic[0] and opcion1.text_rect.collidepoint(pygame.mouse.get_pos()):
			clock=pygame.time.Clock()
			timer=pygame.time.get_ticks()
			return timer
			break
		if clic[0] and pygame.Rect.collidepoint(opcion2.text_rect,pygame.mouse.get_pos()):
			rewards.rewards()
			break
		if clic[0] and pygame.Rect.collidepoint(opcion3.text_rect,pygame.mouse.get_pos()):
			break
		
		screen.blit(background,(0,0))
		#screen.blit(i.text,i.text_rect)
		screen.blit(opcion1.text,opcion1.text_rect)
		screen.blit(opcion2.text,opcion2.text_rect)
		screen.blit(opcion3.text,opcion3.text_rect)
		screen.blit(max.text,max.text_rect)
		pygame.display.flip()
		