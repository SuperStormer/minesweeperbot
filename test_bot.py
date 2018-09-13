import unittest
import numpy as np
from bot import is_valid_flagging # pylint: disable=E0611
cells=np.array([[0,0,0],[0,8,0],[0,0,0]])
region=np.array([[0,0],[0,1],[0,2],[1,0],[1,2],[2,0],[2,1],[2,2]])
def test_is_valid_flagging_true():
	flags=np.array([[0,0],[0,1],[0,2],[1,0],[1,2],[2,0],[2,1],[2,2]])
	assert is_valid_flagging(flags,region,cells)
def test_is_valid_flagging_false():
	flags=np.array([[0,0],[2,2]])
	assert not is_valid_flagging(flags,region,cells)

if __name__ == '__main__':
	unittest.main()