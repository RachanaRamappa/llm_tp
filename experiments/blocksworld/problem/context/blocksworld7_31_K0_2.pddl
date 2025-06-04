
    (define (problem prob-2)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 b5 b6 b7 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (arm-empty )
(clear b1)
(clear b3)
(clear b5)
(clear b6)
(clear b7)
(clear-table t6)
(on b1 b2)
(on b3 b4)
(on-table b2 t3)
(on-table b4 t5)
(on-table b5 t1)
(on-table b6 t4)
(on-table b7 t2)
        )      
        (:goal (and (on b5 b7)))
        
    )
    