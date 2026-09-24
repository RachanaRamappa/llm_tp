; first subgoal (on b6 b7) (on b7 b8) (on-table b8 t3) is already achieved in initial state.
(unstack b3 b4) ; Second subgoal: (on b4 b3) (on b3 b5) (on-table b5 t2): first, unstack top block and put down on t4
(putdown b3 t4)
(unstack b4 b5) ; unstack middle block and put down on t5
(putdown b4 t5)
(pickup b5 t2)  ; pick up bottom block and put down on t6
(putdown b5 t6)
(pickup b5 t6) ; to achieve (on-table b5 t2)
(putdown b5 t2)
(pickup b3 t4)  ; to achieve (on b3 b5)
(stack b3 b5)
(pickup b4 t5) ; to achieve  (on b4 b3)
(stack b4 b3)
(unstack b1 b2) ; Third Subgoal: (on b2 b1) (on-table b1 t1) : first, unstack top block and put down on t4
(putdown b1 t4)
(pickup b2 t1) ; pick up bottom block and put down on t5
(putdown b2 t5)
(pickup b1 t4) ; to achieve (on-table b1 t1)
(putdown b1 t1)
(pickup b2 t5) ; to achieve (on b2 b1)
(stack b2 b1)
; cost = 20 (unit cost)