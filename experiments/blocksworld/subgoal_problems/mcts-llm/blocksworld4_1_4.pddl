
    (define (problem prob-4)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (arm-empty )
(clear b1)
(clear b2)
(clear b4)
(clear-table t1)
(clear-table t2)
(clear-table t5)
(on b4 b3)
(on-table b1 t4)
(on-table b2 t6)
(on-table b3 t3)
        )      
        (:goal (and (on b2 b1)))
        
    )
    