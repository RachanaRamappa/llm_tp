(unstack b5 b6) ; to achieve (clear b5): unstack b5 from b6 and put down on clear table
(putdown b5 t4)
(unstack b6 b7) ; to achieve (clear b6): unstack b6 from b7 and put down on clear table
(putdown b6 t5)
(unstack b3 b4) ; to achieve (clear-table t2): move b3, b4 which was stacked on on t2
(putdown b3 t6)
(pickup b4 t2)
; cost = 7 (unit cost)

; Planning time: 0.8271095752716064 seconds
; Planning time: 0.8271095752716064 seconds