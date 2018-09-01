import itertools
from multiprocessing import Pool
from os import getcwd
from random import randint
from subprocess import Popen
from time import sleep
from typing import Callable, Iterator, List, Optional, Tuple

import mss
import numpy as np
from PIL import Image
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
from scipy.ndimage import label

from cell_surrondings import CellSurrondings
from get_board_array import get_board_array

mouse=MouseController()
keyboard=KeyboardController()
mines=np.full((16,30),False) #IMPORTANT:0th axis is y, 1st axis is x so indexing is mines[y,x] not mines[x,y]
def is_mine_factory(cell_surrondings:CellSurrondings)->Callable[[np.ndarray],bool]:
	def is_mine(indices:np.ndarray)->bool:
		coordinates=cell_surrondings.get_cell_coordinates(indices)
		if 0<=coordinates[0]<=29 and 0<=coordinates[1]<=15:
			return mines[coordinates[::-1]]
		return False	
	return is_mine
#filters out mines
#TODO:replace this with operator.not on is_mine
def is_safe_cell_factory(cell_surrondings:CellSurrondings)->Callable[[np.ndarray],bool]:
	is_mine=is_mine_factory(cell_surrondings)
	def is_safe_cell(indices:np.ndarray)->bool:
		return not is_mine(indices)# and cell_surrondings.cell_surrondings[tuple(indices)] != -1
	return is_safe_cell	
def click_cell(x:int,y:int):
	mouse.position=(20+x*22,115+y*22)
	mouse.click(Button.left)
def get_effective_mines(cell_surrondings:CellSurrondings)->int:
	is_mine=is_mine_factory(cell_surrondings)
	#get the number of mines around the cell
	cell_mine_count=cell_surrondings.cell_surrondings[1,1]
	return cell_mine_count-[is_mine(indices) for indices in cell_surrondings.empty_cells].count(True)

def add_mines(cell_surrondings:CellSurrondings):
	empty_cells:List[Tuple[int,int]]=list(filter(is_safe_cell_factory(cell_surrondings),cell_surrondings.empty_cells))
	#if there are the same amount of unopened squares as the effective number of mines, they are all mines
	if len(empty_cells) == get_effective_mines(cell_surrondings):
		for indices in empty_cells:
			mines[cell_surrondings.get_cell_coordinates(indices)[::-1]]=True

def get_safe(cell_surrondings:CellSurrondings)->Optional[Iterator[Tuple[int,int]]]:
	#there are no more unmarked mines
	if get_effective_mines(cell_surrondings)==0:
		is_safe_cell=is_safe_cell_factory(cell_surrondings)
		return (cell_surrondings.get_cell_coordinates(indices) for indices in cell_surrondings.empty_cells if is_safe_cell(indices))
	return None
def normal_solver(cells:np.ndarray):
	#add mines first
	for y,row in enumerate(cells[1:-1]):#the slice is to avoid the -1 paddings
		for x,cell in enumerate(row[1:-1]):
			if cell>0:
				cell_surrondings=CellSurrondings(x,y,cells)
				add_mines(cell_surrondings)
	#then get all safe squares
	clicked_safe=False
	for y,row in enumerate(cells[1:-1]):
		for x,cell in enumerate(row[1:-1]):
			if cell>0:
				cell_surrondings=CellSurrondings(x,y,cells)
				safe_cells=get_safe(cell_surrondings)
				if safe_cells is not None:
					for safe_cell in safe_cells:
						click_cell(*safe_cell)
						clicked_safe=True
	return clicked_safe	
def is_border(cell_surrondings:CellSurrondings)->bool:
	is_unopened=cell_surrondings.cell_surrondings[1,1]== 0
	is_mine=mines[cell_surrondings.y,cell_surrondings.x] 
	touches_opened_cell =(cell_surrondings.cell_surrondings>0).any()
	return is_unopened and not is_mine and touches_opened_cell
def is_valid_flagging(flags:Tuple[bool,...],region:np.ndarray,cells:np.ndarray)->bool:
	flag_coords=[region[index] for index in np.nonzero(flags)[0]]
	if len(mines.nonzero()[0])+len(flag_coords)<=99:#99 is number of mines
		#not any of them are invalid
		return not any(cell>0 and not is_valid_flagging_single(CellSurrondings(x,y,cells),flag_coords) for y,row in enumerate(cells[1:-1]) for x,cell in enumerate(row[1:-1]))
	return False	
#returns if the flagging is valid per square(even if there is no flagging)
#TODO:reimplement this
def is_valid_flagging_single(cell_surrondings:CellSurrondings,flag_coords:np.ndarray):
	flag_coords_tuples:Iterator[Tuple[int,int]]=map(tuple,flag_coords) # type: ignore
	num_proposed_flagging=[cell_surrondings.get_cell_coordinates(indices) in flag_coords_tuples for indices in cell_surrondings.empty_cells].count(True)
	return num_proposed_flagging == get_effective_mines(cell_surrondings)
def get_solution(args):
	flags,region,cells=args
	if is_valid_flagging(flags,region,cells):
		return flags
	return None	
			
#TODO finish implementing this
def tank_solver(cells:np.ndarray)->bool:
	border_cells=np.reshape(np.fromiter((is_border(CellSurrondings(x,y,cells)) for y,row in enumerate(cells[1:-1]) for x,cell in enumerate(row[1:-1])),dtype=bool),(16,30))
	labels,num_labels=label(border_cells)
	segregated_regions=[np.transpose((labels==i).nonzero()) for i in range(1,num_labels+1)]
	clicked_safe=False
	for region in segregated_regions:#also indexed [y,x]
		flag_permutations=itertools.product([False,True],repeat=len(region))
		solutions:List[Tuple[int,...]]=[flags for flags in flag_permutations if is_valid_flagging(flags,region,cells) if is_valid_flagging(flags,region,cells)]
		"""
		with Pool() as pool:
			solutions=[x for x in pool.imap_unordered(get_solution,zip(flag_permutations,itertools.repeat(region),itertools.repeat(cells)),15)]
		"""
		stacked_solutions=np.vstack(solutions)		
		#all of the cells that are always mines in the solutions
		mine_cells=(region[i] for i,is_mine in enumerate(np.apply_along_axis(lambda x:x.all(),0,stacked_solutions)) if is_mine)
		#all of the cells that are always not mines in the solutions
		safe_cells=(region[i] for i,is_safe in enumerate(np.apply_along_axis(lambda x:not x.any(),0,stacked_solutions)) if is_safe)
		for cell in mine_cells:
			mines[cell[::-1]]=True
		for cell in safe_cells:
			click_cell(*cell)
			clicked_safe=True
	return clicked_safe


def guess(cells:np.ndarray):
	x=randint(0,29)
	y=randint(0,15)
	if not mines[y,x] and cells[y,x]== 0:
		click_cell(x,y)
	else:
		guess(cells)

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
		clicked_safe=normal_solver(cells)
		if not clicked_safe:
			clicked_safe=tank_solver(cells)
			if not clicked_safe:
				guess(cells[1:-1,1:-1])
		with mss.mss() as sct:
			screenshot=sct.grab(sct.monitors[0])
			img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
			is_win=img.getpixel((30,480))==(255,0,0)		
		sleep(0.05)	
if __name__=="__main__":
	main()
