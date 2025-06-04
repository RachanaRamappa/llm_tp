import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import symbolic as sym
from collections import defaultdict
import utils.prompts as prompts
import utils.llm_functions as llm
import os
import argparse


# chain-of-thought
def cot(model, domain, problem, temperature):
    if domain == "barman":
        args = prompts.get_barman_args(1)
    if domain == "blocksworld":
        args = prompts.get_blocksworld_args(1)
    if domain == "gripper":
        args = prompts.get_gripper_args(1)
    system_prompt = args.cot_prompt

    chat_history = []
    chat_history.append({
        "role": "system",
        "content": system_prompt
    })

    user_prompt = f'''
    Question:
    Problem PDDL: \n{problem}\n
    Plan PDDL:
    '''

    chat_history.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    completion = llm.get_session_completion(chat_history, model=model, max_tokens=4096, temperature=temperature, logprobs=False)
    response_text = completion["choices"][0]['message']["content"].strip()

    return response_text


def run_cot_experiment(domain, prob_size, prob_idx, model, max_tokens, algorithm, temperature):
    domain_f = f"../domains/domain_{domain}.pddl"
    problem_f = f"../experiments/{domain}/problem/{domain}{prob_size}_{prob_idx}.pddl"
    llm_plan_f = f"../experiments/{domain}/plan/{algorithm}/{domain}{prob_size}_{prob_idx}.pddl"

    with open(problem_f, "r") as f:
        problem = f.read()

    start_time = time.perf_counter()
    plan = cot(model, domain, problem, temperature)
    end_time = time.perf_counter()
    planning_time = end_time - start_time

    with open(llm_plan_f, "w") as f:
        f.write(plan)

    success, log = sym.validate(domain_f=domain_f, problem_f=problem_f, plan_f=llm_plan_f)

    print(f"Problem size: {prob_size}, Problem idx: {prob_idx}, Success: {success}")

    return planning_time, success


def run(model, max_tokens, domain, algorithm, temperature, p_num, p_size, p_idx):
    results = defaultdict(list)
    # Create directory for results if it does not exist
    results_dir = f"../experiments/{domain}/plan/{algorithm}/"
    os.makedirs(results_dir, exist_ok=True)

    for plan_number in p_num:
        for prob_size in p_size:
            for prob_idx in p_idx:
                try:
                    planning_time, success = run_cot_experiment(domain, prob_size, prob_idx, model, max_tokens, algorithm, temperature)
                    results[(prob_size, plan_number)].append((prob_idx, planning_time, success))
                except Exception as e:
                    print(f"Experiment failed for prob_size={prob_size}, prob_idx={prob_idx}, plan_number={plan_number}. Error: {e}")
                    results[(prob_size, plan_number)].append((prob_idx, None, False))

    # Calculate and print summary statistics
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

            for prob_idx, _, success in result_list:
                status = "Success" if success else "Failure"
                problem_str = f"Problem {prob_idx}: {status}\n"
                summary_file.write(problem_str)
                print(problem_str)
            summary_file.write("\n")
            print()


def main():
    '''
    example
    run("gpt-4o", 4096, "barman", "cot", 0.0, [1], range(2, 11), [1])
    run("gpt-4o", 4096, "blocksworld", "cot", 0.0, [1], range(3, 11), [1])
    run("gpt-4o", 4096, "gripper", "cot", 0.0, [1], range(2, 11), [1])
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True, default="gpt-4o", help="Name of gpt model")
    parser.add_argument("--domain", type=str, required=True, choices=["barman", "blocksworld", "gripper"], help="Name of PDDL domain")
    parser.add_argument("--temperature", type=float, required=True, default=0.0, help="temparature of llm")
    parser.add_argument("--sizes", type=int, nargs="+", default=list(range(3, 11)),
                        help="Number of objects (e.g. --sizes 2 3 4 5 6 7 8 9 10)")
    args = parser.parse_args()

    run(args.model, 4096, args.domain, "cot", args.temperature, [1], args.sizes, [1])


if __name__ == "__main__":
    main()
