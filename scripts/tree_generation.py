import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import prompts, llm_functions as llm
import time
import tree as t
import symbolic as sym
import pddlpy
from collections import defaultdict
import re


'''
Prompt LLM to generate N plans 
and generate an action tree
'''


def sample_plan_once(model, domain, problem, plan_number, max_tokens, temperature=0.7):
    if domain == "barman":
        args = prompts.get_barman_args(plan_number)
    if domain == "blocksworld":
        args = prompts.get_blocksworld_args(plan_number)
    if domain == "gripper":
        args = prompts.get_gripper_args(plan_number)
    system_prompt = args.subgoal_mcts_prompt
    # system_prompt = args.mcts_prompt

    chat_history = [{
        "role": "system",
        "content": system_prompt
    }]

    user_prompt = f'''
        Question: 
        Problem PDDL: \n{problem}\n
        {plan_number} different plan PDDL: 
        '''
    chat_history.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    completion = llm.get_session_completion(chat_history, model=model, max_tokens=max_tokens,
                                            temperature=temperature, logprobs=True)

    return completion


def apply_action(state, action_str, domprob):
    """Applies an action to the current state and returns the updated state."""
    parts = action_str.replace('(', '').replace(')', '').split()
    action_name = parts[0]
    action_params = parts[1:]

    action = domprob.domain.operators[action_name]
    if not action:
        raise ValueError(f"Action {action_name} not found in domain")

    # Binding action parameters
    bindings = dict(zip(action.variable_list.keys(), action_params))

    def bind(var):
        return bindings.get(var, var)

    state_dict = defaultdict(set, {pred: set(tuples) for pred, tuples in state})

    # Check preconditions
    def check_preconditions():
        # Specific handling for 'fill-shot' action
        if action_name == "fill-shot":
            # Collect conditions to check
            conditions_to_check = []
            for precond in action.precondition_pos:
                pred = precond.predicate[0]
                args = precond.predicate[1:]

                if pred == "clean":
                    conditions_to_check.append(tuple(bind(a) for a in args))
                elif pred == "used":
                    conditions_to_check.append(tuple(bind(a) for a in args))
                else:
                    if tuple(bind(a) for a in args) not in state_dict.get(pred, set()):
                        return False, precond

            # Check if at least one of the conditions (clean or used) is satisfied
            if not any(cond in state_dict.get("clean", set()) or cond in state_dict.get("used", set()) for cond in conditions_to_check):
                return False, "(clean ?s) and (used ?s ?i) both"

        else:
            # General precondition check
            for precond in action.precondition_pos:
                pred = precond.predicate[0]
                args = precond.predicate[1:]
                if tuple(bind(a) for a in args) not in state_dict.get(pred, set()):
                    return False, precond

        return True, None
    satisfied, unmet_precond = check_preconditions()
    if not satisfied:
        raise ValueError(f"Preconditions {unmet_precond} failed for action {action_name}")

    # Apply effects
    new_state = defaultdict(set, {k: set(v) for k, v in state_dict.items()})
    for effect in action.effect_pos:
        pred = effect.predicate[0]
        args = effect.predicate[1:]
        new_state[pred].add(tuple(bind(a) for a in args))
    for effect in action.effect_neg:
        pred = effect.predicate[0]
        args = effect.predicate[1:]
        new_state[pred].discard(tuple(bind(a) for a in args))

    keys_to_remove = [key for key, value in new_state.items() if not value]

    for key in keys_to_remove:
        del new_state[key]

    new_state = tuple(sorted((k, tuple(sorted(v))) for k, v in new_state.items()))
    return new_state


def pddl_str_to_state_tuple(pddl_str):
    state_elements = re.findall(r'\((.*?)\)', pddl_str)
    state_tuple = []

    for element in state_elements:
        parts = element.split()
        predicate = parts[0]
        parameters = tuple(parts[1:])
        state_tuple.append((predicate, parameters))

    return tuple(state_tuple)


def state_tuple_to_pddl_str(state_tuple):
    pddl_str = ""

    for state in state_tuple:
        predicate = state[0]
        objects = state[1]

        for obj in objects:
            obj_str = " ".join(obj)
            pddl_str += f"({predicate} {obj_str})\n"

    return pddl_str.strip()


def create_state_tree(domprob, model, plan_number, domain, problem, max_tokens, temperature):
    completion = sample_plan_once(model, domain, problem, plan_number, max_tokens, temperature=temperature)
    actions_with_prob = llm.seq_prob(completion)  # list(zip(actions, action_probabilities))

    # split actions
    plans = []
    current_plan = []
    for action, prob in actions_with_prob:
        if action.startswith("Plan PDDL") or action.startswith("plan"):
            if current_plan:
                plans.append(current_plan)
                current_plan = []
        elif action and not action.startswith("; cost"):
            current_plan.append((action, prob))
    if current_plan:
        plans.append(current_plan)

    # plans[0]: Plan PDDL 1, plans[1]: Plan PDDL 2, ...
    plans = [plan for plan in plans if plan]

    for i in range(len(plans)):
        print(f"Plan {i + 1}: ")
        for j in range(len(plans[i])):
            print(plans[i][j][0])
        print()


    # construct action tree
    initial_state_set = domprob.initialstate()
    initial_state = defaultdict(set)
    for atom in initial_state_set:
        predicate = atom.predicate[0]
        args = atom.predicate[1:]
        initial_state[predicate].add(tuple(args))
    initial_state = tuple(sorted((k, tuple(sorted(v))) for k, v in initial_state.items()))
    tree = t.Tree(initial_state)

    for idx1, plan in enumerate(plans):
        state = initial_state
        parent_node = state
        for idx2, (action, prob) in enumerate(plan):
            try:
                new_state = apply_action(state, action, domprob)
                child_node = new_state
                tree.add_node(parent_node, child_node, action, prob, [idx1+1, idx2+1], 0, 0)
                parent_node = child_node
                state = new_state
            except ValueError as e:
                print(f"In Plan {idx1+1}, {idx2+1}th action {action} is failed.")
                print(f"Error applying action: {e}")
                break
    return tree
