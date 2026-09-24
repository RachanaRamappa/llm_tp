# Commands to set up environment and run all planners for the llm_tp project

# 1. Create the Conda environment (choose appropriate yaml for OS)
conda env create -f environment_mac.yml   # macOS
# conda env create -f environment.yml    # Linux

# 2. Activate the environment
conda activate llm_tp

# 3. Build Fast‑Downward (run once)
# git clone https://github.com/aibasel/downward.git
# cd downward && ./build.py -j$(nproc) && cd ..
# Export the path to fast‑downward so the scripts can find it
export FD_PATH="$(pwd)/downward/fast-downward.py"

# 4. Run the Fast‑Downward baseline
python scripts/run_fd.py \
    --domain barman \
    --planner seq-opt-fdss-1 \
    --sizes 2 3 4 5 6 7 8 9 10 \
    --path "$FD_PATH"

# 5. Run the Symbolic‑LLM planner
python scripts/run_subgoal.py \
    --model gpt-4o \
    --domain barman \
    --subgoal_planner symbolic-llm \
    --temperature 0.0 \
    --planner seq-opt-fdss-1 \
    --sizes 2 3 4 5 6 7 8 9 10 \
    --path "$FD_PATH"

# 6. Run the MCTS‑LLM planner (sample n_s candidate plans)
python scripts/run_subgoal.py \
    --model gpt-4o \
    --domain barman \
    --subgoal_planner mcts-llm \
    --temperature 0.0 \
    --ns 1 2 3 \
    --sizes 2 3 4 5 6 7 8 9 10

# 7. (Optional) Run the Chain‑of‑Thought baseline
python scripts/run_llm.py \
    --model gpt-4o \
    --domain barman \
    --temperature 0.0 \
    --sizes 2 3 4 5 6 7 8 9 10

# 8. (Optional) Validate a specific plan manually
# python scripts/validate_plans.py \
#    --domain barman \
#    --problem_file experiments/barman/problem/barman5_1.pddl \
#    --plan_file experiments/barman/plan/symbolic-llm/barman5_1.pddl

# 9. (Optional) Re‑plan on a failed plan
# python scripts/replanning.py \
#    --domain barman \
#    --failed_plan experiments/barman/plan/mcts-llm/barman5_1_N1.pddl \
#    --model gpt-4o \
#    --temperature 0.0

