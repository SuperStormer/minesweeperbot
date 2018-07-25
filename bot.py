from os import getcwd
from subprocess import Popen
from time import sleep
from typing import Iterator, List, Tuple

import numpy as np
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

from cell_surrondings import CellSurrondings
from get_board_array import get_board_array

MINESWEEPER_URL="http://minesweeperonline.com/"
mouse= MouseController()
keyboard=KeyboardController()
mines=np.full((16,30),False)#IMPORTANT:0th axis is y, 1st axis is x so indexing is mines[y,x] not mines[x,y]
def is_mine_factory(cell_surrondings:CellSurrondings):
	def is_mine(indices:np.ndarray)->bool:
		coordinates=cell_surrondings.get_cell_coordinates(indices)
		if 0<=coordinates[0]<=29 and 0<=coordinates[1]<=15:
			return mines[coordinates[::-1]]
		else:
			return False	
	return is_mine
def click_cell(cell_x:int,cell_y:int):
	print("Clicked",cell_x,",",cell_y)
	mouse.position=(5+cell_x*16.5,85+cell_y*16.5)
	mouse.click(Button.left)
def get_effective_mines(cell_surrondings:CellSurrondings):
	is_mine=is_mine_factory(cell_surrondings)
	return cell_surrondings.cell_surrondings[1,1]-[is_mine(indices) for indices in cell_surrondings.get_empty_cells()].count(True)

def add_mines(cell_surrondings:CellSurrondings):
	is_mine=is_mine_factory(cell_surrondings)
	def filter_empty_cells(indices):
		return not is_mine(cell_surrondings.get_cell_coordinates(indices)) and cell_surrondings.cell_surrondings[tuple(indices)] != -1
	empty_cells:List[Tuple[int,int]]=list(filter(filter_empty_cells,cell_surrondings.get_empty_cells()))
	#if there are the same amount of unopened squares as the effective number of mines, they are all mines
	if len(empty_cells) == get_effective_mines(cell_surrondings):
		for indices in empty_cells:
			mines[cell_surrondings.get_cell_coordinates(indices)[::-1]]=True

def get_safe(cell_surrondings:CellSurrondings)->Iterator[Tuple[int,int]]:
	#there are no more unmarked mines
	if get_effective_mines(cell_surrondings)==0:
		return (cell_surrondings.get_cell_coordinates(indices) for indices in cell_surrondings.get_empty_cells())
#TODO detect win and stop while loop
with keyboard.pressed(Key.alt):
	keyboard.press(Key.tab)
	sleep(0.5)
	keyboard.release(Key.tab)
#webbrowser.open(MINESWEEPER_URL)
Popen("start website/main.html",cwd=getcwd(),shell=True)
sleep(0.5)
mouse.press(Button.left)
mouse.release(Button.left)
sleep(0.5)	
keyboard.press(Key.f11)
keyboard.release(Key.f11)
sleep(3)
click_cell(14,7)
while True:
	cells=get_board_array()
	print(cells)
	#add mines first
	for y,row in enumerate(cells[1:-1]):#the slice is to avoid the -1 paddings
		for x,cell in enumerate(row[1:-1]):
			if cell>0:
				cell_surrondings=CellSurrondings(cells[y:y+3,x:x+3],x,y)
				add_mines(cell_surrondings)
	#then get all safe squares
	for y,row in enumerate(cells[1:-1]):
		for x,cell in enumerate(row[1:-1]):
			if cell>0:
				cell_surrondings=CellSurrondings(cells[y:y+3,x:x+3],x,y)
				safe_cells=get_safe(cell_surrondings)
				if safe_cells is not None:
					for cell in safe_cells:
						click_cell(*cell)
	sleep(0.4)				
