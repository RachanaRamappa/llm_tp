
(define (problem prob)
  (:domain blocksworld)
  (:objects
    b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block
    t1 t2 t3 t4 t5 t6 - table
  )
  (:init
    (arm-empty)
    (on b1 b2)
    (on b2 b3)
    (on-table b3 t5)

    (on b4 b5)
    (on b5 b6)
    (on-table b6 t4)

    (on b7 b8)
    (on b8 b9)
    (on b9 b10)
    (on-table b10 t3)

    (clear b1)
    (clear b4)
    (clear b7)
    (clear-table t1)
    (clear-table t2)
    (clear-table t6)
  )
  (:goal
    (and
      (on-table b7 t3)
      (on b9 b7)
      (on b10 b9)
      (on b8 b10)
      (on-table b6 t4)
      (on b5 b6)
      (on b4 b5)
      (on-table b2 t5)
      (on b3 b2)
      (on b1 b3))))
