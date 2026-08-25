import os
import subprocess
import time


# Run PDDL plan validator VAL
def validate(domain_f, problem_f, plan_f):
    cmd = f'"Validate" -v "{domain_f}" "{problem_f}" "{plan_f}"'
    output = subprocess.getoutput(cmd)

    if "Plan valid" in output:
        return True, output
    else:
        return False, output


# Run Fast Downward planner
def fd_planner(plan_f, sas_f, domain_f, problem_f, planner, path):
    cmd = (
        f'"python" "{path}" '
        f'--alias "{planner}" '
        f'--search-time-limit 1000 '
        f'--plan-file "{plan_f}" '
        f'--sas-file "{sas_f}" '
        f'"{domain_f}" "{problem_f}"'
    )

    start_time = time.time()
    output = subprocess.getoutput(cmd)
    end_time = time.time()

    planning_time = end_time - start_time

    success = "Solution found." in output

    plan = ""

    if os.path.exists(plan_f):
        with open(plan_f, "r") as f:
            plan = f.read()

    return success, plan, output, planning_time

