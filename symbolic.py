import os
import sys
import subprocess
import shutil
import time


def _find_validate_bin():
    validate_bin = shutil.which("Validate") or shutil.which("validate")
    if validate_bin:
        return validate_bin

    # Check local workspace builds
    candidates = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../VAL/build/bin/Validate")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../VAL/build/bin/validate")),
        "/opt/VAL/bin/Validate",
        "/opt/VAL/bin/validate",
    ]
    for c in candidates:
        if os.path.isfile(c) and os.access(c, os.X_OK):
            return c

    return "Validate"


# Run PDDL plan validator VAL
def validate(domain_f, problem_f, plan_f):
    validate_bin = _find_validate_bin()
    cmd = f'"{validate_bin}" -v "{domain_f}" "{problem_f}" "{plan_f}"'
    output = subprocess.getoutput(cmd)

    if "Plan valid" in output:
        return True, output
    else:
        return False, output


# Run Fast Downward planner
def fd_planner(plan_f, sas_f, domain_f, problem_f, planner, path):
    if not path:
        local_fd = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../downward/fast-downward.py"))
        if os.path.isfile(local_fd):
            path = local_fd
        else:
            path = "fast-downward.py"

    cmd = (
        f'"{sys.executable}" "{path}" '
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

