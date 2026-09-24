
    (define (problem prob-1)
        (:domain barman)
        (:objects shaker1 - shaker 
    left right - hand 
    shot1 shot2 shot3 - shot 
    ingredient1 ingredient2 ingredient3 - ingredient 
    cocktail1 cocktail2 - cocktail 
    dispenser1 dispenser2 dispenser3 - dispenser 
    l0 l1 l2 - level)
        (:init 
            (clean shot3)
(cocktail-part1 cocktail1 ingredient2)
(cocktail-part1 cocktail2 ingredient2)
(cocktail-part2 cocktail1 ingredient1)
(cocktail-part2 cocktail2 ingredient3)
(contains shaker1 cocktail1)
(contains shot1 cocktail1)
(dispenses dispenser1 ingredient1)
(dispenses dispenser2 ingredient2)
(dispenses dispenser3 ingredient3)
(empty shot2)
(empty shot3)
(handempty right)
(holding left shaker1)
(next l0 l1)
(next l1 l2)
(ontable shot1)
(ontable shot2)
(ontable shot3)
(shaked shaker1)
(shaker-empty-level shaker1 l0)
(shaker-level shaker1 l1)
(used shot2 ingredient2)
        )      
        (:goal (and (contains shot2 cocktail2)))
        
    )
    