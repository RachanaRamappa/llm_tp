
(define (problem BW-rand-9)
  (:domain blocksworld)
  (:objects
    b1 b2 b3 b4 b5 b6 b7 b8 - block
    t1 t2 t3 t4 t5 t6 - table
  )
  (:init
    (arm-empty)
    ; Initial state specification for t1, t2, t3
    (on b1 b2)
    (on-table b2 t1)
    (on b3 b4)
    (on b4 b5)
    (on-table b5 t2)
    (on b6 b7)
    (on b7 b8)
    (on-table b8 t3)
    (clear b1)
    (clear b3)
    (clear b6)
    (clear-table t4)
    (clear-table t5)
    (clear-table t6)
  )
  (:goal
    (and
    ; first subgoal : change the order of blocks on t3
      (on-table b8 t3)
      (on b7 b8)
      (on b6 b7)
      ;second subgoal : change the order of blocks on t2
      (on-table b5 t2)
      (on b3 b5)
      (on b4 b3)
      ; third subgoal : change the order of blocks on t1
      (on-table b1 t1)
      (on b2 b1)
    )
  )
)
