
    (define (problem prob-0)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (arm-empty)
    (on b1 b2)
    (on b2 b3)
    (on-table b3 t4)

    (on b4 b5)
    (on b5 b6)
    (on-table b6 t2)

    (on b7 b8)
    (on b8 b9)
    (on b9 b10)
    (on-table b10 t3)

    (clear b1)
    (clear b4)
    (clear b7)
    (clear-table t1)
    (clear-table t5)
    (clear-table t6)
        )      
        (:goal (and (clear b7)(clear b8)(clear b9)(clear b10)(clear-table t3)))
        
    )
    