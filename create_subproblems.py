from pathlib import Path
import re

original = Path("../experiments/barman/backup/barman4_1.pddl")
output_dir = Path("../experiments/barman/plan")

problem = original.read_text()

subgoals = [
    "(contains shot1 cocktail1)",
    "(contains shot2 cocktail2)",
    "(contains shot3 cocktail3)",
    "(contains shot4 cocktail4)",
]

# Replace everything from (:goal to the final closing parentheses
goal_pattern = re.compile(
    r"\s*\(:goal\s*\(and.*?\)\s*\)\s*\)\s*$",
    re.DOTALL
)

for i, subgoal in enumerate(subgoals, start=1):
    new_goal = f"""
  (:goal
    (and {subgoal})))
"""

    new_problem = goal_pattern.sub(new_goal, problem)

    output_file = output_dir / f"barman_subgoal_4_{i}.pddl"
    output_file.write_text(new_problem)

    print(f"Created: {output_file}")
