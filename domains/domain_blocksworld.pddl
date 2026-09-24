(define (domain blocksworld)
  (:requirements :strips)
  (:types block table)
  (:predicates
    ; environment conditions
    (clear ?x - block)
    (on-table ?x - block ?table - table)
    (arm-empty)
    (holding ?x - block)
    (on ?x - block ?y - block)
    (clear-table ?table - table)
  )
  ; When the block is bottom block and clear, pick up the block
  (:action pickup
    :parameters (?ob - block ?table - table)
    :precondition (and (clear ?ob) (on-table ?ob ?table) (arm-empty))
    :effect (and (holding ?ob) (not (clear ?ob))
                 (not (on-table ?ob ?table)) (not (arm-empty))(clear-table ?table)))
  ; When the robot arm is holding the block and nothing is on the table, put down the block on the table
  (:action putdown
    :parameters (?ob - block ?table - table)
    :precondition (and (holding ?ob) (clear-table ?table))
    :effect (and (clear ?ob) (arm-empty)
                 (on-table ?ob ?table) (not (holding ?ob)) (not (clear-table ?table))))
  ; When the robot arm is holding the block, stack the block on the a top block.
  (:action stack
    :parameters (?ob - block ?underob - block)
    :precondition (and (clear ?underob) (holding ?ob))
    :effect (and (arm-empty) (clear ?ob) (on ?ob ?underob)
                 (not (clear ?underob)) (not (holding ?ob))))
  ; When the block is not bottom block and clear, unstack the block.
  (:action unstack
    :parameters (?ob - block ?underob - block)
    :precondition (and (on ?ob ?underob) (clear ?ob) (arm-empty))
    :effect (and (holding ?ob) (clear ?underob)
                 (not (on ?ob ?underob)) (not (clear ?ob))
                 (not (arm-empty))))
)
