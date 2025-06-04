
    (define (problem prob-1)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 b5 b6 b7 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (clear b1)
(clear b3)
(clear b5)
(clear b6)
(clear b7)
(clear-table t2)
(holding b4)
(on b1 b2)
(on-table b2 t1)
(on-table b3 t6)
(on-table b5 t4)
(on-table b6 t5)
(on-table b7 t3)
        )      
        (:goal (and (on-table b5 t2)))
        
    )
    