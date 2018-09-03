from typing import Tuple

import numpy as np
#IMPORTANT:indexing is [y,x] not [x,y]
cdef class CellSurrondings:
	cdef public cell_surrondings
	cdef public int x
	cdef public int y
	cdef public empty_cells
	cpdef __init__(self,int x,int y,cells):
		self.cell_surrondings=cells[y:y+3,x:x+3]
		self.x=x
		self.y=y
		self.empty_cells=np.transpose(np.nonzero(self.cell_surrondings==0)[::-1])
	cpdef (int,int) get_cell_coordinates(self,indices):
		if 0<=indices[0]<=2 and 0<=indices[1]<=2:
			return self.x+indices[0]-1,self.y+indices[1]-1
		raise IndexError()	

	def __iter__(self):
		return iter(self.cell_surrondings)
	def __repr__(self):
		return "CellSurrondings({0!r})".format(self.__dict__)

