import mss
import numpy as np
from PIL import Image

CELL_SIZE=20
color_codes={
		(0, 0, 255): 1,
		(0, 123, 0): 2,
		(255, 0, 0): 3,
		(0, 0, 123): 4,
		(123, 0, 0): 5,
		(0, 123, 123): 6,
		(0, 0, 0): 7,
		(123, 123, 123): 8,
		(189, 189, 189): 0#unopened/opened blank 
	} 
def get_cell_type(cell):
	cell_type=color_codes[cell.getpixel((15,16))]
	if cell_type == 0 and cell.getpixel((1,16)) != (255,255,255):
		cell_type=-1
	return cell_type

def get_board_array():
	with mss.mss() as sct:
		screenshot=sct.grab(sct.monitors[0])
		img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
		#board=img.crop((384,111,1044,463))
		board=img.crop((13,101,613,421))
		board.save("temp/board.png")
	width,height=board.size
	cell_imgs=[board.crop((i,j,i+CELL_SIZE,j+CELL_SIZE)) for j in range(0,height,CELL_SIZE) for i in range(0,width,CELL_SIZE)]
	#take the color from (15,16) and identify number based on color 
	cells=np.fromiter((get_cell_type(cell) for cell in cell_imgs),dtype=np.int8)
	return np.reshape(cells,(16,30))
