(grasp left shot4) ; grasp the shot with largest index. In this case (shot1, shot2, shot3, shot4), it's shot4.
(fill-shot shot4 ingredient3 left right dispenser3) ; Prepare first ingredient.
(pour-shot-to-clean-shaker shot4 ingredient3 shaker1 left l0 l1)
(clean-shot shot4 ingredient3 left right) ; clean shot4.
(fill-shot shot4 ingredient2 left right dispenser2) ; Prepare second ingredient.
(pour-shot-to-used-shaker shot4 ingredient2 shaker1 left l1 l2)
(leave left shot4)
(grasp right shaker1)
(shake cocktail1 ingredient3 ingredient2 shaker1 right left) ; cocktail-part1(ingredient3) is first parameter, and then cockail-part2(ingredient2) comes as next parameter in shake action.
(pour-shaker-to-shot cocktail1 shot1 right shaker1 l2 l1) ; (contains shot1 cocktail1) is achieved.
; cost = 10 (unit cost)
