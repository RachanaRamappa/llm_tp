import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import prompts, llm_functions as llm
from scripts import tree_generation as tg
from scripts import mcts
import pddlpy
import time
from scripts import symbolic as sym
import re
from collections import defaultdict


def generate_subgoals(model, domain, problem, max_tokens, temperature=0.0):
    if domain == "barman":
        args = prompts.get_barman_args(0)
    elif domain == "blocksworld":
        args = prompts.get_blocksworld_args(0)
    elif domain == "gripper":
        args = prompts.get_gripper_args(0)
    else:
        raise ValueError(f"Unknown domain: {domain}")
    system_prompt = args.subgoal_prompt

    chat_history = [{
        "role": "system",
        "content": system_prompt
    }]

    # Defensive check: if problem is passed as a file path, read the file content
    if os.path.isfile(problem):
        with open(problem, "r") as f:
            problem_content = f.read()
    else:
        problem_content = problem

    user_prompt = f'''
    Now we have a new problem defined in this domain
    Problem: {problem_content}
    Subgoals:
    '''
    chat_history.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    completion = llm.get_session_completion(chat_history, model=model, max_tokens=max_tokens,
                                            temperature=temperature, logprobs=True)

    goals_str = completion["choices"][0]['message']["content"]
    # Strip <think> reasoning if present
    if "<think>" in goals_str and "</think>" in goals_str:
        goals_str = goals_str.split("</think>", 1)[1]

    subgoals = re.findall(r'\(:goal\s*\(.*?\)\)\)', goals_str, re.DOTALL)
    if not subgoals:
        subgoals = re.findall(r'\(:goal\s*\(.*?\)\)', goals_str, re.DOTALL)

    chat_history.append(
        {
            "role": "assistant",
            "content": completion["choices"][0]['message']["content"]
        }
    )
    print("Subgoals: \n", subgoals)

    return subgoals


def create_pddl_problem_file(new_problem_f, domain_name, init_state, subgoal, objects, i):
    os.makedirs(os.path.dirname(new_problem_f), exist_ok=True)
    pddl_problem_str = f"""
    (define (problem prob-{i})
        (:domain {domain_name})
        (:objects {objects})
        (:init 
            {init_state}
        )      
        {subgoal}
        
    )
    """
    with open(new_problem_f, "w") as file:
        file.write(pddl_problem_str)


