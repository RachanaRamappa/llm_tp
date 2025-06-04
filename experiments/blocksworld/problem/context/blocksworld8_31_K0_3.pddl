
    (define (problem prob-3)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 b5 b6 b7 b8 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (arm-empty )
(clear b1)
(clear b3)
(clear b6)
(clear b8)
(clear-table t4)
(clear-table t6)
(on b1 b2)
(on b3 b4)
(on b4 b5)
(on b8 b7)
(on-table b2 t2)
(on-table b5 t1)
(on-table b6 t3)
(on-table b7 t5)
        )      
        (:goal (and (on b6 b8)))
        
    )
    