
(define (problem prob)
  (:domain blocksworld)
  (:objects
    b1 b2 b3 b4 b5 b6 b7 b8 - block
    t1 t2 t3 t4 t5 t6 - table
  )
  (:init
    (arm-empty)
    (on b1 b2)
    (on-table b2 t6)

    (on b3 b4)
    (on b4 b5)
    (on-table b5 t1)

    (on b6 b7)
    (on b7 b8)
    (on-table b8 t4)

    (clear b1)
    (clear b3)
    (clear b6)
    (clear-table t2)
    (clear-table t5)
    (clear-table t3)
  )
  (:goal
    (and
      (on-table b7 t4)
      (on b6 b7)
      (on b8 b6)
      (on-table b4 t1)
      (on b5 b4)
      (on b3 b5)
      (on-table b2 t6)
      (on b1 b2))))
