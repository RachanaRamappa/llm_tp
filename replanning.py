import os
import sys
import re
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from utils import llm_functions as llm
from scripts import symbolic as sym


REPLAN_PROBLEM_SYSTEM_PROMPT = """You are an expert AI planning engineer and PDDL syntax/semantics specialist.
A symbolic planner (Fast Downward) or PDDL validator encountered an error with a PDDL problem formulation.
Your task is to correct the problem PDDL based on the error message, ensuring all object names, types, initial state predicates, and goal definitions are strictly valid according to the domain PDDL.

Output ONLY the complete, corrected Problem PDDL starting with (define (problem ...).
Do NOT include markdown formatting, backticks, or explanation.
"""


def replan_problem_pddl(
    domain_f,
    problem_f,
    error_message,
    planner="seq-opt-fdss-1",
    path=None,
    plan_output_f=None,
    model=None,
    max_attempts=4,
    temperature=0.0
):
    """
    Implements Neuro-Symbolic Task Replanning (Section V of paper):
    1. Detects failures from Fast Downward (syntax error, unsolvable problem) or VAL validator.
    2. Zero-shot CoT prompt guides LLM in refining the Problem PDDL structure, predicates, or goal states.
    3. Runs Fast Downward on the corrected Problem PDDL to generate the exact valid plan.
    4. Validates the resulting plan with VAL.
    """
    target_model = model or os.getenv("LLM_MODEL", llm.DEFAULT_MODEL)

    with open(domain_f, "r") as f:
        domain_content = f.read()

    with open(problem_f, "r") as f:
        problem_content = f.read()

    current_error = error_message
    current_problem = problem_content

    if not plan_output_f:
        plan_output_f = problem_f.replace(".pddl", ".plan")
    sas_output_f = plan_output_f + ".sas"

    print()
    print("=" * 75)
    print("       NEURO-SYMBOLIC TASK REPLANNING (Section V Framework)")
    print("=" * 75)
    print(f"Problem file : {problem_f}")
    print(f"Domain file  : {domain_f}")
    print(f"Planner      : {planner}")
    print(f"Max attempts : {max_attempts}")
    print("=" * 75)

    history = []

    for attempt in range(1, max_attempts + 1):
        print(f"\n[Replanning Attempt {attempt}/{max_attempts}] Prompting LLM to correct Problem PDDL...")

        user_prompt = f"""Domain PDDL:
{domain_content}

Faulty Problem PDDL:
{current_problem}

Planner / Validator Error Message:
{current_error}

Please analyze the error message, identify any syntax errors, invalid object names, inconsistent predicates, or malformed goals, and provide the fully corrected Problem PDDL.
Remember to output ONLY the corrected PDDL problem definition.
"""

        messages = [
            {"role": "system", "content": REPLAN_PROBLEM_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]

        start_time = time.perf_counter()
        completion = llm.get_session_completion(
            messages,
            model=target_model,
            max_tokens=4095,
            temperature=temperature
        )
        corrected_pddl = completion["choices"][0]["message"]["content"]
        elapsed = time.perf_counter() - start_time

        # Clean code fences
        corrected_pddl = llm.clean_llm_content(corrected_pddl)
        if "define" in corrected_pddl:
            # Extract from (define to the end
            corrected_pddl = "(" + corrected_pddl.split("(", 1)[1]

        # Save corrected problem PDDL
        with open(problem_f, "w") as f:
            f.write(corrected_pddl)

        # Run Fast Downward on the corrected Problem PDDL
        fd_success, plan, fd_output, fd_time = sym.fd_planner(
            plan_f=plan_output_f,
            sas_f=sas_output_f,
            domain_f=domain_f,
            problem_f=problem_f,
            planner=planner,
            path=path
        )

        if fd_success:
            # Validate plan with VAL
            val_success, val_output = sym.validate(domain_f, problem_f, plan_output_f)
            if val_success:
                print(f"Attempt {attempt}: SUCCESS! Problem corrected by LLM ({elapsed:.2f}s). Fast Downward solved it in {fd_time:.2f}s.")
                history.append({"attempt": attempt, "success": True, "time": elapsed + fd_time, "error": None})
                return True, plan, history
            else:
                print(f"Attempt {attempt}: Fast Downward found plan but VAL check failed: {val_output.strip().splitlines()[-1] if val_output else ''}")
                current_error = val_output
        else:
            print(f"Attempt {attempt}: Fast Downward failed on corrected problem: {fd_output.strip().splitlines()[-1] if fd_output else ''}")
            current_error = fd_output

        history.append({"attempt": attempt, "success": False, "time": elapsed + fd_time, "error": current_error})
        current_problem = corrected_pddl

    print(f"\nReplanning exceeded {max_attempts} attempts.")
    return False, "", history


if __name__ == "__main__":
    # Test replanning demonstration on a syntactically/semantically broken problem PDDL
    test_domain = os.path.join(BASE_DIR, "domains/domain_blocksworld.pddl")
    test_problem = os.path.join(BASE_DIR, "experiments/blocksworld/problem/test_syntax_error.pddl")

    # Write a broken problem with malformed syntax: missing parenthesis and invalid predicate (on_table instead of on-table)
    broken_pddl = """(define (problem prob-broken)
  (:domain blocksworld)
  (:objects
    b1 b2 b3 - block
    t1 t2 t3 t4 t5 t6 - table
  )
  (:init
    (arm-empty)
    (on b1 b2)
    (on b2 b3)
    (on_table b3 t3)  ; SYNTAX ERROR: on_table instead of on-table

    (clear b1)
    (clear-table t5)
    (clear-table t2)
    (clear-table t6)
    (clear-table t4)
    (clear-table t1)
  )
  (:goal
    (and
      (on-table b1 t3)
      (on b3 b1)
      (on b2 b3)
    )
  ; SYNTAX ERROR: missing closing parenthesis
"""
    with open(test_problem, "w") as f:
        f.write(broken_pddl)

    # Trigger Fast Downward to catch the syntax error
    test_plan = test_problem.replace(".pddl", ".plan")
    test_sas = test_problem + ".sas"
    success, plan, fd_output, _ = sym.fd_planner(test_plan, test_sas, test_domain, test_problem, "seq-opt-fdss-1", None)

    print(f"Initial planner run on broken problem succeeded: {success}")
    print(f"Planner error:\n{fd_output[:250]}...")

    # Run Neuro-Symbolic Task Replanner to recover
    replan_success, repaired_plan, hist = replan_problem_pddl(
        domain_f=test_domain,
        problem_f=test_problem,
        error_message=fd_output,
        max_attempts=4
    )

    print(f"\nFinal Replanning Recovery Succeeded: {replan_success}")
    if replan_success:
        print(f"Generated Plan:\n{repaired_plan}")
