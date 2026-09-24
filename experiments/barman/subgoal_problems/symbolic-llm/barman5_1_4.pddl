
    (define (problem prob-4)
        (:domain barman)
        (:objects shaker1 - shaker 
    left right - hand 
    shot1 shot2 shot3 shot4 shot5 shot6 - shot 
    ingredient1 ingredient2 ingredient3 - ingredient 
    cocktail1 cocktail2 cocktail3 cocktail4 cocktail5 - cocktail 
    dispenser1 dispenser2 dispenser3 - dispenser 
    l0 l1 l2 - level)
        (:init 
            (clean shot5)
(clean shot6)
(cocktail-part1 cocktail1 ingredient2)
(cocktail-part1 cocktail2 ingredient1)
(cocktail-part1 cocktail3 ingredient3)
(cocktail-part1 cocktail4 ingredient1)
(cocktail-part1 cocktail5 ingredient2)
(cocktail-part2 cocktail1 ingredient1)
(cocktail-part2 cocktail2 ingredient3)
(cocktail-part2 cocktail3 ingredient2)
(cocktail-part2 cocktail4 ingredient3)
(cocktail-part2 cocktail5 ingredient3)
(contains shaker1 cocktail4)
(contains shot1 cocktail1)
(contains shot2 cocktail2)
(contains shot3 cocktail3)
(contains shot4 cocktail4)
(dispenses dispenser1 ingredient1)
(dispenses dispenser2 ingredient2)
(dispenses dispenser3 ingredient3)
(empty shot5)
(empty shot6)
(handempty left)
(holding right shaker1)
(next l0 l1)
(next l1 l2)
(ontable shot1)
(ontable shot2)
(ontable shot3)
(ontable shot4)
(ontable shot5)
(ontable shot6)
(shaked shaker1)
(shaker-empty-level shaker1 l0)
(shaker-level shaker1 l1)
        )      
        (:goal (and (contains shot5 cocktail5)))
        
    )
    