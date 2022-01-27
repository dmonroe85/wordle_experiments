from functools import reduce
from pprint import pformat
from typing import List, Optional, Set
import json
import os
import sys
import time

from joblib import Parallel, delayed

from wordle.simulator import build_batch_runs
from wordle.strategies import (
    ALL_STRATEGY_NAMES,
    STRATEGY_LOOKUP,
    STRATEGIES_THAT_USE_FEEDBACK_CACHE,
    STRATEGIES_THAT_USE_ORDERED_CACHE,
)
from wordle.strategies.feedback_lookup_cache import (
    FEEDBACK_CACHE_PATH,
    ORDERED_CACHE_PATH,
)
from wordle.types import CliConfig, Stats

RESULTS_DIR = "results"


def check_cached_strategies(
    conf: CliConfig,
    cache_strategies: List[str],
    cache_path: str,
) -> Set[str]:
    missing_strategies = set()
    for strategy in cache_strategies:
        strat_name = strategy.__name__
        strat_requested = strat_name in conf.strategy_names
        cache_exists = os.path.isdir(cache_path)
        if strat_requested and not cache_exists:
            missing_strategies.add(strat_name)
    return missing_strategies


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

    flc_missing_strategies = check_cached_strategies(
        conf, STRATEGIES_THAT_USE_FEEDBACK_CACHE, FEEDBACK_CACHE_PATH
    )
    olc_missing_strategies = check_cached_strategies(
        conf, STRATEGIES_THAT_USE_ORDERED_CACHE, ORDERED_CACHE_PATH
    )

    if flc_missing_strategies:
        print(
            "The following strategies require precomputing the feedback cache:"
        )
        print('\n'.join(sorted(flc_missing_strategies)))
        print(
            "In order to use these strategies, please run:\n"
            "  python -m wordle.scripts.precompute_matching_feedback\n"
        )
    if olc_missing_strategies:
        print(
            "The following strategies require precomputing the ordered cache:"
        )
        print('\n'.join(sorted(olc_missing_strategies)))
        print(
            "In order to use these strategies, please run:\n"
            "  python -m wordle.scripts.partition_ordered_feedback\n"
        )
    if flc_missing_strategies or olc_missing_strategies:
        print("Will resume in just a moment...")
        time.sleep(5)

    
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
