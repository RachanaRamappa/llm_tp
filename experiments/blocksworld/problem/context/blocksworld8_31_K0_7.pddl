
    (define (problem prob-7)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 b5 b6 b7 b8 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (arm-empty )
(clear b1)
(clear b4)
(clear b5)
(clear b6)
(clear-table t3)
(clear-table t6)
(on b1 b2)
(on b5 b3)
(on b6 b8)
(on b8 b7)
(on-table b2 t2)
(on-table b3 t1)
(on-table b4 t4)
(on-table b7 t5)
        )      
        (:goal (and (on b4 b5)))
        
    )
    