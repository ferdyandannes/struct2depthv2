import cv2
import numpy as np
import os
import glob

f = open("Motion/totalmotion1.txt", "r")

i = 0
testsite_array = []
object_motion = []
scaling = 4

ego_prev_rotate1 = 0
ego_prev_rotate2 = 0
ego_prev_rotate3 = 0

ego_next_rotate1 = 0
ego_next_rotate2 = 0
ego_next_rotate3 = 0

obj_prev_rotate1 = 0
obj_prev_rotate2 = 0
obj_prev_rotate3 = 0

obj_next_rotate1 = 0
obj_next_rotate2 = 0
obj_next_rotate3 = 0

obj_prev_x_past = 320
obj_prev_y_past = 250

size = 1000, 1000, 3
blank_image = np.zeros(size, dtype=np.uint8)
scale = 10

traj = np.zeros((500,640,3), dtype=np.uint8)
traj2 = np.zeros((500,640,3), dtype=np.uint8)
traj_comb = np.zeros((500,640,3), dtype=np.uint8)
traj_comb_new = np.zeros((500,640,3), dtype=np.uint8)

traj_new = np.zeros((1000,1280,3), dtype=np.uint8)
traj_viz = np.zeros((1000,1280,3), dtype=np.uint8)

traj_newz = np.zeros((1000,1280,3), dtype=np.uint8)

ego_baru_x = 0
ego_baru_y = 0
obj_baru_x = 0
obj_baru_y = 0

ego_baru_x2 = 0
ego_baru_y2 = 0

write_x_ego = 0
write_y_ego = 0


# Guide to the txt files
# ego
# testsite_array[i][0][1] = translation X
# testsite_array[i][1] = translation Y
# testsite_array[i][2] = translation Z
# testsite_array[i][3] = rotation X
# testsite_array[i][4] = rotation Y
# testsite_array[i][5][0] = rotation Z
# testsite_array[i][5][1] = translation X
# testsite_array[i][6] = translation Y
# testsite_array[i][7] = translation Z
# testsite_array[i][8] = rotation X
# testsite_array[i][9] = rotation Y
# testsite_array[i][10] = rotation Z
# object
# testsite_array[i][11] = translation X
# testsite_array[i][12] = translation Y
# testsite_array[i][13] = translation Z
# testsite_array[i][14] = rotation X
# testsite_array[i][15] = rotation Y
# testsite_array[i][16][0] = rotation Z
# testsite_array[i][16][1] = translation X
# testsite_array[i][17] = translation Y
# testsite_array[i][18] =  translation Z
# testsite_array[i][19] = rotation X
# testsite_array[i][20] = rotation Y
# testsite_array[i][21] = rotation Z

for row in f:
    testsite_array.append(row)

