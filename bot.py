from os import getcwd
from subprocess import Popen
from time import sleep
from typing import Callable, Iterator, List, Tuple
from random import randint
import mss
import numpy as np
from PIL import Image
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

from cell_surrondings import CellSurrondings
from get_board_array import get_board_array

mouse=MouseController()
keyboard=KeyboardController()
mines=np.full((16,30),False)#IMPORTANT:0th axis is y, 1st axis is x so indexing is mines[y,x] not mines[x,y]
def is_mine_factory(cell_surrondings:CellSurrondings)->Callable[[np.ndarray],bool]:
	def is_mine(indices:np.ndarray)->bool:
		coordinates=cell_surrondings.get_cell_coordinates(indices)
		if 0<=coordinates[0]<=29 and 0<=coordinates[1]<=15:
			return mines[coordinates[::-1]]
		return False	
	return is_mine
#filters out mines	
def is_safe_cell_factory(cell_surrondings:CellSurrondings)->Callable[[np.ndarray],bool]:
	is_mine=is_mine_factory(cell_surrondings)
	def is_safe_cell(indices:np.ndarray)->bool:
		return not is_mine(indices) and cell_surrondings.cell_surrondings[tuple(indices)] != -1
	return is_safe_cell	
def click_cell(cell_x:int,cell_y:int):
	print("Clicked",cell_x,",",cell_y)
	mouse.position=(20+cell_x*22,115+cell_y*22)
	mouse.click(Button.left)
def get_effective_mines(cell_surrondings:CellSurrondings)->int:
	is_mine=is_mine_factory(cell_surrondings)
	#get the number of mines around the cell
	cell_mine_count=cell_surrondings.cell_surrondings[1,1]
	return cell_mine_count-[is_mine(indices) for indices in cell_surrondings.get_empty_cells()].count(True)

def add_mines(cell_surrondings:CellSurrondings):
	empty_cells:List[Tuple[int,int]]=list(filter(is_safe_cell_factory(cell_surrondings),cell_surrondings.get_empty_cells()))
	#if there are the same amount of unopened squares as the effective number of mines, they are all mines
	if len(empty_cells) == get_effective_mines(cell_surrondings):
		for indices in empty_cells:
			mines[cell_surrondings.get_cell_coordinates(indices)[::-1]]=True

def get_safe(cell_surrondings:CellSurrondings)->Iterator[Tuple[int,int]]:
	#there are no more unmarked mines
	if get_effective_mines(cell_surrondings)==0:
		is_safe_cell:Callable=is_safe_cell_factory(cell_surrondings)
		return (cell_surrondings.get_cell_coordinates(indices) for indices in cell_surrondings.get_empty_cells() if is_safe_cell(indices))
def main():
	with keyboard.pressed(Key.alt):
		keyboard.press(Key.tab)
		sleep(0.5)
		keyboard.release(Key.tab)
	sleep(0.1)	
	Popen("start website/main.html",cwd=getcwd(),shell=True)
	sleep(0.5)
	mouse.press(Button.left)
	mouse.release(Button.left)
	sleep(0.5)	
	keyboard.press(Key.f11)
	keyboard.release(Key.f11)
	sleep(3)
	click_cell(14,7)
	is_win=False
	while not is_win:
		cells=get_board_array()
		print(cells)
		#add mines first
		for y,row in enumerate(cells[1:-1]):#the slice is to avoid the -1 paddings
			for x,cell in enumerate(row[1:-1]):
				if cell>0:
					cell_surrondings=CellSurrondings(cells[y:y+3,x:x+3],x,y)
					add_mines(cell_surrondings)
		#then get all safe squares
		clicked_safe=False
		for y,row in enumerate(cells[1:-1]):
			for x,cell in enumerate(row[1:-1]):
				if cell>0:
					cell_surrondings=CellSurrondings(cells[y:y+3,x:x+3],x,y)
					safe_cells=get_safe(cell_surrondings)
					if safe_cells is not None:
						for safe_cell in safe_cells:
							click_cell(*safe_cell)
							clicked_safe=True
		if not clicked_safe:
			click_cell(randint(0,29),randint(0,15))
		with mss.mss() as sct:
			screenshot=sct.grab(sct.monitors[0])
			img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
			is_win=img.getpixel((30,480))==(255,0,0)		
		sleep(0.4)	
if __name__=="__main__":
	main()
