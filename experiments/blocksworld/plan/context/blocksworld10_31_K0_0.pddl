; From initial state, t1, t5, t9 is clear
(unstack b7 b8)
(putdown b7 t1) ; now (on-table b7 t1)
(unstack b8 b9)
(putdown b8 t5) ; now (on-table b8 t5)
(unstack b9 b10)
(putdown b9 t6) ; now (on-table b9 t6)
(pickup b10 t3) ; to achieve (clear-table t3), we should pick up b10
(stack b10 b4)  ; Now every table (t1, t2, ..., t6) are all not clear. So b10 should be stacked on another clear block. It's ALWAYS (stack b10 b4)
