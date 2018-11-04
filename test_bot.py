import numpy as np
import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

from bot import is_valid_flagging  # pylint: disable=E0611
from bot import is_valid_flagging_single  # pylint: disable=E0611
from cell_surrondings import CellSurrondings  # pylint: disable=E0611

cells = np.array([[-1, -1, -1, -1, -1], [-1, 0, 0, 0, -1], [-1, 0, 8, 0, -1], [-1, 0, 0, 0, -1], [-1, -1, -1, -1, -1]])
all_eight = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]])

# yapf: disable
@pytest.mark.parametrize(
	"flags,region,cells", [
	((True, True, True, True, True, True, True, True), all_eight, cells),
	(
	(True, True, False, True),
	np.array([[0, 1], [1, 1], [2, 1], [2, 0]]),
	np.array([[-1, -1, -1, -1, -1], [-1, 2, 0, 0, -1], [-1, 3, 0, 0, -1], [-1, 0, 0, 0, -1], [-1, -1, -1, -1, -1]])
	),
	(
	(False, True, True, False, False, True, False, True, True, True, True, True, True,
	True, True, True, True, True, True, True, True, True, True, True, True, True, True),
	np.array([
	[ 5, 10],
	[ 5, 11],
	[ 5, 12],
	[ 5, 13],
	[ 5, 14],
	[ 5, 15],
	[ 5, 16],
	[ 5, 17],
	[ 6, 17],
	[ 7, 17],
	[ 7, 18],
	[ 8, 18],
	[ 9, 18],
	[10, 18],
	[10, 19],
	[10, 20],
	[11, 20],
	[12, 20],
	[12, 21]]),
	np.array([
	[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # pylint:disable=C0326
	[-1,  0,  0,  0,  0,  1, -1, -1,  1,  1,  1, -1, -1], # pylint:disable=C0326
	[-1,  0,  0,  4,  2,  1,  1,  1,  2,  0,  1, -1, -1], # pylint:disable=C0326
	[-1,  0,  0,  2, -1, -1,  2,  0,  3,  2,  3,  3, -1], # pylint:disable=C0326
	[-1,  0,  0,  2,  1, -1,  2,  0,  3,  2,  0,  0, -1], # pylint:disable=C0326
	[-1,  0,  0,  0,  2,  1,  2,  2,  3,  0,  4,  3, -1], # pylint:disable=C0326
	[-1,  0,  0,  3,  3,  0,  1,  2,  0,  4,  0,  1, -1], # pylint:disable=C0326
	[-1,  1,  2,  0,  3,  2,  1,  2,  0,  4,  2,  1, -1], # pylint:disable=C0326
	[-1, -1,  1,  2,  0,  1, -1,  2,  3,  0,  1, -1, -1], # pylint:disable=C0326
	[-1, -1,  1,  2,  2,  1, -1,  1,  0,  2,  1, -1, -1], # pylint:disable=C0326
	[-1, -1,  1,  0,  2,  1,  1,  1,  1,  2,  1,  1, -1], # pylint:disable=C0326
	[-1, -1,  2,  2,  4,  0,  3,  1, -1,  1,  0,  1, -1], # pylint:disable=C0326
	[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]  # pylint:disable=C0326
	])
	)
	]
)
#yapf: enable
def test_is_valid_flagging_true(flags, region, cells):
	assert is_valid_flagging(flags, region, cells)

# yapf: disable
@pytest.mark.parametrize(
	"invalid_flags,region,cells", [
	(((True, True, True, True, True, True, True, True),), all_eight, cells),
	(
	((True, True, False, True), (True, True, True, False)), np.array([[0, 1], [1, 1], [2, 1], [2, 0]]),
	np.array([
	[-1, -1, -1, -1, -1],
	[-1, 2, 0, 0, -1],
	[-1, 3, 0, 0, -1],
	[-1, 0, 0, 0, -1],
	[-1, -1, -1, -1, -1]])
	)
	]
)
# yapf: enable
@given(
	data=st.data()
	#flags=st.tuples(
	#st.booleans(), st.booleans(), st.booleans(), st.booleans(), st.booleans(), st.booleans(), st.booleans(), st.booleans()
	#)
)
def test_is_valid_flagging_false(data, invalid_flags, region, cells):
	flags = tuple(data.draw(st.lists(st.booleans(), min_size=len(invalid_flags), max_size=len(invalid_flags))))
	assume(not flags in invalid_flags)
	assert not is_valid_flagging(flags, region, cells)

#@given(st.lists(st.tuples(st.integers(0,8),st.integers(0,8)),max_size=200,unique=True))
#def test_is_valid_flagging_errors(flags):
#	is_valid_flagging(np.array(flags),region,cells)
def test_is_valid_flagging_single_true():
	cell_surrondings = CellSurrondings(1, 1, cells)
	assert is_valid_flagging_single(cell_surrondings, list(map(tuple, all_eight)))  #type:ignore

@given(st.lists(st.tuples(st.integers(0, 2), st.integers(0, 2)), max_size=200, unique=True))
def test_is_valid_flagging_single_false(flags):
	assume(sorted(flags) != [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)])
	assume((1, 1) not in flags)
	assert not is_valid_flagging_single(CellSurrondings(1, 1, cells), flags)
