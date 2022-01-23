from functools import reduce
from pprint import pformat
from typing import List, Optional
import json
import os
import sys
import time

from joblib import Parallel, delayed

from wordle.simulator import build_batch_runs
from wordle.strategies import ALL_STRATEGY_NAMES, STRATEGY_LOOKUP
from wordle.types import CliConfig, Stats

RESULTS_DIR = "results"

def run(conf: CliConfig):
    unsupported_strategies = ','.join([
        s for s in conf.strategy_names if s not in ALL_STRATEGY_NAMES
    ])
    if unsupported_strategies:
        errmsg = (
            "Provided strategies not supported:\n"
            f"{unsupported_strategies}"
            "\n\nPlease select a strategy from the following:\n"
            f"{','.join(ALL_STRATEGY_NAMES)}"
        )
        print(errmsg)
        sys.exit(-1)
    
    strategies_to_run = [STRATEGY_LOOKUP[s] for s in conf.strategy_names]
    
    print(f"Running:\n{pformat(conf)}")
    start_time = time.time()
    stats_list = Parallel(n_jobs=conf.parallelism)(
        delayed(run)()
        for run in build_batch_runs(
            strategies_to_run,
            conf.n_trials_per_answer,
            conf.n_answers_to_test,
            conf.max_guesses,
            conf.batch_size,
        )
    )
    end_time = time.time()
    
    print(f"Merging {len(stats_list)} results together")
    stats = reduce(
        lambda s1, s2: s1.merge(s2),
        stats_list,
    )

    if not conf.dry_run:
        print("Writing outputs")
        os.makedirs(RESULTS_DIR, exist_ok=True)
        for strategy_name, guess_history in stats.dict().items():
            result_path = os.path.join(RESULTS_DIR, f"results-{strategy_name}.json")
            with open(result_path, "w") as ostream:
                json.dump({strategy_name: guess_history}, ostream)

    print(f"Completed in {end_time - start_time} seconds")
