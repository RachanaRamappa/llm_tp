
(define (problem prob)
  (:domain blocksworld)
  (:objects
    b1 b2 b3 b4 b5 b6 - block
    t1 t2 t3 t4 t5 t6 - table
  )
  (:init
    (arm-empty)
    (on b1 b2)
    (on-table b2 t2)

    (on b3 b4)
    (on-table b4 t4)
    (on b5 b6)
    (on-table b6 t6)
    (clear b1)
    (clear b3)
    (clear b5)
    (clear-table t3)
    (clear-table t5)
    (clear-table t1)
  )
  (:goal
    (and
      (on-table b6 t6)
      (on b5 b6)
      (on-table b4 t4)
      (on b3 b4)
      (on-table b1 t2)
      (on b2 b1))))
