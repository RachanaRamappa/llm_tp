
    (define (problem prob-5)
        (:domain blocksworld)
        (:objects b1 b2 b3 b4 b5 b6 b7 - block
    t1 t2 t3 t4 t5 t6 - table)
        (:init 
            (clear b1)
(clear b3)
(clear b4)
(clear b7)
(clear-table t1)
(clear-table t5)
(holding b2)
(on b6 b5)
(on b7 b6)
(on-table b1 t4)
(on-table b3 t6)
(on-table b4 t3)
(on-table b5 t2)
        )      
        (:goal (and (on-table b4 t1)))
        
    )
    