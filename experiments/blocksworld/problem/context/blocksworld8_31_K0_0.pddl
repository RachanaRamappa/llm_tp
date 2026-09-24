
    (define (problem prob-0)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 b5 b6 b7 b8 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (arm-empty)
    (on b1 b2)
    (on-table b2 t2)

    (on b3 b4)
    (on b4 b5)
    (on-table b5 t1)

    (on b6 b7)
    (on b7 b8)
    (on-table b8 t5)

    (clear b1)
    (clear b3)
    (clear b6)
    (clear-table t6)
    (clear-table t4)
    (clear-table t3)
        )      
        (:goal (and (clear b6)(clear b7)(clear b8)(clear-table t5)))
        
    )
    