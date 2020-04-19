import pygame, sys
import time
import numpy as np
import re
from random import randint

def MAKEME(lis):
	s = ''
	l=[]
	for i in range(1,10):
		if i in lis:
			s+=str(i)+ ' '
		else:
			s+='  '
		if i%3==0:
			l+=[s]
			s=''
	return l

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

		while True:
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
					val = MAKEME(self.solver.state_POS[j][i])
					for v in range(3):

						x = sx + (i*50)
						y = sy + (j*50)

						smallText = self.Pygame.font.SysFont("comicsansms",20)
						textSurf, textRect = self.text_objects(val[v], smallText,'green')
						textRect.center = ( (x+(w/2)), (y+((h/6)*(v+1)*1.5)) )
						self.gameDisplay.blit(textSurf, textRect)
				else:
					val = str(self.solver.PuzzleOBJ[j][i])
					x = sx + (i*50)
					y = sy + (j*50)

					smallText = self.Pygame.font.SysFont("comicsansms",50)
					textSurf, textRect = self.text_objects(val, smallText,'red')
					textRect.center = ( (x+(w/2)), (y+(h/2)) )
					self.gameDisplay.blit(textSurf, textRect)

	def game_loop(self):
		while not self.solver.Solve():
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

		while True:
			for event in self.Pygame.event.get():
				if event.type == self.Pygame.QUIT:
					self.Pygame.quit()
					# quit()
					
			if self.solver.issolved():

				self.gameDisplay.fill(self.colors['white'])
				self.drawBoxs()
				self.fillValues()
				self.button("SOLVED",650,285,150,50,self.colors['green'],self.colors['bright_green'], self.Dispaly)
				self.Pygame.display.update()
				self.clock.tick(7)
			else:
				self.gameDisplay.fill(self.colors['white'])
				self.drawBoxs()
				self.fillValues()
				self.button("FAIL",650,285,150,50,self.colors['red'],self.colors['bright_red'], self.Dispaly)
				self.Pygame.display.update()
				self.clock.tick(7)


	def quitgame(self):
		self.Pygame.quit()
		# quit()

