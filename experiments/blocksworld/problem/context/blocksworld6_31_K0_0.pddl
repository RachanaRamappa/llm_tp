
    (define (problem prob-0)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 b5 b6 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (arm-empty)
    (on b1 b2)
    (on-table b2 t5)

    (on b3 b4)
    (on-table b4 t6)
    (on b5 b6)
    (on-table b6 t3)
    (clear b1)
    (clear b3)
    (clear b5)
    (clear-table t2)
    (clear-table t4)
    (clear-table t1)
        )      
        (:goal (and (clear b5)(clear b6)(clear-table t3)))
        
    )
    