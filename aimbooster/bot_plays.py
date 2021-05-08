from utils import grab_screen
import numpy as np
import win32gui, win32ui, win32con, win32api
import cv2
import time
import matplotlib.pyplot as plt 
import time
import keyboard


def threshold_slow(image):
	    # grab the image dimensions
    h = image.shape[0]
    w = image.shape[1]
    
    # loop over the image, pixel by pixel
    for x in range(0,w,5):
        for y in range(0,h,5):
        	r,g,b = image[y,x]
        	#print(r,g,b)
        	if (r == 255) & (g == 219) & (b == 195):
        		click(150+x, 320+y)
        		#time.sleep(0.1)
        		break

def click(x,y):	
	win32api.SetCursorPos((x,y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def look_at_image():
	screen = grab_screen(region=(0,0,1920,1080))
	crop_img = screen[320:820, 150:810]
	plt.imshow(crop_img)
	plt.show()


def run_while():
	while keyboard.is_pressed('q') == False:

		last = time.time()
		screen = grab_screen(region=(0,0,1920,1080))
		crop_img = screen[320:820, 150:810]
		
		
		threshold_slow(crop_img)

		#print('Loop took:', time.time()-last, 'seconds')



if __name__ == '__main__':
	#look_at_image()

	run_while()
