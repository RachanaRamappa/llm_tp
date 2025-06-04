; In initial state, (at ball1 room3)  and (at-robby robot1 room3). Both gripper of robot1 is free.
(pick robot1 ball1 room3 lgripper1) ; pick ball1 with free gripper of robot1.
(move robot1 room3 room1) ; move robot1 to room1, where ball1 should be placed.
(drop robot1 ball1 room1 lgripper1) ; drop ball1 at room1, with the gripper holding the ball.
