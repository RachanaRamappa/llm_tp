
    (define (problem prob-0)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 b5 b6 b7 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (arm-empty)
    (on b1 b2)
    (on-table b2 t1)
    (on b3 b4)
    (on-table b4 t2)
    (on b5 b6)
    (on b6 b7)
    (on-table b7 t3)
    (clear b1)
    (clear b3)
    (clear b5)
    (clear-table t4)
    (clear-table t5)
    (clear-table t6)
        )      
        (:goal (and (clear b5)(clear b6)(clear b7)(clear-table t2)))
        
    )
    