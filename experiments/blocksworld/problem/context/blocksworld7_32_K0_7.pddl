
    (define (problem prob-7)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 b5 b6 b7 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (arm-empty )
(clear b1)
(clear b2)
(clear b3)
(clear b7)
(clear-table t3)
(clear-table t6)
(on b3 b4)
(on b6 b5)
(on b7 b6)
(on-table b1 t4)
(on-table b2 t5)
(on-table b4 t1)
(on-table b5 t2)
        )      
        (:goal (and (clear b1)(clear b2)(clear-table t4)))
        
    )
    