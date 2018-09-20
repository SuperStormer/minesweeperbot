import hypothesis.strategies as st
import numpy as np
from hypothesis import assume, given

from bot import is_valid_flagging, is_valid_flagging_single  # pylint: disable=E0611

from cell_surrondings import CellSurrondings  # pylint: disable=E0611

cells = np.array([[-1, -1, -1, -1, -1], [-1, 0, 0, 0, -1], [-1, 0, 8, 0, -1], [-1, 0, 0, 0, -1], [-1, -1, -1, -1, -1]])
region = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]])
all_eight = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]])

def test_is_valid_flagging_true():
	assert is_valid_flagging(all_eight, region, cells)

@given(st.lists(st.tuples(st.integers(0, 2), st.integers(0, 2)), max_size=200, unique=True))
def test_is_valid_flagging_false(flags):
	#flags=np.array([[0,0],[2,2]])
	assume(not np.array_equal(flags, np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]])))
	assert not is_valid_flagging(np.array(flags), region, cells)

#@given(st.lists(st.tuples(st.integers(0,8),st.integers(0,8)),max_size=200,unique=True))
#def test_is_valid_flagging_errors(flags):
#	is_valid_flagging(np.array(flags),region,cells)
def test_is_valid_flagging_single_true():
	cell_surrondings = CellSurrondings(1, 1, cells)
	assert is_valid_flagging_single(cell_surrondings, list(map(tuple, all_eight)))

@given(st.lists(st.tuples(st.integers(0, 2), st.integers(0, 2)), max_size=200, unique=True))
def test_is_valid_flagging_single_false(flags):
	assume(not np.array_equal(flags, np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]])))
	np.seterr(all='raise')
	print(cells)
	assert not is_valid_flagging_single(CellSurrondings(1, 1, cells), flags)
