
    (define (problem prob-11)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (arm-empty )
(clear b1)
(clear b3)
(clear b4)
(clear b9)
(clear-table t1)
(clear-table t4)
(on b1 b2)
(on b4 b5)
(on b5 b6)
(on b8 b7)
(on b9 b8)
(on-table b2 t5)
(on-table b3 t6)
(on-table b6 t3)
(on-table b7 t2)
        )      
        (:goal (and (on b3 b1)))
        
    )
    