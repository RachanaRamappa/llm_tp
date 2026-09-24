
    (define (problem prob-0)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 b5 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (arm-empty)
    (on b1 b2)
    (on-table b2 t5)

    (on b3 b4)
    (on b4 b5)
    (on-table b5 t6)

    (clear b1)
    (clear b3)
    (clear-table t3)

    (clear-table t4)
    (clear-table t1)
    (clear-table t2)
        )      
        (:goal (and (clear b1) (clear b2) (clear-table t5)))
        
    )
    