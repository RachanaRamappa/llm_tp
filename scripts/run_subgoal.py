import time
import symbolic as sym, subgoal
import pddlpy
from collections import defaultdict
import os
import argparse


# run the whole: symbolic-llm or mcts-llm
def run_subgoal_experiment(domain, prob_size, prob_idx, plan_number, model, max_tokens, algorithm, temperature, fd_planner, path):
    domain_f = f"../domains/domain_{domain}.pddl"
    problem_f = f"../experiments/{domain}/problem/{domain}{prob_size}_{prob_idx}.pddl"
    if algorithm == "symbolic-llm":
        plan_f = f"../experiments/{domain}/plan/{algorithm}/{domain}{prob_size}_{prob_idx}.pddl"
    else:
        plan_f = f"../experiments/{domain}/plan/{algorithm}/{domain}{prob_size}_{prob_idx}_N{plan_number}.pddl"

    domprob = pddlpy.DomainProblem(domain_f, problem_f)

    with open(problem_f, "r") as f:
        problem = f.read()

    subgoals = subgoal.generate_subgoals(model, domain, problem, max_tokens, temperature=0.0)
    start_time = time.perf_counter()
    if algorithm == "symbolic-llm":
        final_plan = subgoal.solve_symbolic_llm(domprob, domain, model, prob_size, prob_idx, subgoals, fd_planner, plan_f, path)
    else:
        final_tree, final_plan, states_path, actions_path = subgoal.solve_mcts_llm(domprob, domain, model, plan_f,
                                                                                       plan_number, prob_size, prob_idx,
                                                                                       subgoals, max_tokens, temperature)
    end_time = time.perf_counter()
    planning_time = end_time - start_time

    # if algorithm == "mcts-llm":
    #     final_tree.visualize_tree(states_path, actions_path, planning_time, image_f)

    print("Planning time:", end_time - start_time)

    success, log = sym.validate(domain_f=domain_f, problem_f=problem_f, plan_f=plan_f)
    print(f"Problem size: {prob_size}, Problem idx: {prob_idx}: ", success)

    return planning_time, success


def run(model, max_tokens, domain, algorithm, temperature, fd_planner, p_num, p_size, p_idx, path):
    results = defaultdict(list)

    # Create directory for results if it does not exist
    results_dir = f"../experiments/{domain}/plan/{algorithm}/"
    os.makedirs(results_dir, exist_ok=True)

    results_dir = f"../experiments/{domain}/subgoal_problems/{algorithm}/"
    os.makedirs(results_dir, exist_ok=True)

    for plan_number in p_num:
        for prob_size in p_size:
            for prob_idx in p_idx:
                try:
                    planning_time, success = run_subgoal_experiment(domain, prob_size, prob_idx, plan_number, model, max_tokens, algorithm, temperature, fd_planner, path)
                    results[(prob_size, plan_number)].append((prob_idx, planning_time, success))
                except Exception as e:
                    print(f"Experiment failed for prob_size={prob_size}, prob_idx={prob_idx}, plan_number={plan_number}. Error: {e}")
                    results[(prob_size, plan_number)].append((prob_idx, None, False))

        ## Calculate and print summary statistics
        with open(os.path.join(results_dir, "summary.txt"), "a") as summary_file:
            for (prob_size, plan_number), result_list in results.items():
                successful_results = [time for _, time, success in result_list if success]
                if successful_results:
                    total_time = sum(time for time in successful_results)
                    avg_time = total_time / len(successful_results)

                    success_count = len(successful_results)
                    success_rate = success_count / len(result_list)
                else:
                    avg_time = 0
                    success_rate = 0

                summary_str = (f"Problem size: {prob_size}, Plan number: {plan_number}\n"
                               f"Average planning time: {avg_time:.4f} seconds\n"
                               f"Success rate: {success_rate:.4%}\n")
                summary_file.write(summary_str)
                print(summary_str)

                for prob_idx, _, success, _ in result_list:
                    status = "Success" if success else "Failure"
                    problem_str = f"Problem {prob_idx}: {status}\n"
                    summary_file.write(problem_str)
                    print(problem_str)
                summary_file.write("\n")
                print()


def main():
    '''
    example
    # mcts-llm planner as subgoal planner
    run("gpt-4o", 2048, "barman", "mcts-llm", 0.0, "seq-opt-fdss-1", [3, 4, 5], range(2,11), [1], path)
    run("gpt-4o", 2048, "blocksworld", "mcts-llm", 0.0, "seq-opt-fdss-1", [3, 4, 5], range(3, 11), [1], path)
    run("gpt-4o", 2048, "gripper", "mcts-llm", 0.0, "seq-opt-fdss-1", [3, 4, 5], range(2, 11), [1], path)

    # symbolic-llm planner as subgoal planner
    run("gpt-4o", 2048, "barman", "symbolic-llm", 0.0, "seq-opt-fdss-1", [1], range(2, 11), [1], path)
    run("gpt-4o", 2048, "blocksworld", "symbolic-llm", 0.0, "seq-opt-fdss-1", [1], range(3, 11), [1], path)
    run("gpt-4o", 2048, "gripper", "symbolic-llm", 0.0, "seq-opt-fdss-1", [1], range(2, 11), [1], path)
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True, default="gpt-4o", help="Name of gpt model")
    parser.add_argument("--domain", type=str, required=True, choices=["barman", "blocksworld", "gripper"], help="Name of PDDL domain")
    parser.add_argument("--subgoal_planner", type=str, required=True, choices=["mcts-llm", "symbolic-llm"], help="Choose subgoal planner")
    parser.add_argument("--temperature", type=float, default=0.0, help="temparature of llm")
    parser.add_argument("--planner", type=str, choices=["seq-opt-fdss-1", "seq-sat-lama-2011"], default="seq-opt-fdss-1", help="Fast Downward planner configuration")
    parser.add_argument("--ns", type=int, nargs="+", default=list(range(1, 2)),
                        help="Number of sampled plans(n_s) when using mcts llm (e.g. --ns 3 4 5)")
    parser.add_argument("--sizes", type=int, nargs="+", default=list(range(3, 11)),
                        help="Number of objects (e.g. --sizes 2 3 4 5 6 7 8 9 10)")
    parser.add_argument("--path", type=str, default="", help="Path to fast-downward.py")

    args = parser.parse_args()

    run(args.model, 2048, args.domain, args.subgoal_planner, args.temperature, args.planner, args.ns, args.sizes, [1], args.path)

if __name__ == "__main__":
    main()