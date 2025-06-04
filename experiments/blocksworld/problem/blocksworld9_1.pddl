
(define (problem prob)
  (:domain blocksworld)
  (:objects
    b1 b2 b3 b4 b5 b6 b7 b8 b9 - block
    t1 t2 t3 t4 t5 t6 - table
  )
  (:init
    (arm-empty)
    (on b1 b2)
    (on b2 b3)
    (on-table b3 t3)

    (on b4 b5)
    (on b5 b6)
    (on-table b6 t5)

    (on b7 b8)
    (on b8 b9)
    (on-table b9 t2)

    (clear b1)
    (clear b4)
    (clear b7)
    (clear-table t1)
    (clear-table t6)
    (clear-table t4)
  )
  (:goal
    (and
      (on-table b9 t2)
      (on b8 b9)
      (on b7 b8)
      (on-table b5 t5)
      (on b4 b5)
      (on b6 b4)
      (on-table b1 t3)
      (on b3 b1)
      (on b2 b3))))
