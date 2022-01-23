from functools import reduce
import json
from typing import List, Optional

from joblib import Parallel, delayed

from wordle.simulator import build_runners
from wordle.strategies import STRATEGY_LOOKUP
from wordle.types import Stats

RESULTS_DIR = "results"

def run(
    n_trials_per_answer: int,
    n_answers_to_test: Optional[int],
    parallelism: int,
    strategy_names: List[str],
    dry_run: bool,
):
    strategies_to_run = [STRATEGY_LOOKUP[s] for s in strategy_names]
    
    print(
        f"Running {len(strategies_to_run)} strategies, {n_trials_per_answer} "
        "trials on each answer word."
    )
    stats_list = Parallel(n_jobs=parallelism)(
        delayed(run)()
        for run in build_runners(
            strategies_to_run,
            n_trials_per_answer,
            n_answers_to_test,
        )
    )
    
    print(f"Merging {len(stats_list)} results together")
    stats = reduce(
        lambda s1, s2: s1.merge(s2),
        stats_list,
    )

    if not dry_run:
        print("Writing outputs")
        for strategy_name, guess_history in stats.dict().items():
            result_path = os.path.join(RESULTS_DIR, f"results-{strategy_name}.json")
            with open(result_path, "w") as ostream:
                json.dump({strategy_name: guess_history}, ostream)

    print("Completed!")
