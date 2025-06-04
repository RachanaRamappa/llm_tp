(empty-shaker right shaker1 cocktail2 l1 l0) ; In initial state, (shaked shaker1). So empty, clean, and leave the shaker.
(clean-shaker right left shaker1)
(leave right shaker1)
(grasp left shot4) ; grasp the shot with largest index. In this case (shot1, shot2, shot3, shot4), it's shot4.
(fill-shot shot4 ingredient2 left right dispenser2) ;  In initial state, (used shot4 ingredient2). This is same with cocktail-part1 of cocktail3. So prepare cocktail-part1 first for efficient planning without cleaning the shot.
(pour-shot-to-clean-shaker shot4 ingredient2 shaker1 left l0 l1)
(clean-shot shot4 ingredient2 left right) ; clean shot4.
(fill-shot shot4 ingredient3 left right dispenser3) ; Prepare cocktail-part2.
(grasp right shaker1)
(pour-shot-to-used-shaker shot4 ingredient3 shaker1 left l1 l2)
(leave left shot4)
(shake cocktail3 ingredient2 ingredient3 shaker1 right left) ; cocktail-part1 is first parameter, and then cockail-part2 comes as next parameter in shake action.
(pour-shaker-to-shot cocktail3 shot3 right shaker1 l2 l1) ; (contains shot3 cocktail3) is achieved.
; unit cost = 14 (unit cost)