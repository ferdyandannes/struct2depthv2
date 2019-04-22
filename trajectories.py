import cv2
import numpy as np
import os
import glob

f = open("egomotion5.txt", "r")
#f = open("objmotion.txt", "r")
#print(f.read())

i = 0
testsite_array = []

rotate1 = 0
rotate2 = 0
rotate3 = 0

xbaru = 0
ybaru = 0
zbaru = 0

size = 1000, 1000, 3
blank_image = np.zeros(size, dtype=np.uint8)
scale = 10

traj = np.zeros((1000,1280,3), dtype=np.uint8)
trajectories = np.zeros((1000,1280,3), dtype=np.uint8)

for row in f:
	testsite_array.append(row)

for i in range(len(testsite_array)):
	print('start')
	testsite_array[i] = testsite_array[i].strip().split(",")
	
	testsite_array[i][0] = testsite_array[i][0].split()
	testsite_array[i][5] = testsite_array[i][5].split()

	# VERSION 1
	#x = (float(testsite_array[i][0][1])*1000*1000)/(36000*3)
	#y = (float(testsite_array[i][1])*1000*1000)/(36000*3)
	#z = (float(testsite_array[i][2])*1000*1000)/(36000*3)

	# VERSION 2
	x = float(testsite_array[i][0][1])*1000*1000/36000*3
	y = float(testsite_array[i][1])*1000*1000/36000*3
	z = float(testsite_array[i][2])*1000*1000/36000*3
	prev_rot1 = float(testsite_array[i][3])
	prev_rot2 = float(testsite_array[i][4])
	prev_rot3 = float(testsite_array[i][5][0])

	rotate1 = rotate1 + prev_rot1
	rotate2 = rotate2 + prev_rot2
	rotate3 = rotate3 + prev_rot3

	coorY = (((np.cos(rotate2)*np.cos(rotate3)) - (np.sin(rotate1)*np.sin(rotate2)*np.sin(rotate3)))*x) - (np.cos(rotate1)*np.sin(rotate3)*y) + (((np.sin(rotate2)*np.cos(rotate3))+(np.sin(rotate1)*np.cos(rotate2)*np.sin(rotate3)))*z)
	coorX = ((np.cos(rotate1)*np.sin(rotate2))*x) + (np.sin(rotate1)*y) + ((np.cos(rotate1)*np.cos(rotate2))*z)


	# Methods 1
	xbaru += float(testsite_array[i][0][1])
	ybaru += float(testsite_array[i][1])
	zbaru += float(testsite_array[i][2])
	#print("X = ", float(testsite_array[i][0][1]) , "    Y = ", float(testsite_array[i][1]), "   Z = ", float(testsite_array[i][2]))
	#print("X = ", xbaru*100 , " Y = ", ybaru*100, " Z = ", zbaru*100)
	#print("X = ", int(xbaru*500)+500 , "    Y = ", int(ybaru*500)+500, "    Z = ", int(zbaru*500)+500)
	#print('')


	# Show the total of trajectories
	cv2.circle(trajectories, (int(coorX*500)+200, int(coorY*250)+200) ,1, (0,255,0), 2)



	# Loadable coordinate 
	# 1. coorY
	# 2. coorX

	# Ego-motion cordinates
	pre_x, pre_y = coorY*scale, -coorX*scale

	H = np.float32([[1,0,-pre_x],[0,1,-pre_y]])
	rows,cols = traj.shape[:2]
	traj_new = cv2.warpAffine(traj,H,(1280, 1000),flags=cv2.INTER_LANCZOS4)

	# Warping 2D
	traj = traj_new
	cv2.line(traj_new, (640, 500),(int(640-pre_x), int(500-pre_y)), (255,255,255), int(scale*0.7))

	traj_new = cv2.warpAffine(traj, H, (1280, 1000))
	M_2 = cv2.getRotationMatrix2D((640, 500), float(rotate2) * 180 / np.pi, 1)
	new_2 = cv2.warpAffine(traj_new, M_2, (1280, 1000))


	# Print the coordinates
	print("X = ", pre_x , " Y = ", pre_y)
	print('')
	cv2.circle(trajectories, (int(640-pre_x), int(500-pre_y)) ,1, (0,255,0), 2)
	cv2.imshow("lele", trajectories)

	
	# Show the total of trajectories
	#cv2.circle(trajectories, (pre_x, pre_y) ,1, (0,255,0), 2)

	#cv2.imshow("eee", new_2)
	#cv2.imshow("dadadada", traj_new)
	cv2.waitKey(1)

	

#cv2.imshow("eee", blank_image)
#cv2.waitKey(0)