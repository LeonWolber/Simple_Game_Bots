from utils import grab_screen
import time
import cv2
import matplotlib.pyplot as plt
import win32gui, win32ui, win32con, win32api
import numpy as np
import math

START_RADIUS = 34 # default size of player starting off the game


# for now hard coded
LEFT = np.array([290, 450+85])
RIGHT = np.array([650, 450+85])
UP = np.array([470, 260+85])
DOWN = np.array([475, 620+85])



def blur(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    return blur

def circles(img):
    coords = []
    
    rows=img.shape[0]
    # Find circles
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, rows/16,
                               param1=70, param2=50,
                               minRadius=1, maxRadius=100)
    # If some circle is found
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        # loop over the circles
        for (x, y, r) in circles:


            coords.append(np.array([x,y,r]))

            cv2.circle(img, (x, y), r, (0, 255, 0), 2)

    return coords, img

def calc_difference(lst, center):
	# calculate the difference in x,y coords from center(player position)
    x_diff = round(math.sqrt((center[0] - lst[0])**2))
    y_diff = round(math.sqrt((center[1] - lst[1])**2))
    # extract radius
    r = lst[2]
    
    return [x_diff, y_diff, r]


def find_smallest_r(lst, center):

    # calculate differences of coordinates
    my_list = [calc_difference(i, center) for i in lst]
    
    # sort to find closest x,y neighbours
    sorted_list = sorted(my_list , key=lambda k: [k[0], k[1]])
    if len(sorted_list) != 0:
	    closest_smaller_than_me_temp = [i for i in sorted_list if i[2] < 34][0]
	    closest_smaller_than_me = np.array(closest_smaller_than_me_temp[:2]) + center[:2]

	    
	    return closest_smaller_than_me, lst


def move(x,y):
	# move mouse
    win32api.SetCursorPos((x,y))


# def show_plt():

#     screen = grab_screen(region=(0,0,1920,1080))
#     crop = screen[85:950, 0:970]
#     copy = crop.copy()
#     plt.imshow(crop)
#     plt.show()


# def find_blobs(image):
#     center_x = image.shape[0]
#     center_y = image.shape[1]
#     params = cv2.SimpleBlobDetector_Params()
#     params.filterByCircularity = True
#     params.minCircularity = 0
#     params.maxCircularity = 1
#     params.minDistBetweenBlobs = 5
#     params.filterByArea = True
#     params.minArea = 1
#     params.maxArea = 500000
#     params.filterByInertia = True
#     params.minInertiaRatio = 0
#     params.maxInertiaRatio = 1
#     params.filterByConvexity = True
#     params.minConvexity = 0
#     params.maxConvexity = 1
#     detector = cv2.SimpleBlobDetector_create(params)
#     found_blobs = detector.detect(image)
#     image = cv2.drawKeypoints(image, found_blobs, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
#     return image

# returns coordinates of detected blobs within image
	    # im = find_blobs(gray)







def run():
    while True:

	    screen = grab_screen(region=(0,0,1920,1080)) 
	    crop = screen[85:950, 0:970] # select region of interest
	    center = int(crop.shape[0]/2), int(crop.shape[1]/2) # x,y,r


	    copy = crop.copy()
	    gray = cv2.cvtColor(copy, cv2.COLOR_RGB2GRAY)

	 
	    # use HoughCircles to detect circles within image
	    circle_coords, img = circles(gray)

	    # calculate distance to smallest detected circles
	    closest_coord, all_circles = find_smallest_r(circle_coords, center)
	    print(f'Moving to -> {closest_coord}')

	    
	    # go to eat closest blob thats smaller than me
	    move(closest_coord[0],closest_coord[1])
	    # ToDo: implement functionality to go as long as own radius increases

	    # g = [i for i in all_circles if (i[0] > center[0]-5) & (qi[0] < center[0]+5) & (i[1] > center[1]-5) & (i[1] < center[1]+5)]
	    # if len(g) > 0:
	    # 	new_radius = g[0][2]
	    time.sleep(1)



	    # cv2.imshow('', img)
	    # if cv2.waitKey(25) & 0xFF == ord('q'):
	    #     cv2.destroyAllWindows()
	    #     cv2.waitKey(0)
	    #     break




if __name__ == '__main__':

    run()
    #show_plt()
