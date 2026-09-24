
    (define (problem prob-8)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 b5 b6 b7 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (arm-empty )
(clear b1)
(clear b2)
(clear b4)
(clear b6)
(clear-table t3)
(clear-table t6)
(on b4 b3)
(on b5 b7)
(on b6 b5)
(on-table b1 t1)
(on-table b2 t4)
(on-table b3 t5)
(on-table b7 t2)
        )      
        (:goal (and (on-table b2 t3)))
        
    )
    