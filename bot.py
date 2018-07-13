import webbrowser
from time import sleep
import mss
from PIL import Image
from get_board_array import get_board_array
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

MINESWEEPER_URL="http://minesweeperonline.com/"
mouse= MouseController()
keyboard=KeyboardController()
with keyboard.pressed(Key.alt):
	keyboard.press(Key.tab)
	sleep(0.5)
	keyboard.release(Key.tab)
webbrowser.open(MINESWEEPER_URL)
sleep(0.5)
mouse.press(Button.left)
mouse.release(Button.left)
sleep(0.5)	
keyboard.press(Key.f11)
keyboard.release(Key.f11)
sleep(4)
with mss.mss() as sct:
		screenshot=sct.grab(sct.monitors[0])
		img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
		board=img.crop((384,111,1044,463))
		board.save("temp/board.png")
		board.show()
		cells=get_board_array(board)
		print(cells)	
		
		
	
