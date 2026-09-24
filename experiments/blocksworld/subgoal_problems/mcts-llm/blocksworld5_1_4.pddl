
    (define (problem prob-4)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 b5 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (arm-empty )
(clear b2)
(clear b3)
(clear b4)
(clear b5)
(clear-table t2)
(clear-table t6)
(on b2 b1)
(on-table b1 t5)
(on-table b3 t3)
(on-table b4 t4)
(on-table b5 t1)
        )      
        (:goal (and (on-table b3 t6)))
        
    )
    