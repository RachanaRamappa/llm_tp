import os
import sys
import re
from pathlib import Path

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from scripts import symbolic as sym


def find_problem_file(domain, size, idx):
    candidates = [
        os.path.join(BASE_DIR, f"experiments/{domain}/problem/{domain}{size}_{idx}.pddl"),
        os.path.join(BASE_DIR, f"experiments/{domain}/problem/{domain}_{size}_{idx}.pddl"),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


def validate_all_plans():
    domains = ["blocksworld", "gripper", "barman"]
    planners = ["seq-opt-fdss-1", "symbolic-llm", "mcts-llm"]

    records = []

    print("=" * 80)
    print("           COMPREHENSIVE PDDL PLAN VALIDATION (VAL)")
    print("=" * 80)

    for domain in domains:
        domain_f = os.path.join(BASE_DIR, f"domains/domain_{domain}.pddl")
        if not os.path.isfile(domain_f):
            print(f"Domain file not found: {domain_f}")
            continue

        for planner in planners:
            plan_dir = os.path.join(BASE_DIR, f"experiments/{domain}/plan/{planner}")
            if not os.path.isdir(plan_dir):
                continue

            for fname in sorted(os.listdir(plan_dir)):
                if not (fname.endswith(".pddl") or fname.endswith(".plan")):
                    continue
                if fname.endswith(".sas") or fname.endswith(".txt") or fname.endswith(".png"):
                    continue

                plan_f = os.path.join(plan_dir, fname)
                if not os.path.isfile(plan_f) or os.path.getsize(plan_f) == 0:
                    continue

                # Filter out intermediate subgoal slices like blocksworld3_1_0.pddl or barman2_1_1.pddl
                if re.search(r"_\d+_\d+\.pddl$", fname):
                    continue

                m = re.match(rf"^{domain}(\d+)_(\d+)(_N\d+)?\.(pddl|plan)$", fname)
                if not m:
                    # Also check test files or other formats
                    m2 = re.match(r".*?(\d+)_(\d+).*", fname)
                    if not m2:
                        continue
                    size = int(m2.group(1))
                    idx = int(m2.group(2))
                else:
                    size = int(m.group(1))
                    idx = int(m.group(2))

                problem_f = find_problem_file(domain, size, idx)
                if not problem_f:
                    continue

                # Run VAL validator
                valid, output = sym.validate(domain_f, problem_f, plan_f)

                # Extract plan steps count
                steps = 0
                step_match = re.search(r"Plan size:\s*(\d+)", output)
                if step_match:
                    steps = int(step_match.group(1))
                else:
                    # Count non-empty non-comment lines
                    with open(plan_f, "r") as pf:
                        lines = [l.strip() for l in pf if l.strip() and not l.strip().startswith(";")]
                        steps = len(lines)

                status_str = "VALID" if valid else "INVALID"
                records.append({
                    "domain": domain,
                    "planner": planner,
                    "size": size,
                    "index": idx,
                    "file": fname,
                    "steps": steps,
                    "valid": valid,
                    "output_snippet": output.strip().splitlines()[-1] if output.strip() else ""
                })

                print(f"[{domain.upper():11s}] [{planner:15s}] Size {size:2d} ({fname}): {status_str} ({steps} steps)")

    print("=" * 80)
    print()

    # Generate Markdown Table Summary
    summary_md_path = os.path.join(BASE_DIR, "experiments/validation_matrix.md")
    with open(summary_md_path, "w") as md:
        md.write("# Comprehensive Plan Validation Matrix\n\n")
        md.write("Generated using the official PDDL plan validator **VAL** (`Validate`).\n\n")
        md.write("| Domain | Planner | Problem Size | Plan File | Action Steps | VAL Status |\n")
        md.write("| :--- | :--- | :---: | :--- | :---: | :---: |\n")

        for r in records:
            status_badge = "✅ VALID" if r["valid"] else "❌ INVALID"
            md.write(f"| **{r['domain'].capitalize()}** | `{r['planner']}` | Size {r['size']} | `{r['file']}` | {r['steps']} | {status_badge} |\n")

    print(f"Validation matrix saved to: {summary_md_path}")
    return records


if __name__ == "__main__":
    validate_all_plans()
