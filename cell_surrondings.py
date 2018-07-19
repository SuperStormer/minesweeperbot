import numpy as np
from typing import Tuple
class CellSurrondings:
    def __init__(self,cell_surrondings:np.ndarray,cell_x:int,cell_y:int):
       self.cell_surrondings=cell_surrondings
       self.cell_x=cell_x
       self.cell_y=cell_y
    def get_cell_coordinates(self,indices:Tuple[int])->Tuple[int]:
        return self.cell_x+indices[0]-1,self.cell_y+indices[1]-1
    def get_empty_cells(self)->np.ndarray:
        return np.transpose(np.nonzero(self.cell_surrondings==0))
    def __iter__(self):
        return self.cell_surrondings