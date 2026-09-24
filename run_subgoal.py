import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

import argparse
import time
from collections import defaultdict

import pddlpy
import symbolic as sym
from utils import llm_functions as llm

from subgoal import (
    generate_subgoals,
    solve_symbolic_llm,
    solve_mcts_llm
)


# ============================================================
# RUN SYMBOLIC-LLM / MCTS-LLM EXPERIMENT
# ============================================================

def run(
    model,
    max_tokens,
    domain,
    subgoal_planner,
    temperature,
    p_num,
    p_size,
    p_idx,
    planner=None,
    path=None
):
    results = defaultdict(list)

    results_dir = os.path.join(
        BASE_DIR,
        f"experiments/{domain}/plan/{subgoal_planner}/"
    )

    os.makedirs(results_dir, exist_ok=True)

    domain_f = os.path.join(BASE_DIR, f"domains/domain_{domain}.pddl")

    for plan_number in p_num:

        for prob_size in p_size:

            for prob_idx in p_idx:

                problem_f = os.path.join(
                    BASE_DIR,
                    f"experiments/{domain}/problem/{domain}{prob_size}_{prob_idx}.pddl"
                )

                if not os.path.exists(problem_f):
                    print(
                        f"Problem file not found: {problem_f}"
                    )
                    results[
                        (prob_size, plan_number)
                    ].append(
                        (prob_idx, None, False)
                    )
                    continue

                print()
                print("=" * 70)
                print("SUBGOAL PLANNING EXPERIMENT")
                print("=" * 70)
                print(f"Domain          : {domain}")
                print(f"Problem size    : {prob_size}")
                print(f"Problem index   : {prob_idx}")
                print(f"Model           : {model}")
                print(f"Subgoal planner : {subgoal_planner}")
                print(f"Temperature     : {temperature}")

                if planner:
                    print(f"Planner         : {planner}")

                print("=" * 70)

                try:

                    # ------------------------------------------------
                    # Load PDDL problem
                    # ------------------------------------------------

                    domprob = pddlpy.DomainProblem(
                        domain_f,
                        problem_f
                    )

                    with open(problem_f, "r") as f:
                        problem = f.read()

                    # ------------------------------------------------
                    # Generate subgoals using LLM
                    # ------------------------------------------------

                    start_time = time.perf_counter()

                    subgoals = generate_subgoals(
                        model=model,
                        domain=domain,
                        problem=problem,
                        max_tokens=max_tokens,
                        temperature=temperature
                    )

                    print()
                    print("Generated subgoals:")
                    print("-" * 50)

                    for i, subgoal in enumerate(
                        subgoals,
                        start=1
                    ):
                        print(
                            f"Subgoal {i}: {subgoal}"
                        )

                    print(
                        f"Number of subgoals: "
                        f"{len(subgoals)}"
                    )

                    # ------------------------------------------------
                    # Symbolic-LLM
                    # ------------------------------------------------

                    if subgoal_planner == "symbolic-llm":

                        if planner is None:
                            planner = "seq-opt-fdss-1"

                        if path is None:
                            default_fd = os.path.abspath(
                                os.path.join(BASE_DIR, "../downward/fast-downward.py")
                            )
                            if os.path.isfile(default_fd):
                                path = default_fd
                            else:
                                raise ValueError(
                                    "The --path argument is "
                                    "required for symbolic-llm."
                                )

                        plan_f = os.path.join(
                            BASE_DIR,
                            f"experiments/{domain}/plan/symbolic-llm/{domain}{prob_size}_{prob_idx}.pddl"
                        )

                        os.makedirs(
                            os.path.dirname(plan_f),
                            exist_ok=True
                        )

                        print()
                        print("=" * 70)
                        print("STARTING SYMBOLIC-LLM")
                        print("=" * 70)

                        result = solve_symbolic_llm(
                            domprob=domprob,
                            domain=domain,
                            model=model,
                            prob_size=prob_size,
                            prob_idx=prob_idx,
                            subgoals=subgoals,
                            planner=planner,
                            plan_f=plan_f,
                            path=path
                        )

                    # ------------------------------------------------
                    # MCTS-LLM
                    # ------------------------------------------------

                    elif subgoal_planner == "mcts-llm":

                        plan_f = os.path.join(
                            BASE_DIR,
                            f"experiments/{domain}/plan/mcts-llm/{domain}{prob_size}_{prob_idx}_N{plan_number}.pddl"
                        )

                        os.makedirs(
                            os.path.dirname(plan_f),
                            exist_ok=True
                        )

                        print()
                        print("=" * 70)
                        print("STARTING MCTS-LLM")
                        print("=" * 70)

                        result = solve_mcts_llm(
                            domprob=domprob,
                            domain=domain,
                            model=model,
                            plan_f=plan_f,
                            plan_number=plan_number,
                            prob_size=prob_size,
                            prob_idx=prob_idx,
                            subgoals=subgoals,
                            max_tokens=max_tokens,
                            temperature=temperature
                        )

                    else:

                        raise ValueError(
                            "Unknown subgoal planner: "
                            f"{subgoal_planner}"
                        )

                    end_time = time.perf_counter()

                    planning_time = (
                        end_time - start_time
                    )

                    # ------------------------------------------------
                    # Determine success via symbolic validator
                    # ------------------------------------------------

                    if result is not None and os.path.exists(plan_f) and os.path.getsize(plan_f) > 0:
                        success, val_output = sym.validate(
                            domain_f=domain_f,
                            problem_f=problem_f,
                            plan_f=plan_f
                        )
                        if not success:
                            print("Validation output:")
                            print(val_output)
                    else:
                        success = False

                    results[
                        (prob_size, plan_number)
                    ].append(
                        (
                            prob_idx,
                            planning_time,
                            success
                        )
                    )

                    print()
                    print("=" * 70)
                    print("EXPERIMENT RESULT")
                    print("=" * 70)
                    print(
                        f"Problem size    : {prob_size}"
                    )
                    print(
                        f"Problem index   : {prob_idx}"
                    )
                    print(
                        f"Planning time   : "
                        f"{planning_time:.4f} seconds"
                    )
                    print(
                        f"Success         : {success}"
                    )
                    print("=" * 70)

                except Exception as e:

                    print()
                    print("=" * 70)
                    print("EXPERIMENT FAILED")
                    print("=" * 70)
                    print(
                        f"Problem size={prob_size}, "
                        f"problem index={prob_idx}"
                    )
                    print(
                        f"Error: {e}"
                    )
                    print("=" * 70)

                    results[
                        (prob_size, plan_number)
                    ].append(
                        (
                            prob_idx,
                            None,
                            False
                        )
                    )

    # ========================================================
    # SUMMARY
    # ========================================================

    summary_file_path = os.path.join(
        results_dir,
        "summary.txt"
    )

    with open(
        summary_file_path,
        "a"
    ) as summary_file:

        for (
            prob_size,
            plan_number
        ), result_list in results.items():

            successful_results = [
                planning_time
                for _, planning_time, success
                in result_list
                if success
                and planning_time is not None
            ]

            if successful_results:

                avg_time = (
                    sum(successful_results)
                    / len(successful_results)
                )

                success_count = (
                    len(successful_results)
                )

                success_rate = (
                    success_count
                    / len(result_list)
                )

            else:

                avg_time = 0
                success_rate = 0

            summary_str = (
                f"Problem size: {prob_size}, "
                f"Plan number: {plan_number}\n"
                f"Average planning time: "
                f"{avg_time:.4f} seconds\n"
                f"Success rate: "
                f"{success_rate:.4%}\n"
            )

            summary_file.write(
                summary_str
            )

            print()
            print(summary_str)

            for (
                prob_idx,
                _,
                success
            ) in result_list:

                status = (
                    "Success"
                    if success
                    else "Failure"
                )

                problem_str = (
                    f"Problem {prob_idx}: "
                    f"{status}\n"
                )

                summary_file.write(
                    problem_str
                )

                print(problem_str)

            summary_file.write("\n")


