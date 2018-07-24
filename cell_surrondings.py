from typing import Tuple

import numpy as np


class CellSurrondings:
    def __init__(self,cell_surrondings:np.ndarray,cell_x:int,cell_y:int):
       self.cell_surrondings=cell_surrondings
       self.cell_x=cell_x
       self.cell_y=cell_y
    def get_cell_coordinates(self,indices:np.ndarray)->Tuple[int,int]:
        return self.cell_x+indices[0]-1,self.cell_y+indices[1]-1
    def get_empty_cells(self)->np.ndarray:
        #returns in x,y pairs
        #needs to reverse to return in x,y pairs
        return np.fromiter((indices[::-1] for indices in np.transpose(np.nonzero(self.cell_surrondings==0))),dtype=np.int8)
    def __iter__(self):
        return self.cell_surrondings
    def __repr__(self):
        return "CellSurrondings({0!r})".format(self.__dict__)
