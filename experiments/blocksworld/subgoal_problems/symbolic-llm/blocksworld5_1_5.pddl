
    (define (problem prob-5)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 b5 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (arm-empty )
(clear b2)
(clear b3)
(clear b4)
(clear b5)
(clear-table t1)
(clear-table t4)
(on b2 b1)
(on-table b1 t5)
(on-table b3 t6)
(on-table b4 t2)
(on-table b5 t3)
        )      
        (:goal (and (on b5 b3)))
        
    )
    