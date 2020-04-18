import pygame, sys
import time
import numpy as np
import re
from random import randint


def getPuzzle(name):
	PuzzleOBJ = []
	with open(name, 'r') as file:
		lines = file.read()
	lines = re.findall(r'\d+', lines)
	for line in lines[0:9]:
		l = []
		for c in line:
			l += [int(c)]
		PuzzleOBJ += [l]
	print(PuzzleOBJ)
	return PuzzleOBJ


class GUI(object):
	"""docstring for GUI"""
	def __init__(self,name, solver):
		self.solver = solver
		self.name = name
		self.Pygame = pygame
		self.Pygame.init()
		self.Pygame.font.init()
		self.display_width = 800
		self.display_height = 600
		self.font = self.Pygame.font.SysFont('arial',25)
		self.gameDisplay = self.Pygame.display.set_mode((self.display_width,self.display_height))
		self.Pygame.display.set_caption(self.name)
		self.clock = self.Pygame.time.Clock()
		self.colors={
					'black':(0,0,0),
					'bright_green':(0,255,0),
					'bright_red':(255,0,0),
					'white':(255,255,255),
					'red':(200,0,0),
					'green':(0,200,0),
					'blue':(0,0,255),
					'dead':(128,128,128),
					'msg':(0,153,64)
		}

	def text_objects(self, text, font, color = 'black'):
		textSurface = font.render(text, True, self.colors[color])
		return textSurface, textSurface.get_rect()
 
	def button(self,msg,x,y,w,h,ic,ac,action=None):
		mouse = self.Pygame.mouse.get_pos()
		click = self.Pygame.mouse.get_pressed()
		if x+w > mouse[0] > x and y+h > mouse[1] > y:
			self.Pygame.draw.rect(self.gameDisplay, ac,(x,y,w,h))
			if click[0] == 1 and action != None:
				action()         
		else:
			self.Pygame.draw.rect(self.gameDisplay, ic,(x,y,w,h))
		smallText = self.Pygame.font.SysFont("comicsansms",20)
		textSurf, textRect = self.text_objects(msg, smallText)
		textRect.center = ( (x+(w/2)), (y+(h/2)) )
		self.gameDisplay.blit(textSurf, textRect)
	   
	def Dispaly(self):

		intro = True

		while intro:
			for event in self.Pygame.event.get():
				if event.type == self.Pygame.QUIT:
					self.Pygame.quit()
					# quit()
					
			self.gameDisplay.fill(self.colors['white'])
			largeText = self.Pygame.font.SysFont("comicsansms",115)
			TextSurf, TextRect = self.text_objects(self.name, largeText)
			TextRect.center = ((self.display_width/2),(self.display_height/2))
			self.gameDisplay.blit(TextSurf, TextRect)

			self.button("GO!",150,450,100,50,self.colors['green'],self.colors['bright_green'], self.game_loop)
			self.button("Quit",550,450,100,50,self.colors['red'],self.colors['bright_red'], self.quitgame)

			self.Pygame.display.update()
			self.clock.tick(15)

	def drawBoxs(self):
		self.gameDisplay.fill(self.colors['black'],(0,0,600,600))
		sx = 75
		sy = 75
		for i in range(10):
			x = sx + (i*50)
			if i in [0,3,6,9]:
				w = 3
			else:
				w = 1
			self.gameDisplay.fill(self.colors['white'],(x, 75, w, 450))

		for i in range(10):
			y = sy + (i*50)
			if i in [0,3,6,9]:
				w = 3
			else:
				w = 1
			self.gameDisplay.fill(self.colors['white'],(75, y, 450, w))
		
	def fillValues(self):
		sx = 75
		sy = 75
		w  = 50
		h  = 50
		for i in range(9):
			for j in range(9):
				if self.solver.PuzzleOBJ[j][i] == 0:
					continue
				val = str(self.solver.PuzzleOBJ[j][i])
				x = sx + (i*50)
				y = sy + (j*50)

				smallText = self.Pygame.font.SysFont("comicsansms",50)
				textSurf, textRect = self.text_objects(val, smallText,'red')
				textRect.center = ( (x+(w/2)), (y+(h/2)) )
				self.gameDisplay.blit(textSurf, textRect)

	def game_loop(self):
		while self.solver.Solve():
			self.gameDisplay.fill(self.colors['white'])



			self.drawBoxs()
			self.fillValues()
			self.Pygame.display.update()
			self.clock.tick(7)

			key =True
			while key:
				for event in self.Pygame.event.get():
					if event.type == self.Pygame.QUIT:
						self.Pygame.quit()
						# quit()

					if event.type == self.Pygame.KEYDOWN:
						key = False

	def quitgame(self):
		self.Pygame.quit()
		# quit()

class SudokuSolver(object):
	"""docstring for SudokuSolver"""
	def __init__(self, PuzzleOBJ):
		super(SudokuSolver, self).__init__()
		self.PuzzleOBJ = PuzzleOBJ
		self.getIntState()

	def getIntState(self):
		self.state = []
		for i in range(9):
			p_row = []
			for j in range(9):
				possible = []
				if self.PuzzleOBJ[i][j] == 0:
					possible = self.checkForPossible(i, j, True)
				p_row += [possible]
			self.state += [p_row]
		print(self.state)

	def getCurrState(self):
		for i in range(9):
			for j in range(9):
				if self.PuzzleOBJ[i][j] == 0:
					possible = self.checkForPossible(i,j, False)

	def checkForPossible(self, i, j, first_time = False):
		if first_time :
			possible = list(range(1,10))
		else:
			possible = self.state[i][j]

		for y in range(9):
			val = self.PuzzleOBJ[y][j]
			if val != 0 and val in possible:
				possible.remove(val)

		for x in range(9):
			val = self.PuzzleOBJ[i][x]
			if val != 0 and val in possible:
				possible.remove(val)

		sx = (i//3)*3
		sy = (j//3)*3
		for m in range(3):
			for n in range(3):
				val = self.PuzzleOBJ[sx+m][sy+n]
				if val != 0 and val in possible:
					possible.remove(val)

		return possible


	def ApplyAlgo1(self):
		for i in range(9):
			for j in range(9):
				if len(self.state[i][j]) == 1:
					self.PuzzleOBJ[i][j] = self.state[i][j][0]
					self.state[i][j] = []
					return True

		return False

	def Solve(self):
		updated = self.ApplyAlgo1()
		if updated :
			self.getCurrState()
		return True

if __name__ == '__main__':

	puzzle = getPuzzle('input.txt')

	solver = SudokuSolver(puzzle)
	game = GUI('sudokuSolver', solver)

	try:
		game.Dispaly()
		
	except Exception as e:
		game.Pygame.quit()
		raise e

