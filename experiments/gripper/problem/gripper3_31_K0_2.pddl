
    (define (problem prob-2)
        (:domain gripper)
        (:objects robot1 robot2 robot3 robot4 - robot
    rgripper1 lgripper1 rgripper2 lgripper2 rgripper3 lgripper3 rgripper4 lgripper4 - gripper
    room1 room2 room3 room4 - room
    ball1 ball2 ball3 - object)
        (:init 
            (at ball1 room1)
(at ball2 room2)
(at ball3 room3) ; ball3 is at room3.
(at-robby robot1 room1) ; robot1 is at room1.
(at-robby robot2 room2) ; robot2 is at room2.
(at-robby robot3 room2) ; robot3 is at room2.
(at-robby robot4 room1) ; robot4 is at room1.
(free robot1 lgripper1)
(free robot1 rgripper1)
(free robot2 lgripper2)
(free robot2 rgripper2)
(free robot3 lgripper3)
(free robot3 rgripper3)
(free robot4 lgripper4)
(free robot4 rgripper4)
        )      
        (:goal (and (at ball3 room4)))
        
    )
    