# ============================================================
# MAIN
# ============================================================

def main():

    default_model = os.getenv("LLM_MODEL", llm.DEFAULT_MODEL)
    default_fd = os.getenv(
        "FD_PATH",
        os.path.abspath(os.path.join(BASE_DIR, "../downward/fast-downward.py"))
    )

    parser = argparse.ArgumentParser(
        description=(
            "Run subgoal-based Symbolic-LLM "
            "or MCTS-LLM planning."
        )
    )

    parser.add_argument(
        "--model",
        type=str,
        default=default_model,
        help="LLM model name (e.g. Qwen/Qwen3-32B)"
    )

    parser.add_argument(
        "--domain",
        type=str,
        required=True,
        choices=[
            "barman",
            "blocksworld",
            "gripper"
        ],
        help="PDDL domain"
    )

    parser.add_argument(
        "--subgoal_planner",
        "--subgoalplanner",
        dest="subgoal_planner",
        type=str,
        required=True,
        choices=[
            "symbolic-llm",
            "mcts-llm"
        ],
        help=(
            "Subgoal planner to use."
        )
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="LLM temperature"
    )

    parser.add_argument(
        "--planner",
        type=str,
        default="seq-opt-fdss-1",
        help=(
            "Fast Downward planner used by "
            "symbolic-llm."
        )
    )

    parser.add_argument(
        "--sizes",
        type=int,
        nargs="+",
        default=list(range(2, 11)),
        help=(
            "Problem sizes, e.g. "
            "--sizes 2 3 4 5"
        )
    )

    parser.add_argument(
        "--ns",
        type=int,
        nargs="+",
        default=[1],
        help=(
            "Plan numbers / number of candidate "
            "plans used by MCTS-LLM."
        )
    )

    parser.add_argument(
        "--path",
        type=str,
        default=default_fd if os.path.isfile(default_fd) else None,
        help=(
            "Path to fast-downward.py. "
            "Used for symbolic-llm."
        )
    )

    args = parser.parse_args()

    run(
        model=args.model,
        max_tokens=4096,
        domain=args.domain,
        subgoal_planner=args.subgoal_planner,
        temperature=args.temperature,
        p_num=args.ns,
        p_size=args.sizes,
        p_idx=[1],
        planner=args.planner,
        path=args.path
    )


if __name__ == "__main__":
    main()