for i in range(len(testsite_array)):
    #print('')
    print('Frame ', i)
    # Separate the data ego-motion
    testsite_array[i] = testsite_array[i].strip().split(",")
    testsite_array[i][0] = testsite_array[i][0].split()
    testsite_array[i][5] = testsite_array[i][5].split()
    testsite_array[i][16] = testsite_array[i][16].split()

    # print(testsite_array[i][0][1], ' ', testsite_array[i][1], ' ', testsite_array[i][2], ' ', testsite_array[i][3], ' '
    #     , testsite_array[i][4], ' ', testsite_array[i][5][0], ' ', testsite_array[i][5][1], ' ', testsite_array[i][6]
    #     , ' ', testsite_array[i][7], ' ', testsite_array[i][8], ' ', testsite_array[i][9], ' ', testsite_array[i][10]
    #     , ' ', testsite_array[i][11], ' ', testsite_array[i][12], ' ', testsite_array[i][13], ' ', testsite_array[i][14]
    #     , ' ', testsite_array[i][15], ' ', testsite_array[i][16][0], ' ', testsite_array[i][16][1], ' ', testsite_array[i][17]
    #     , ' ', testsite_array[i][18], ' ', testsite_array[i][19], ' ', testsite_array[i][20], ' ', testsite_array[i][21])

    # EGO PREVIOUS FRAME
    ego_x_prev = float(testsite_array[i][0][1])*scaling
    ego_y_prev = float(testsite_array[i][1])*scaling
    ego_z_prev = float(testsite_array[i][2])*scaling

    ego_rot1_prev = float(testsite_array[i][3])
    ego_rot2_prev = float(testsite_array[i][4])
    ego_rot3_prev = float(testsite_array[i][5][0])

    ego_prev_rotate1 = ego_prev_rotate1 + ego_rot1_prev
    ego_prev_rotate2 = ego_prev_rotate2 + ego_rot2_prev
    ego_prev_rotate3 = ego_prev_rotate3 + ego_rot3_prev

    ego_coorY_prev = (((np.cos(ego_prev_rotate2)*np.cos(ego_prev_rotate3)) - (np.sin(ego_prev_rotate1)*np.sin(ego_prev_rotate2)*np.sin(ego_prev_rotate3)))*ego_x_prev) - (np.cos(ego_prev_rotate1)*np.sin(ego_prev_rotate3)*ego_y_prev)+ (((np.sin(ego_prev_rotate2)*np.cos(ego_prev_rotate3))+(np.sin(ego_prev_rotate1)*np.cos(ego_prev_rotate2)*np.sin(ego_prev_rotate3)))*ego_z_prev)
    ego_coorX_prev = ((np.cos(ego_prev_rotate1)*np.sin(ego_prev_rotate2))*ego_x_prev) + (np.sin(ego_prev_rotate1)*ego_y_prev) + ((np.cos(ego_prev_rotate1)*np.cos(ego_prev_rotate2))*ego_z_prev)

    ego_prev_x, ego_prev_y = ego_coorY_prev*scale, -ego_coorX_prev*scale

    # EGO NEXT FRAMES
    ego_x_next = float(testsite_array[i][5][1])*scaling
    ego_y_next = float(testsite_array[i][6])*scaling
    ego_z_next = float(testsite_array[i][7])*scaling

    ego_rot1_next = float(testsite_array[i][8])
    ego_rot2_next = float(testsite_array[i][9])
    ego_rot3_next = float(testsite_array[i][10])

    ego_next_rotate1 = ego_next_rotate1 + ego_rot1_next
    ego_next_rotate2 = ego_next_rotate2 + ego_rot2_next
    ego_next_rotate3 = ego_next_rotate3 + ego_rot3_next

    ego_coorY_next = (((np.cos(ego_next_rotate2)*np.cos(ego_next_rotate3)) - (np.sin(ego_next_rotate1)*np.sin(ego_next_rotate2)*np.sin(ego_next_rotate3)))*ego_x_next) - (np.cos(ego_next_rotate1)*np.sin(ego_next_rotate3)*ego_y_next) + (((np.sin(ego_next_rotate2)*np.cos(ego_next_rotate3))+(np.sin(ego_next_rotate1)*np.cos(ego_next_rotate2)*np.sin(ego_next_rotate3)))*ego_z_next)
    ego_coorX_next = ((np.cos(ego_next_rotate1)*np.sin(ego_next_rotate2))*ego_x_next) + (np.sin(ego_next_rotate1)*ego_y_next) + ((np.cos(ego_next_rotate1)*np.cos(ego_next_rotate2))*ego_z_next)

    ego_next_x, ego_next_y = ego_coorY_next*scale, -ego_coorX_next*scale

    # OBJ PREVIOUS FRAMES
    obj_x_prev = float(testsite_array[i][11])*scaling
    obj_y_prev = float(testsite_array[i][12])*scaling
    obj_z_prev = float(testsite_array[i][13])*scaling

    obj_rot1_prev = float(testsite_array[i][14])
    obj_rot2_prev = float(testsite_array[i][15])
    obj_rot3_prev = float(testsite_array[i][16][0])

    obj_prev_rotate1 = obj_prev_rotate1 + obj_rot1_prev
    obj_prev_rotate2 = obj_prev_rotate2 + obj_rot2_prev
    obj_prev_rotate3 = obj_prev_rotate3 + obj_rot3_prev

    obj_coorY_prev = (((np.cos(obj_prev_rotate2)*np.cos(obj_prev_rotate3)) - (np.sin(obj_prev_rotate1)*np.sin(obj_prev_rotate2)*np.sin(obj_prev_rotate3)))*obj_x_prev) - (np.cos(obj_prev_rotate1)*np.sin(obj_prev_rotate3)*obj_y_prev) + (((np.sin(obj_prev_rotate2)*np.cos(obj_prev_rotate3))+(np.sin(obj_prev_rotate1)*np.cos(obj_prev_rotate2)*np.sin(obj_prev_rotate3)))*obj_z_prev)
    obj_coorX_prev = ((np.cos(obj_prev_rotate1)*np.sin(obj_prev_rotate2))*obj_x_prev) + (np.sin(obj_prev_rotate1)*obj_y_prev) +((np.cos(obj_prev_rotate1)*np.cos(obj_prev_rotate2))*obj_z_prev)

    obj_prev_x, obj_prev_y = obj_coorY_prev*scale, -obj_coorX_prev*scale

    # OBJ NEXT FRAMES
    obj_x_next = float(testsite_array[i][16][1])*scaling
    obj_y_next = float(testsite_array[i][17])*scaling
    obj_z_next = float(testsite_array[i][18])*scaling

    obj_rot1_next = float(testsite_array[i][19])
    obj_rot2_next = float(testsite_array[i][20])
    obj_rot3_next = float(testsite_array[i][21])

    obj_next_rotate1 = obj_next_rotate1 + obj_rot1_next
    obj_next_rotate2 = obj_next_rotate2 + obj_rot2_next
    obj_next_rotate3 = obj_next_rotate3 + obj_rot3_next

    obj_coorY_next = (((np.cos(obj_next_rotate2)*np.cos(obj_next_rotate3)) - (np.sin(obj_next_rotate1)*np.sin(obj_next_rotate2)*np.sin(obj_next_rotate3)))*obj_x_next) - (np.cos(obj_next_rotate1)*np.sin(obj_next_rotate3)*obj_y_next) + (((np.sin(ego_next_rotate2)*np.cos(obj_next_rotate3))+(np.sin(obj_next_rotate1)*np.cos(obj_next_rotate2)*np.sin(obj_next_rotate3)))*obj_z_next)
    obj_coorX_next = ((np.cos(obj_next_rotate1)*np.sin(obj_next_rotate2))*obj_x_next) + (np.sin(obj_next_rotate1)*obj_y_next) + ((np.cos(obj_next_rotate1)*np.cos(obj_next_rotate2))*obj_z_next)

    obj_next_x, obj_next_y = obj_coorY_next*scale, -obj_coorX_next*scale


    ############## VISUALIZATION PART ###############
    H = np.float32([[1,0,ego_baru_x],[0,1,ego_baru_y]])
    asddsa = cv2.warpAffine(traj_viz, H,(1280,1000),flags=cv2.INTER_LANCZOS4)



    if i % 2 == 0 :
        ego_baru_x = ego_baru_x2
        ego_baru_y = ego_baru_y2
    else :
        ego_baru_x = ego_baru_x + (-ego_prev_x*1.5)
        ego_baru_y = ego_baru_y + (-ego_prev_y*1.5)

        ego_baru_x2 = ego_baru_x2 + (-ego_next_x*1.5)
        ego_baru_y2 = ego_baru_y2 + (-ego_next_y*1.5)

    write_x_ego = 640 - ego_baru_x
    write_y_ego = 500 - ego_baru_y

    cv2.circle(traj_new, (int(write_x_ego), int(write_y_ego)) ,1, (0,255,0), 2)

    traj_viz = traj_new.copy()

    cv2.rectangle(traj_viz, (int(write_x_ego)-7,int(write_y_ego)-14), (int(write_x_ego)+7,int(write_y_ego)+14), (0,255,0), 2)

    cv2.imshow("wenakno", traj_viz)
    #cv2.imshow("obj", traj_new2)
    cv2.waitKey(1)
    #traj_comb = traj_ego
    #cv2.imshow("traj_comb 2", traj_comb)

#cv2.imwrite("7.jpg", asddsa)
cv2.waitKey(0)