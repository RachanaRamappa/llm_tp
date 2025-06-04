
    (define (problem prob-12)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (arm-empty )
(clear b1)
(clear b3)
(clear b6)
(clear b9)
(clear-table t5)
(clear-table t6)
(on b3 b2)
(on b5 b4)
(on b6 b5)
(on b7 b10)
(on b8 b7)
(on b9 b8)
(on-table b1 t1)
(on-table b10 t3)
(on-table b2 t4)
(on-table b4 t2)
        )      
        (:goal (and (on b1 b3)))
        
    )
    