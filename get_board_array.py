import mss
import numpy as np
from PIL import Image
from config import BOARD_HEIGHT, BOARD_WIDTH
CELL_SIZE = 22
BOARD_X = 14
BOARD_Y = 111
COLOR_CODES = {
    (0, 0, 255): 1,
    (0, 123, 0): 2,
    (255, 0, 0): 3,
    (0, 0, 123): 4,
    (123, 0, 0): 5,
    (0, 123, 123): 6,
    (0, 0, 0): 7,
    (123, 123, 123): 8,
    (189, 189, 189): 0  #unopened/opened blank
}

def get_cell_type(cell) -> int:
	cell_type = COLOR_CODES[cell.getpixel((15, 16))]
	#cell_type=COLOR_CODES[cell.getpixel((13,14))]
	if cell_type == 0 and cell.getpixel((1, 16)) != (255, 255, 255):
		cell_type = -1
	return cell_type

def get_board_array() -> np.ndarray:
	with mss.mss() as sct:
		screenshot = sct.grab(sct.monitors[0])
		img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
		#board=img.crop((384,111,1044,463))
		board = img.crop((BOARD_X, BOARD_Y, BOARD_X + CELL_SIZE * BOARD_WIDTH, BOARD_Y + CELL_SIZE * BOARD_HEIGHT))
	width, height = board.size
	cell_imgs = [
	    board.crop((i, j, i + CELL_SIZE, j + CELL_SIZE)) for j in range(0, height, CELL_SIZE) for i in range(0, width, CELL_SIZE)
	]
	cells = np.fromiter((get_cell_type(cell) for cell in cell_imgs), dtype=np.int8)
	grid = np.reshape(cells, (BOARD_HEIGHT, BOARD_WIDTH))
	#surrond grid with -1(so you can make cell_surrondings with no errors)
	return np.concatenate(
	    (
	        np.full((1, BOARD_WIDTH + 2), -1, dtype=np.int8),  #top row of -1
	        np.insert(grid, (0, BOARD_WIDTH), -1, axis=1),  #fill sides with -1
	        np.full((1, BOARD_WIDTH + 2), -1, dtype=np.int8)
	    )
	)  #bottom row of -1
