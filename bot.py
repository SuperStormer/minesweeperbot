import webbrowser
from time import sleep
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
cells=get_board_array()
print(cells)	
		
		
	
