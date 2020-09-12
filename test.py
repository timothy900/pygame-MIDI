import pygame
import pygame.midi
from time import sleep
import random


pygame.init()

# screen settings
size = width, height = 800, 600
bg_color = (0, 0, 0)
white = (220, 220, 220)

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Interval Training') 

##
font = pygame.font.Font('freesansbold.ttf', 64) 
text = font.render('Interval Training', True, white)
textRect = text.get_rect()  
textRect.center = (width // 2, height // 5) 
##

def draw_genButton():
	but_w = 400 # button width
	but_h = 100 # button height
	x = width/2 - but_w/2 # button x coordiante
	y = height - but_h - 75 # button y coordinate

	gray = (170, 170, 170)

	mouse_pos = pygame.mouse.get_pos()
	if (x <= mouse_pos[0] <= x+but_w) and (y <= mouse_pos[1] <= y+but_h):
		pygame.draw.rect(screen, gray, (x, y, but_w, but_h))
		on_button = True
	else:
		pygame.draw.rect(screen, white, (x, y, but_w, but_h))
		on_button = False


	# draw a border
	border_col = (100, 100, 100)
	border_coords = ((x, y), (x+but_w, y), (x+but_w, y+but_h), (x, y+but_h))
	pygame.draw.lines(screen, border_col, True, (border_coords), 3)

	return on_button


def playRandInterval(max_interval):
	# plays a random interval
	# params: 
	# max_interval - max distance in half notes

	gr_piano = 0 # grand piano
	ch_organ = 19 # church organ
	instrument = gr_piano

	pygame.midi.init()
	port = pygame.midi.get_default_output_id()
	midi_out = pygame.midi.Output(port, 0)

	try:
		midi_out.set_instrument(instrument)

		# 72 is middle C, 127 is "how loud" - max is 127
		note1 = 72 + (random.randint(-max_interval, max_interval))
		note2 = 72 +(random.randint(-max_interval, max_interval))
		while note1 == note2: note2 = (random.randint(-max_interval, max_interval))

		midi_out.note_on(note1, 127) 
		sleep(1)
		midi_out.note_off(note1 , 127)
		
		midi_out.note_on(note2, 127)
		sleep(1)
		midi_out.note_off(note2 , 127)

		print(note1, note2)

	finally:
		del midi_out
		pygame.midi.quit()


def main():
	clock = pygame.time.Clock()
	run = True

	while run:
		clock.tick(60)

		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if draw_genButton():	
					playRandInterval(5)

		screen.fill(bg_color)
		draw_genButton()

		# title text
		screen.blit(text, textRect) 

		pygame.display.flip()

	pygame.quit()
	quit()


main()
