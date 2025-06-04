; In initial state, (at ball3 room3), and (at-robby robot1 room1) (at-robby robot2 room2) (at-robby robot3 room2) (at-robby robot4 room1), which means there is no robot at room3.
(move robot4 room1 room3) ; move a robot which has a free gripper (in this case, robot4) to room3. Now (at-robby robot4 room3).
(pick robot4 ball3 room3 lgripper4) ; Since (at-robby robot4 room3), pick ball3 with free gripper of robot4 at room3. (it's room3 not room1, because robot4 moved to room3 in last action.)
(move robot4 room3 room4) ; move robot4 to room4, where ball3 should be placed.
(drop robot4 ball3 room4 lgripper4) ; drop ball3 at room4, with the gripper holding the ball.
