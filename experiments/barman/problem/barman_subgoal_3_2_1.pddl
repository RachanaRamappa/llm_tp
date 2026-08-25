(empty-shaker right shaker1 cocktail1 l1 l0) ; In initial state, (shaked shaker1). So empty, clean, and leave the shaker.
(clean-shaker right left shaker1)
(leave right shaker1)
(grasp left shot4) ; grasp the shot with largest index. In this case (shot1, shot2, shot3, shot4), it's shot4.
(fill-shot shot4 ingredient2 left right dispenser2) ; In initial state, (used shot4 ingredient2). This is same with cocktail-part2 of cocktail2. So prepare cocktail-part2 first for efficient planning without cleaning the shot.
(pour-shot-to-clean-shaker shot4 ingredient2 shaker1 left l0 l1)
(clean-shot shot4 ingredient2 left right) ; clean shot4.
(fill-shot shot4 ingredient1 left right dispenser1) ; Prepare cocktail-part1
(pour-shot-to-used-shaker shot4 ingredient1 shaker1 left l1 l2)
(leave left shot4)
(grasp right shaker1)
(shake cocktail2 ingredient1 ingredient2 shaker1 right left) ; cocktail-part1 is first parameter, and then cocktail-part2 comes as next parameter in shake action.
(pour-shaker-to-shot cocktail2 shot2 right shaker1 l2 l1) ; (contains shot2 cocktail2) is achieved.
; cost = 13 (unit cost)