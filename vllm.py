
import os
import pddlpy

from subgoal import generate_subgoals, solve_mcts_llm

# ============================================================
# CONFIGURATION
# ============================================================

domain = "barman"
problem = "../experiments/barman/problem/barman_context_1.pddl"
model = "Qwen/Qwen3-0.6B"

plan_file = "../experiments/barman/plan/mcts-llm/barman_test.pddl"

plan_number = 1
prob_size = 1
prob_idx = 1

max_tokens = 150
temperature = 0.0

# ============================================================
# CHECK FILES
# ============================================================

print("==============================================")
print("        MCTS-LLM PLANNER TEST")
print("==============================================")

print("Domain :", domain)
print("Problem:", problem)
print("Model  :", model)
print()

print("Problem exists:", os.path.exists(problem))
print("Domain exists :", os.path.exists(f"domains/domain_{domain}.pddl"))

if not os.path.exists(problem):
    raise FileNotFoundError(problem)

if not os.path.exists(f"../domains/domain_{domain}.pddl"):
    raise FileNotFoundError(f"domains/domain_{domain}.pddl")

# ============================================================
# LOAD PDDL
# ============================================================

domprob = pddlpy.DomainProblem(
    f"../domains/domain_{domain}.pddl",
    problem
)

# ============================================================
# GENERATE SUBGOALS
# ============================================================

print()
print("==============================================")
print("        GENERATING SUBGOALS")
print("==============================================")

subgoals = generate_subgoals(
    #domprob=domprob,
    domain=domain,
    model=model,
    problem=problem,
    max_tokens=100,
    temperature=0.0
)

print()
print("Generated subgoals:")

for i, subgoal in enumerate(subgoals, 1):
    print(f"Subgoal {i}:")
    print(subgoal)
    print()

print("Number of subgoals:", len(subgoals))

# ============================================================
# RUN MCTS-LLM
# ============================================================

print()
print("==============================================")
print("        STARTING MCTS-LLM")
print("==============================================")

result = solve_mcts_llm(
    domprob=domprob,
    domain=domain,
    model=model,
    plan_f=plan_file,
    plan_number=plan_number,
    prob_size=prob_size,
    prob_idx=prob_idx,
    subgoals=subgoals,
    max_tokens=max_tokens,
    temperature=temperature
)

# ============================================================
# EXTRACT RESULT
# ============================================================

if isinstance(result, tuple):

    connected_tree = result[0]
    final_plan = result[1]
    states = result[2]
    actions = result[3]

else:

    connected_tree = None
    final_plan = result
    states = []
    actions = []

# ============================================================
# DISPLAY RESULT
# ============================================================

print()
print("==============================================")
print("        FINAL MCTS-LLM PLAN")
print("==============================================")

print(final_plan)

print()
print("==============================================")
print("        ACTIONS")
print("==============================================")

if actions:
    for i, action in enumerate(actions, 1):
        print(f"{i}. {action}")
else:
    print("No actions returned.")

print()
print("==============================================")
print("        STATE PATH")
print("==============================================")

print("Number of states:", len(states))

print()
print("==============================================")
print("        PLAN FILE")
print("==============================================")

print(plan_file)

print()
print("==============================================")
print("        MCTS-LLM TEST FINISHED")
print("==============================================")

