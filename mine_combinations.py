from __future__ import annotations

import itertools

from cell_surrondings import CellSurrondings  # pylint: disable=E0611
from dataclasses import dataclass
from typing import Set, Tuple

@dataclass
class MineCombinations:
	empty_cells: Set[Tuple[int, int]]
	combinations: Set[Tuple[Tuple[int, int], ...]]
	
	@classmethod
	def from_cell_surrondings(cls, cell_surrondings: CellSurrondings, mines: int):
		empty_cells = set(cell_surrondings.get_cell_coordinates(indices) for indices in cell_surrondings.empty_cells)
		combinations = set(
			itertools.combinations(
			(cell_surrondings.get_cell_coordinates(indices) for indices in cell_surrondings.empty_cells), mines
			)
		)
		return cls(empty_cells, combinations)
	
	@classmethod
	def merge_combos(cls, combos1: MineCombinations, combos2: MineCombinations) -> MineCombinations:
		empty_cell_intersection = combos1.empty_cells & combos2.empty_cells
		if empty_cell_intersection == set():
			return None
		combined_empty_cells = combos1.empty_cells | combos2.empty_cells
		#itertools.product(combos1, combos2)
		valid_products = {
			tuple(set(combo1) & set(combo2))
			for combo1 in combos1.combinations
			for combo2 in combos2.combinations if set(combo1) | empty_cell_intersection == set(combo2) | empty_cell_intersection
		}
		return cls(combined_empty_cells, valid_products)
