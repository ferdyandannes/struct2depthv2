import cv2
import numpy as np
import os
import glob

f = open("Motion/egomotion1_ori.txt", "r")
g = open("Motion/objmotion1_tra.txt", "r")
#print(f.read())

i = 0
testsite_array = []
object_motion = []
scaling = 4

rotate1 = 0
rotate2 = 0
rotate3 = 0
rotate1_obj = 0
rotate2_obj = 0
rotate3_obj = 0

size = 1000, 1000, 3
blank_image = np.zeros(size, dtype=np.uint8)
scale = 10

traj = np.zeros((1000,1280,3), dtype=np.uint8)
#traj.fill(255)
traj2 = np.zeros((1000,1280,3), dtype=np.uint8)
#traj2.fill(255)

for row in f:
	testsite_array.append(row)

for obj in g:
	object_motion.append(obj)

for i in range(len(testsite_array)):
	print('start')

	# Separate the data ego-motion
	testsite_array[i] = testsite_array[i].strip().split(",")
	testsite_array[i][0] = testsite_array[i][0].split()
	testsite_array[i][5] = testsite_array[i][5].split()

	# Separate the data object-motion
	object_motion[i] = object_motion[i].strip().split(",")
	object_motion[i][0] = object_motion[i][0].split()
	object_motion[i][5] = object_motion[i][5].split()

	# Ego-motion preprocessing
	x = float(testsite_array[i][0][1])*scaling
	y = float(testsite_array[i][1])*scaling
	z = float(testsite_array[i][2])*scaling
	prev_rot1 = float(testsite_array[i][3])
	prev_rot2 = float(testsite_array[i][4])
	prev_rot3 = float(testsite_array[i][5][0])

	# Print the scaling
	print('X = ', x, ' Y = ', y, ' Z = ', z)

	rotate1 = rotate1 + prev_rot1
	rotate2 = rotate2 + prev_rot2
	rotate3 = rotate3 + prev_rot3

	coorY = (((np.cos(rotate2)*np.cos(rotate3)) - (np.sin(rotate1)*np.sin(rotate2)*np.sin(rotate3)))*x) - (np.cos(rotate1)*np.sin(rotate3)*y) + (((np.sin(rotate2)*np.cos(rotate3))+(np.sin(rotate1)*np.cos(rotate2)*np.sin(rotate3)))*z)
	coorX = ((np.cos(rotate1)*np.sin(rotate2))*x) + (np.sin(rotate1)*y) + ((np.cos(rotate1)*np.cos(rotate2))*z)

	# Object-motion preprocessing
	x = float(object_motion[i][0][1])*scaling
	y = float(object_motion[i][1])*scaling
	z = float(object_motion[i][2])*scaling
	prev_rot1_obj = float(object_motion[i][3])
	prev_rot2_obj = float(object_motion[i][4])
	prev_rot3_obj = float(object_motion[i][5][0])

	rotate1_obj = rotate1_obj + prev_rot1_obj
	rotate2_obj = rotate2_obj + prev_rot2_obj
	rotate3_obj = rotate3_obj + prev_rot3_obj

	coorY_obj = (((np.cos(rotate2_obj)*np.cos(rotate3_obj)) - (np.sin(rotate1_obj)*np.sin(rotate2_obj)*np.sin(rotate3_obj)))*x) - (np.cos(rotate1_obj)*np.sin(rotate3_obj)*y) + (((np.sin(rotate2_obj)*np.cos(rotate3_obj))+(np.sin(rotate1_obj)*np.cos(rotate2_obj)*np.sin(rotate3_obj)))*z)
	coorX_obj = ((np.cos(rotate1_obj)*np.sin(rotate2_obj))*x) + (np.sin(rotate1_obj)*y) + ((np.cos(rotate1_obj)*np.cos(rotate2_obj))*z)

	# Show the total of trajectories	
	#cv2.circle(blank_image, (int(coorX_obj*500)+200, int(coorY_obj*250)+200) ,1, (0,255,0), 2)
	#cv2.imshow("object2", blank_image)

	# Loadable coordinate 
	# 1. coorY
	# 2. coorX

	# Ego-motion cordinates
	pre_x, pre_y = coorY*scale, -coorX*scale
	#print("X = ", pre_x , " Y = ", pre_y)
	#print('')

	H = np.float32([[1,0,-pre_x],[0,1,-pre_y]])
	rows,cols = traj.shape[:2]
	traj_new = cv2.warpAffine(traj,H,(1280, 1000),flags=cv2.INTER_LANCZOS4)

	# Warping 2D
	# Until this part, we can show the trajectories but without any warping, cv2.line give the trajectory
	traj = traj_new
	cv2.line(traj_new, (640, 500),(int(640-pre_x), int(500-pre_y)), (255,255,255), int(scale*0.3))
	#cv2.imshow("ego", traj_new)


	# Object-motion cordinates
	pre_x_obj, pre_y_obj = coorY_obj*scale, -coorX_obj*scale
	#print("X_obj = ", pre_x_obj , " Y_obj = ", pre_y_obj)
	print('')

	H2 = np.float32([[1,0,-pre_x_obj],[0,1,-pre_y_obj]])
	rows,cols = traj2.shape[:2]
	traj_new2 = cv2.warpAffine(traj2,H2,(1280, 1000),flags=cv2.INTER_LANCZOS4)

	# Different window
	traj2 = traj_new2
	cv2.line(traj_new2, (640, 500),(int(640-pre_x_obj), int(500-pre_y_obj)), (255,0,255), int(scale*0.3))
	#cv2.imshow("object", traj_new2)


	# Same windows
	#traj2 = traj_new
	#cv2.line(traj_new, (640, 500),(int(640-pre_x), int(500-pre_y)), (255,255,255), int(scale*0.3))
	#cv2.line(traj_new, (640, 500),(int(640-pre_x_obj), int(500-pre_y_obj)), (255,0,255), int(scale*0.3))
	#cv2.imshow("object", traj_new)

	traj_new = cv2.warpAffine(traj, H, (1280, 1000))
	M_2 = cv2.getRotationMatrix2D((640, 500), float(rotate2) * 180 / np.pi, 1)
	new_2 = cv2.warpAffine(traj_new, M_2, (1280, 1000))


	# Print the coordinates
	#print("X = ", pre_x , " Y = ", pre_y)
	#print('')
	#cv2.circle(trajectories, (int(640-pre_x), int(500-pre_y)) ,1, (0,255,0), 2)
	#cv2.imshow("lele", trajectories)

	
	# Show the total of trajectories
	#cv2.circle(trajectories, (pre_x, pre_y) ,1, (0,255,0), 2)

	cv2.imshow("eee", new_2)
	#cv2.imshow("dadadada", traj_new)
	cv2.waitKey(1)

	

#cv2.imshow("eee", blank_image)
cv2.imwrite("0005_ori_obj.jpg", traj_new)
cv2.imwrite("0005_tra_obj.jpg", traj_new2)
cv2.waitKey(0)