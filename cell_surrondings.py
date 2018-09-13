from typing import Tuple

import numpy as np
#IMPORTANT:indexing is [y,x] not [x,y]
class CellSurrondings:
	def __init__(self,x:int,y:int,cells:np.ndarray):
		self.cell_surrondings=cells[y:y+3,x:x+3]
		self.x=x
		self.y=y
		self.empty_cells=np.transpose(np.nonzero(self.cell_surrondings==0)[::-1])
	def get_cell_coordinates(self,indices:np.ndarray)->Tuple[int,int]:
		if 0<=indices[0]<=2 and 0<=indices[1]<=2:
			return self.x+indices[0]-1,self.y+indices[1]-1
		raise IndexError()	

	def __iter__(self):
		return iter(self.cell_surrondings)
	def __repr__(self):
		return "CellSurrondings(cell_surrondings={0!r},x={1},y={2})".format(self.cell_surrondings,self.x,self.y)

