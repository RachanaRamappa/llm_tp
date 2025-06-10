
(define (problem prob)
  (:domain blocksworld)
  (:objects
    b1 b2 b3 b4 b5 b6 b7 - block
    t1 t2 t3 t4 t5 t6 - table
  )
  (:init
    (arm-empty)
    (on b1 b2)
    (on-table b2 t6)

    (on b3 b4)
    (on-table b4 t5)

    (on b5 b6)
    (on b6 b7)
    (on-table b7 t4)

    (clear b1)
    (clear b3)
    (clear b5)
    (clear-table t2)
    (clear-table t1)
    (clear-table t3)
  )
  (:goal
    (and
      (on-table b5 t4)
      (on b6 b5)
      (on b7 b6)
      (on-table b4 t5)
      (on b3 b4)
      (on-table b1 t6)
      (on b2 b1))))
