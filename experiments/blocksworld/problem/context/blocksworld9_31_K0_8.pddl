
    (define (problem prob-8)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (arm-empty )
(clear b1)
(clear b4)
(clear b9)
(clear-table t1)
(clear-table t4)
(clear-table t6)
(on b1 b2)
(on b2 b3)
(on b4 b5)
(on b5 b6)
(on b8 b7)
(on b9 b8)
(on-table b3 t5)
(on-table b6 t3)
(on-table b7 t2)
        )      
        (:goal (and (clear b1)(clear b2)(clear b3)(clear-table t5)))
        
    )
    