def connect_trees(trees):
    if not trees:
        raise ValueError("The list of trees is empty. Cannot connect trees.")

    # Start with the first tree as the base
    main_tree = trees[0]

    # Iterate over the list of trees
    for i in range(len(trees) - 1):
        current_tree = trees[i]
        next_tree = trees[i + 1]
        next_tree_root = next_tree.root

        # Find a matching leaf node in the current tree that matches the root of the next tree
        matching_leaf = None
        for node in current_tree.G.nodes:
            if node == next_tree_root:
                matching_leaf = node
                break

        if matching_leaf is None:
            raise ValueError(f"No matching leaf node found in Tree {i} for connecting to Tree {i + 1}'s root.")

        # Connect the matching leaf node of the current tree to the root node of the next tree
        main_tree.add_node(matching_leaf, next_tree_root, action=None, weight=1, indices=[i, 0], visits=0, win=0)

        # Add all nodes and edges from next_tree into main_tree
        for node in next_tree.G.nodes:
            if node != next_tree_root:  # Avoid re-adding the root node
                main_tree.G.add_node(node, **next_tree.G.nodes[node])

        for edge in next_tree.G.edges(data=True, keys=True):
            u, v, key, data = edge
            main_tree.G.add_edge(u, v, key=key, **data)

    return main_tree


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def solve_symbolic_llm(domprob, domain, model, prob_size, prob_idx, subgoals, planner, plan_f, path):
    domain_f = os.path.join(BASE_DIR, f"domains/domain_{domain}.pddl")
    problem_f = os.path.join(BASE_DIR, f"experiments/{domain}/problem/{domain}{prob_size}_{prob_idx}.pddl")

    # read original initial state from problem file
    with open(problem_f, 'r') as file:
        pddl_content = file.read()

    init_match = re.search(r'\(:init\s*(.*?)\)\s*\(:goal', pddl_content, re.DOTALL)
    initial_state_str = ""
    if init_match:
        initial_state_str = init_match.group(1).strip()
    states = [initial_state_str]
    subgoal_plans = []

    initial_state_set = domprob.initialstate()
    initial_state = defaultdict(set)
    for atom in initial_state_set:
        predicate = atom.predicate[0]
        args = atom.predicate[1:]
        initial_state[predicate].add(tuple(args))
    initial_state = tuple(sorted((k, tuple(sorted(v))) for k, v in initial_state.items()))
    state = initial_state

    objects_match = re.search(r'\(:objects\s*(.*?)\)\s*\(:', pddl_content, re.DOTALL)
    objects_str = ""
    if objects_match:
        objects_str = objects_match.group(1).strip()

    plan_dir = os.path.join(BASE_DIR, f"experiments/{domain}/plan/symbolic-llm")
    os.makedirs(plan_dir, exist_ok=True)
    subgoal_problems_dir = os.path.join(BASE_DIR, f"experiments/{domain}/subgoal_problems/symbolic-llm")
    os.makedirs(subgoal_problems_dir, exist_ok=True)

    for i, subgoal in enumerate(subgoals):
        subgoal_plan_f = os.path.join(plan_dir, f"{domain}{prob_size}_{prob_idx}_{i}.pddl")
        subgoal_sas_f = os.path.join(plan_dir, f"{domain}{prob_size}_{prob_idx}__{i}.pddl.sas")

        # Create new problem pddl. initial state: states[i], goal state: subgoal
        new_problem_f = os.path.join(subgoal_problems_dir, f"{domain}{prob_size}_{prob_idx}_{i}.pddl")
        create_pddl_problem_file(new_problem_f, domain, states[i], subgoal, objects_str, i)

        success, subgoal_plan, output, planning_time = sym.fd_planner(subgoal_plan_f, subgoal_sas_f, domain_f, new_problem_f, planner, path)
        action_lines = [l.strip() for l in subgoal_plan.splitlines() if l.strip() and not l.strip().startswith(";")]

        if not success:
            print(f"Subgoal {i} planning failed! Triggering Neuro-Symbolic Task Replanning...")
            from scripts import replanning
            replan_ok, repaired_plan, _ = replanning.replan_problem_pddl(
                domain_f=domain_f,
                problem_f=new_problem_f,
                error_message=output,
                planner=planner,
                path=path,
                plan_output_f=subgoal_plan_f
            )
            if replan_ok:
                print(f"Subgoal {i} successfully recovered via replanning!")
                success = True
                subgoal_plan = repaired_plan
                # update action_lines with repaired plan
                action_lines = [l.strip() for l in subgoal_plan.splitlines() if l.strip() and not l.strip().startswith(";")]
            else:
                print(f"Subgoal {i} replanning recovery failed.")
                break

        subgoal_plans.append(subgoal_plan)

        if action_lines:
            for action in action_lines:
                try:
                    new_state = tg.apply_action(state, action, domprob)
                    state = new_state
                except ValueError as e:
                    print(f"Error applying action: {e}")
                    break
        else:
            new_state = state
            print("No action needed")

        new_state_str = tg.state_tuple_to_pddl_str(new_state)
        states.append(new_state_str)


    # save the final plan
    os.makedirs(os.path.dirname(plan_f), exist_ok=True)
    with open(plan_f, "w") as f:
        for plan in subgoal_plans:
            f.write(plan.strip())
            f.write("\n")
    with open(plan_f, "r") as f:
        final_plan = f.read()
    return final_plan