class SudokuSolver(object):
	"""docstring for SudokuSolver"""
	def __init__(self, PuzzleOBJ):
		super(SudokuSolver, self).__init__()
		self.PuzzleOBJ = PuzzleOBJ
		self.getIntState()
		self.getCurrState()

	def getIntState(self):
		# for each cell[9x9x[possible]], possible values
		self.state_POS = [[list(range(1,10)) for i in range(9)] for j in range(9)]
		# for each row[9x[possible]], possible values
		# self.state_ROW = [list(range(1,10)) for i in range(9)]
		# for each col[9x[possible]], possible values
		# self.state_COL = [list(range(1,10)) for i in range(9)]
		# for each box[9x[possible]], possible values
		# self.state_BOX = [list(range(1,10)) for i in range(9)]

	def getCurrState(self):
		for i in range(9):
			for j in range(9):
				val = self.PuzzleOBJ[i][j]

				if val == 0:
					self.checkForPossible(i,j)
					continue
				else:
					self.state_POS[i][j] = []

				# if val in self.state_ROW[i]:
				# 	self.state_ROW[i].remove(val)
				# if val in self.state_COL[j]:
				# 	self.state_COL[j].remove(val)

				# ind = (i//3)*3+(j//3)

				# if val in self.state_BOX[ind]:
				# 	self.state_BOX[ind].remove(val)



		# print('state_POS',self.state_POS)
		# print('state_ROW',self.state_ROW)
		# print('state_COL',self.state_COL)
		# print('state_BOX',self.state_BOX)

	def issolved(self):
		matr = [list(range(1,10)) for i in range(9)]
		matc = [list(range(1,10)) for i in range(9)]
		matb = [list(range(1,10)) for i in range(9)]
		for i in range(9):
			for j in range(9):
				val = self.PuzzleOBJ[i][j]

				ind = (i//3)*3+(j//3)

				if  matr[i][val-1] == val:
					matr[i][val-1] =  0
				else:
					return False
				if  matc[j][val-1] == val:
					matc[j][val-1] =  0
				else:
					return False

				if  matb[ind][val-1] == val:
					matb[ind][val-1] =  0
				else:
					return False


		return True

	def checkForPossible(self, i, j):
		possible = self.state_POS[i][j]

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

		return


	def ApplyAlgo1(self):
		for i in range(9):
			for j in range(9):
				if len(self.state_POS[i][j]) == 1:
					self.PuzzleOBJ[i][j] = self.state_POS[i][j][0]
					self.state_POS[i][j] = []
					return True

		return False

	def ApplyAlgo2(self):

		# row_num
		for i in range(9):
			temp_dict = {}
			temp_dict2 = {}
			for j in range(9):
				for n in self.state_POS[i][j]:
					temp_dict[n]  = temp_dict.get(n,0)+1
					temp_dict2[n] = (i, j)

			for n in temp_dict:
				if temp_dict[n] == 1:
					r,c = temp_dict2[n]
					self.PuzzleOBJ[r][c] = n
					self.state_POS[r][c] = []
					# print('row')
					return True
		# col_num
		for j in range(9):
			temp_dict = {}
			temp_dict2 = {}
			for i in range(9):
				for n in self.state_POS[i][j]:
					temp_dict[n]  = temp_dict.get(n,0)+1
					temp_dict2[n] = (i, j)

			for n in temp_dict:
				if temp_dict[n] == 1:
					r,c = temp_dict2[n]
					self.PuzzleOBJ[r][c] = n
					self.state_POS[r][c] = []
					# print('col')
					return True

		for box in range(9):
			temp_dict = {}
			temp_dict2 = {}

			ibase = (box//3)*3
			jbase = (box%3)*3

			for i in range(3):
				for j in range(3):

					for n in self.state_POS[i+ibase][j+jbase]:
						temp_dict[n]  = temp_dict.get(n,0)+1
						temp_dict2[n] = (i+ibase, j+jbase)

			for n in temp_dict:
				if temp_dict[n] == 1:
					r,c = temp_dict2[n]
					self.PuzzleOBJ[r][c] = n
					self.state_POS[r][c] = []
					# print('Box')
					return True

		return False

	def ApplyAlgo3(self):
		# row_num
		print('entry')
		STATE = False
		for i in range(9):
			temp_dict = {}
			temp_dict2 = {}
			for j in range(9):
				for n in self.state_POS[i][j]:
					if (j//3) not in temp_dict.get(n,[]):
						temp_dict[n]  = temp_dict.get(n,[]) + [j//3]
					temp_dict2[n] = (i, j)

			for n in temp_dict:
				if len(temp_dict[n]) == 1:
					i,j = temp_dict2[n]
					ibase = (i//3)*3
					jbase = (j//3)*3

					for r in range(3):
						for c in range(3):
							if ibase+r == i:
								continue
							if n in self.state_POS[ibase+r][jbase+c]:
								self.state_POS[ibase+r][jbase+c].remove(n)
								STATE = True
								print('removed0',ibase+r,jbase+c, n)


		# col_num
		for j in range(9):
			temp_dict = {}
			temp_dict2 = {}
			for i in range(9):
				for n in self.state_POS[i][j]:
					if (i//3) not in temp_dict.get(n,[]):
						temp_dict[n]  = temp_dict.get(n,[]) + [i//3]
					temp_dict2[n] = (i, j)

			for n in temp_dict:
				if len(temp_dict[n]) == 1:
					i,j = temp_dict2[n]
					ibase = (i//3)*3
					jbase = (j//3)*3

					for r in range(3):
						for c in range(3):
							if jbase+c == j:
								continue
							if n in self.state_POS[ibase+r][jbase+c]:
								self.state_POS[ibase+r][jbase+c].remove(n)
								STATE = True
								print('removed2',ibase+r,jbase+c, n)

		# box_num
		for box in range(9):
			temp_dict_r  = {}
			temp_dict_c  = {}
			temp_dict_r2 = {}
			temp_dict_c2 = {}

			ibase = (box//3)*3
			jbase = (box%3 )*3

			for i in range(3):
				for j in range(3):
					for n in self.state_POS[i+ibase][j+jbase]:
						if (i) not in temp_dict_r.get(n,[]):
							temp_dict_r[n]  = temp_dict_r.get(n,[]) + [i]
							temp_dict_r2[n] = (i+ibase, j+jbase)

						if (j) not in temp_dict_c.get(n,[]):
							temp_dict_c[n]  = temp_dict_c.get(n,[]) + [j]
							temp_dict_c2[n] = (i+ibase, j+jbase)
							

			for n in temp_dict_r :
				if len(temp_dict_r[n]) == 1:

					r,c = temp_dict_r2[n]

					for col in range(9):
						if c//3 == col//3:
							continue
						if n in self.state_POS[r][col] :
							self.state_POS[r][col].remove(n)
							STATE = True
							print('removed3',r,c,col,n)

			for n in temp_dict_c :
				if len(temp_dict_c[n]) == 1:

					r,c = temp_dict_c2[n]

					for row in range(9):
						if r//3 == row//3:
							continue
						if n in self.state_POS[row][c] :
							self.state_POS[row][c].remove(n)
							STATE = True
							print('removed4',r,c,row,n)
				
		return STATE

	def Solve(self):
		updated = self.ApplyAlgo1()

		if not updated:
			updated = self.ApplyAlgo2()

		if not updated:
			updated = self.ApplyAlgo3()


		if updated :
			self.getCurrState()
			return False
		# print(self.state_POS)
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

