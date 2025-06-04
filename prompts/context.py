rw.move_to_init_pose()

t1 = [-0.40, -0.30, 0.79, 0.5, -0.5, -0.5, -0.5]
t2 = [-0.40, -0.525, 0.79, 0.5, -0.5, -0.5, -0.5]
t3 = [-0.40, -0.75, 0.79, 0.5, -0.5, -0.5, -0.5]
t4 = [-0.65, -0.30, 0.79, 0.5, -0.5, -0.5, -0.5]
t5 = [-0.65, -0.525, 0.79, 0.5, -0.5, -0.5, -0.5]
t6 = [-0.65, -0.75, 0.79, 0.5, -0.5, -0.5, -0.5]
approach = [0, 0, -1]

# (unstack b6 b7)
bbox = rw.detect_object('block 6')
grasp_pose, approach_vector = rw.get_grasp_pose('block 6', bbox)
rw.pick_up_object(grasp_pose, approach_vector)

# (putdown b6 t2)
rw.place_object(t2, False)

# (unstack b7 b8)
bbox = rw.detect_object('block 7')
grasp_pose, approach_vector = rw.get_grasp_pose('block 7', bbox)
rw.pick_up_object(grasp_pose, approach_vector)

# (putdown b7 t3)
rw.place_object(t3, False)

# (pickup b8 t5)
bbox = rw.detect_object('block 8')
grasp_pose, approach_vector = rw.get_grasp_pose('block 8', bbox)
rw.pick_up_object(grasp_pose, approach_vector)

# (putdown b8 t4)
rw.place_object(t4, False)

# (pickup b8 t4)
bbox = rw.detect_object('block 8')
grasp_pose, approach_vector = rw.get_grasp_pose('block 8', bbox)
rw.pick_up_object(grasp_pose, approach_vector)

# (putdown b8 t5)
rw.place_object(t5, False)

# (pickup b6 t2)
bbox = rw.detect_object('block 6')
grasp_pose, approach_vector = rw.get_grasp_pose('block 6', bbox)
rw.pick_up_object(grasp_pose, approach_vector)

# (stack b6 b8)
pose_b8 = t5
pose_b6 = pose_b8.copy()
pose_b6[2] += 0.08
rw.place_object(pose_b6, False)

# (pickup b7 t3)
bbox = rw.detect_object('block 7')
grasp_pose, approach_vector = rw.get_grasp_pose('block 7', bbox)
rw.pick_up_object(grasp_pose, approach_vector)

# (stack b7 b6)
pose_b6 = pose_b6.copy()
pose_b7 = pose_b6.copy()
pose_b7[2] += 0.08
rw.place_object(pose_b7, False)

# (unstack b3 b4)
bbox = rw.detect_object('block 3')
grasp_pose, approach_vector = rw.get_grasp_pose('block 3', bbox)
rw.pick_up_object(grasp_pose, approach_vector)

# (putdown b3 t2)
rw.place_object(t2, False)

# (unstack b4 b5)
bbox = rw.detect_object('block 4')
grasp_pose, approach_vector = rw.get_grasp_pose('block 4', bbox)
rw.pick_up_object(grasp_pose, approach_vector)

# (putdown b4 t3)
rw.place_object(t3, False)

# (pickup b5 t1)
bbox = rw.detect_object('block 5')
grasp_pose, approach_vector = rw.get_grasp_pose('block 5', bbox)
rw.pick_up_object(grasp_pose, approach_vector)

# (putdown b5 t4)
rw.place_object(t4, False)

# (pickup b4 t3)
bbox = rw.detect_object('block 4')
grasp_pose, approach_vector = rw.get_grasp_pose('block 4', bbox)
rw.pick_up_object(grasp_pose, approach_vector)

# (putdown b4 t1)
rw.place_object(t1, False)

# (pickup b3 t2)
bbox = rw.detect_object('block 3')
grasp_pose, approach_vector = rw.get_grasp_pose('block 3', bbox)
rw.pick_up_object(grasp_pose, approach_vector)

# (stack b3 b4)
pose_b4 = t1
pose_b3 = pose_b4.copy()
pose_b3[2] += 0.08
rw.place_object(pose_b3, False)

# (pickup b5 t4)
bbox = rw.detect_object('block 5')
grasp_pose, approach_vector = rw.get_grasp_pose('block 5', bbox)
rw.pick_up_object(grasp_pose, approach_vector)

# (stack b5 b3)
pose_b3 = pose_b3.copy()
pose_b5 = pose_b3.copy()
pose_b5[2] += 0.08
rw.place_object(pose_b5, False)

# (unstack b1 b2)
bbox = rw.detect_object('block 1')
grasp_pose, approach_vector = rw.get_grasp_pose('block 1', bbox)
rw.pick_up_object(grasp_pose, approach_vector)

# (putdown b1 t2)
rw.place_object(t2, False)

# (pickup b2 t6)
bbox = rw.detect_object('block 2')
grasp_pose, approach_vector = rw.get_grasp_pose('block 2', bbox)
rw.pick_up_object(grasp_pose, approach_vector)

# (putdown b2 t3)
rw.place_object(t3, False)

# (pickup b1 t2)
bbox = rw.detect_object('block 1')
grasp_pose, approach_vector = rw.get_grasp_pose('block 1', bbox)
rw.pick_up_object(grasp_pose, approach_vector)

# (putdown b1 t6)
rw.place_object(t6, False)

# (pickup b2 t3)
bbox = rw.detect_object('block 2')
grasp_pose, approach_vector = rw.get_grasp_pose('block 2', bbox)
rw.pick_up_object(grasp_pose, approach_vector)

# (stack b2 b1)
pose_b1 = t6
pose_b2 = pose_b1.copy()
pose_b2[2] += 0.08
rw.place_object(pose_b2, False)