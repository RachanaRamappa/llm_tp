import os
import subprocess
import time


# Run pddl plan validator VAL
def validate(domain_f, problem_f, plan_f):
    # This command only works in Linux
    # For windows, you need exe path of the validator
    cmd = f'"Validate" -v "{domain_f}" "{problem_f}" ' f'"{plan_f}"'
    output = subprocess.getoutput(cmd)

    if "Plan valid" in output:
        return True, output
    else:
        return False, output


# Run fast downward planner
def fd_planner(plan_f, sas_f, domain_f, problem_f, planner, path):
    cmd = f'"python" "{path}" --alias "{planner}" --search-time-limit 1000 --plan-file "{plan_f}" --sas-file "{sas_f}" "{domain_f}" "{problem_f}"'
    start_time = time.time()
    output = subprocess.getoutput(cmd)
    end_time = time.time()
    planning_time = end_time - start_time

    plan = ""
    success = False

    if "Solution found." in output:
        success = True
        # Add planning time as a comment to the end of the plan file
        if os.path.exists(plan_f):
            with open(plan_f, "a") as f:
                f.write(f"\n; Planning time: {planning_time} seconds")
            with open(plan_f, "r") as f:
                plan = f.read()

    if os.path.exists(plan_f):
        # Add planning time as a comment to the end of the plan file
        with open(plan_f, "a") as f:
            f.write(f"\n; Planning time: {planning_time} seconds")
        with open(plan_f, "r") as f:
            plan = f.read()

    return success, plan, output, planning_time
