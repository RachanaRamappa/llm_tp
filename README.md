# Fast and Accurate Task Planning using Neuro-Symbolic Language Models and Multi-level Goal Decomposition

This repository is the implementation of our paper [Fast and Accurate Task Planning using Neuro-Symbolic Language Models and Multi-level Goal Decomposition](https://arxiv.org/abs/2409.19250), _IEEE International Conference on Robotics and Automation (ICRA) 2025_.

Look into our [project website](http://graphics.ewha.ac.kr/LLMTAMP/) for more details.


## Setup

###  Install PDDL Planner & Validator
- First, install the [Fast Downward](https://github.com/aibasel/downward) planner with the following [instructions](https://github.com/aibasel/downward/blob/main/BUILD.md).

- Then install the PDDL validator [VAL](https://github.com/KCL-Planning/VAL) with the following [instructions](https://github.com/aibasel/downward/blob/main/BUILD.md#optional-plan-validator).

### Install Our Project
1. Git clone our project
    ```
    git clone https://github.com/Minseo10/llm_tp.git
    cd llm_tp
    ```

2. Create a conda environment
    ```
    conda env create -f environment.yml
    conda activate llm_tp
    ```

3. Put OpenAI Key inside config.json
    ```
    "OPENAI_API_KEY": "YOUR_OPENAI_KEY"
    ```


## Usage
The python scripts for experiments are located in the `scripts` directory.
```
cd scripts
```

### Running our planner
To run the **MCTS LLM** planner,
```
python run_subgoal.py --model "gpt-4o" --domain "barman" --subgoal_planner "mcts-llm" --temperature 0.0 --ns 3 4 5 --sizes 2 3 4 5 6 7 8 9 10
```

To run the **Symbolic LLM** planner,
```
 python run_subgoal.py --model "gpt-4o" --domain "barman" --subgoal_planner "symbolic-llm" --temperature 0.0 --planner "seq-opt-fdss-1"  --sizes 2 3 4 5 6 7 8 9 10 --path "path_to_downward"
```


### Running baselines
To run the **Fast Downward** planner,
```
python run_fd.py --domain "barman" --planner "seq-opt-fdss-1" --sizes 2 3 4 5 6 7 8 9 10 --path "path_to_downward"
```

To run the **Chain-of-Thought** planner,
```
python run_llm.py --model "gpt-4o" --domain "barman" --temperature 0.0 --sizes 2 3 4 5 6 7 8 9 10
```

### Parameter Explanation
- `model`: Name of GPT model. Default to "gpt-4o".
- `domain`: PDDL domain name. Choose among "barman", "blocksworld", "gripper".
- `subgoal_planner`: Choose your subgoal planner between "symbolic-llm" and "mcts-llm".
- `temperature`: Temperature of the LLM. Default to 0.0.
- `planner`: Fast Downward planner configuration. Choose between "seq-opt-fdss-1" and "seq-sat-lama-2011".
- `ns`: Number of sampled plans $n_s$ by LLM when using the MCTS LLM as subgoal planner.
- `sizes`: Problem sizes to test. Defined by the number of objects in each problem PDDL. For barman and gripper, you can test between 2 to 10, and for blocksworld, you can test between 3 to 10.
- `path`: Represents path to `fast-downward.py` in your project. For example, `--path "/home/user/downward/fast-downward.py"`.


## Contact
Please contact 'minseo.kwon@ewha.ac.kr' if you have any questions.



## Citation


IEEE ICRA 2025, [Fast and Accurate Task Planning using Neuro-Symbolic Language Models and Multi-level Goal Decomposition](https://arxiv.org/abs/2409.19250)
```
@article{kwon2024fast,
  title={Fast and accurate task planning using neuro-symbolic language models and multi-level goal decomposition},
  author={Kwon, Minseo and Kim, Yaesol and Kim, Young J},
  journal={arXiv preprint arXiv:2409.19250},
  year={2024}
}
```