import os
import symbolic as sym
import argparse


# Main function to run planner and calculate average planning time for each problem size
def run_fd(domain, planner, p_size, p_idx, path):
    total_times = {size: [] for size in p_size}
    success_counts = {size: 0 for size in p_size}

    print(f"Domain {domain}, using planner {planner}")

    # Create directory for results if it does not exist
    results_dir = f"../experiments/{domain}/plan/{planner}"
    os.makedirs(results_dir, exist_ok=True)

    with open(os.path.join(results_dir, "summary.txt"), "a") as summary_file:
        for prob_size in p_size:
            for prob_idx in p_idx:
                domain_f = f"../domains/domain_{domain}.pddl"
                problem_f = f"../experiments/{domain}/problem/{domain}{prob_size}_{prob_idx}.pddl"
                fd_sas_f = f"../experiments/{domain}/plan/{planner}/{domain}{prob_size}_{prob_idx}.pddl.sas"
                fd_plan_f = f"../experiments/{domain}/plan/{planner}/{domain}{prob_size}_{prob_idx}.pddl"

                success, plan, output, planning_time = sym.fd_planner(fd_plan_f, fd_sas_f, domain_f, problem_f, planner, path)

                if success:
                    total_times[prob_size].append(planning_time)
                    success_counts[prob_size] += 1
                    summary_str = f"Problem Size: {prob_size}, Problem Index: {prob_idx} - Success\n"
                    summary_file.write(summary_str)
                    print(summary_str)

                    summary_str = f"Planning Time: {planning_time:.4f} seconds\n"
                    summary_file.write(summary_str)
                    print(summary_str)

                else:
                    summary_str = f"Problem Size: {prob_size}, Problem Index: {prob_idx} - Failed\n"
                    summary_file.write(summary_str)
                    print(summary_str)

            # After all problem indices for a specific size are completed
            if success_counts[prob_size] > 0:
                average_time = sum(total_times[prob_size]) / success_counts[prob_size]
                summary_str = f"\nAverage planning time for problem size {prob_size} (successful only): {average_time:.4f} seconds\n"
                summary_file.write(summary_str)
                print(summary_str)

            else:
                summary_str = f"No successful plans for problem size {prob_size}\n\n"
                summary_file.write(summary_str)
                print(summary_str)


def main():
    '''
        example
        run_fd("barman", "seq-opt-fdss-1", range(2, 11), [1], path)
        run_fd("blocksworld", "seq-opt-fdss-1", range(3, 11), [1], path)
        run_fd("gripper", "seq-opt-fdss-1", range(2, 11), [1], path)
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", type=str, required=True, choices=["barman", "blocksworld", "gripper"], help="Name of PDDL domain")
    parser.add_argument("--planner", type=str, required=True, choices=["seq-opt-fdss-1", "seq-sat-lama-2011"], default="seq-opt-fdss-1", help="Fast Downward planner configuration")
    parser.add_argument("--sizes", type=int, nargs="+", default=list(range(3, 11)),
                        help="Number of objects (e.g. --sizes 2 3 4 5 6 7 8 9 10)")
    parser.add_argument("--path", type=str, required=True, help="Path to fast-downward.py")
    args = parser.parse_args()
    path = args.path

    run_fd(args.domain, args.planner, args.sizes, [1], path)


if __name__ == "__main__":
    main()
