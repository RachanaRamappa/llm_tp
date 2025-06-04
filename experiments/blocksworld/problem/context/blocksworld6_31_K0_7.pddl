
    (define (problem prob-7)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 b5 b6 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (arm-empty )
(clear b1)
(clear b2)
(clear b3)
(clear b6)
(clear-table t4)
(clear-table t5)
(on b3 b4)
(on b6 b5)
(on-table b1 t1)
(on-table b2 t2)
(on-table b4 t6)
(on-table b5 t3)
        )      
        (:goal (and (on-table b1 t5)))
        
    )
    