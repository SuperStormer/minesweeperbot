from dataclasses import InitVar, dataclass
from typing import Tuple

import numpy as np

#TODO use python 3.7 dataclasses
#IMPORTANT:indexing is [y,x] not [x,y]
@dataclass(frozen=True)
class CellSurrondings:
	x: int
	y: int
	cells: InitVar[np.ndarray]
	
	def __post_init__(self, cells: np.ndarray):
		self.cell_surrondings = cells[self.y:self.y + 3, self.x:self.x + 3]
		self.empty_cells = np.transpose(np.nonzero(self.cell_surrondings == 0)[::-1])
	
	def get_cell_coordinates(self, indices: np.ndarray) -> Tuple[int, int]:
		if 0 <= indices[0] <= 2 and 0 <= indices[1] <= 2:
			return self.x + indices[0] - 1, self.y + indices[1] - 1
		raise IndexError()
	
	def __iter__(self):
		return iter(self.cell_surrondings)
	
	def __repr__(self):
		return "CellSurrondings(cell_surrondings={0!r},x={1},y={2})".format(self.cell_surrondings, self.x, self.y)