def solve_mcts_llm(domprob, domain, model, plan_f, plan_number, prob_size, prob_idx, subgoals, max_tokens, temperature):
    domain_f = os.path.join(BASE_DIR, f"domains/domain_{domain}.pddl")
    problem_f = os.path.join(BASE_DIR, f"experiments/{domain}/problem/{domain}{prob_size}_{prob_idx}.pddl")

    print(f"using model: {model}, plan_number: {plan_number}, prob_size: {prob_size}, prob_idx: {prob_idx}, subgoals: {subgoals}")

    with open(problem_f, 'r') as file:
        pddl_content = file.read()

    init_match = re.search(r'\(:init\s*(.*?)\)\s*\(:goal', pddl_content, re.DOTALL)
    initial_state_str = ""
    if init_match:
        initial_state_str = init_match.group(1).strip()
    states = [initial_state_str]

    initial_state_set = domprob.initialstate()
    initial_state = defaultdict(set)
    for atom in initial_state_set:
        predicate = atom.predicate[0]
        args = atom.predicate[1:]
        initial_state[predicate].add(tuple(args))
    initial_state = tuple(sorted((k, tuple(sorted(v))) for k, v in initial_state.items()))
    state = initial_state

    objects_match = re.search(r'\(:objects\s*(.*?)\)\s*\(:', pddl_content, re.DOTALL)
    objects_str = ""
    if objects_match:
        objects_str = objects_match.group(1).strip()

    trees = []
    states_pathes = [[initial_state]]
    actions_pathes = []

    plan_dir = os.path.join(BASE_DIR, f"experiments/{domain}/plan/mcts-llm")
    os.makedirs(plan_dir, exist_ok=True)
    subgoal_problems_dir = os.path.join(BASE_DIR, f"experiments/{domain}/subgoal_problems/mcts-llm")
    os.makedirs(subgoal_problems_dir, exist_ok=True)

    for i, subgoal in enumerate(subgoals):
        subgoal_plan_f = os.path.join(plan_dir, f"{domain}{prob_size}_{prob_idx}_{i}.pddl")
        subgoal_sas_f = os.path.join(plan_dir, f"{domain}{prob_size}_{prob_idx}_{i}.pddl.sas")
        new_problem_f = os.path.join(subgoal_problems_dir, f"{domain}{prob_size}_{prob_idx}_{i}.pddl")
        create_pddl_problem_file(new_problem_f, domain, states[i], subgoal, objects_str, i)
        with open(new_problem_f, "r") as file:
            new_problem = file.read()

        subgoal_domprob = pddlpy.DomainProblem(domain_f, new_problem_f)

        tree = tg.create_state_tree(subgoal_domprob, model, plan_number, domain, new_problem, max_tokens, temperature)
        states_path, actions_path = mcts.mcts(tree, subgoal_domprob, 50)
        trees.append(tree)

        if states_path != ["; cost = 0 (unit cost)"]:
            states_pathes.append(states_path[1:])

        if actions_path != ["; cost = 0 (unit cost)"]:
            actions_pathes.append(actions_path)

        if states_path and actions_path:  # the planning succeed
            if states_path == ["; cost = 0 (unit cost)"] and actions_path == ["; cost = 0 (unit cost)"]:
                new_state = states_pathes[-1][-1]
                new_state_str = tg.state_tuple_to_pddl_str(new_state)
                states.append(new_state_str)
            else:
                new_state = states_path[-1]
                new_state_str = tg.state_tuple_to_pddl_str(new_state)
                states.append(new_state_str)
                continue
        else:
            print(f"Subgoal {i} MCTS search failed! Triggering Neuro-Symbolic Task Replanning...")
            fd_ok, fd_plan, _, _ = sym.fd_planner(subgoal_plan_f, subgoal_sas_f, domain_f, new_problem_f, "seq-opt-fdss-1", None)
            if fd_ok and fd_plan.strip():
                action_lines = [l.strip() for l in fd_plan.splitlines() if l.strip() and not l.strip().startswith(";")]
                actions_pathes.append(action_lines)
                print(f"Subgoal {i} successfully recovered via replanning ({len(action_lines)} actions)!")
                # advance state
                curr_st = state
                for act in action_lines:
                    try:
                        curr_st = tg.apply_action(curr_st, act, domprob)
                    except Exception:
                        pass
                state = curr_st
                new_state_str = tg.state_tuple_to_pddl_str(state)
                states.append(new_state_str)
                continue
            else:
                print(f"Subgoal {i} planning failed!")
                break

    try:
        connected_tree = connect_trees(trees)
    except ValueError as e:
        connected_tree = None
        print(e)

    os.makedirs(os.path.dirname(plan_f), exist_ok=True)
    with open(plan_f, "w") as f:
        for actions_path in actions_pathes:
            for action in actions_path:
                f.write(f"{action}\n")
            f.write("\n")  # add a newline between subgoal plans

    with open(plan_f, "r") as f:
        final_plan = f.read()

    combined_states_path = [state for states_path in states_pathes for state in states_path]
    combined_actions_path = [action for actions_path in actions_pathes for action in actions_path]

    return connected_tree, final_plan, combined_states_path, combined_actions_path

