import webbrowser
from time import sleep
from get_board_array import get_board_array
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
from cell_surrondings import CellSurrondings
from collections import Counter
import numpy as np
from typing import Tuple,List
from subprocess import Popen
from os import getcwd
MINESWEEPER_URL="http://minesweeperonline.com/"
mouse= MouseController()
keyboard=KeyboardController()
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
sleep(4)
mines=np.full((16,30),False)
def is_mine_factory(cell_surrondings:CellSurrondings):
	def is_mine(indices:Tuple[int,int]):
		return mines[cell_surrondings.get_cell_coordinates(indices)]
	return is_mine	
def get_effective_mines(cell_surrondings:CellSurrondings):
	is_mine=is_mine_factory(cell_surrondings)
	return [is_mine(indices) for indices in cell_surrondings.get_empty_cells()].count(True)

def add_mines(cell_surrondings:CellSurrondings):
	empty_cells:List[Tuple[int,int]]=list(filter(is_mine_factory(cell_surrondings),cell_surrondings.get_empty_cells()))
	#if there are the same amount of unopened squares as the effective number of mines, they are all mines
	if len(empty_cells) == get_effective_mines(cell_surrondings):
		for indices in empty_cells:
			mines[cell_surrondings.get_cell_coordinates(indices)]=True
def get_safe(cell_surrondings:CellSurrondings):
	#there are no more unmarked mines
	if get_effective_mines(cell_surrondings)==0:
		return cell_surrondings.get_empty_cells()
cells=get_board_array()
print(cells)	
		
		
	
