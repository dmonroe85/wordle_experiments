from functools import reduce
import json

from joblib import Parallel, delayed

from wordle.simulator import build_runners, Stats
from wordle.strategies import *

n_iterations_per_word = 10
strategies = [
    StrategyRandomWithReplacement,
    StrategyRandomWithoutReplacement,
    StrategyFilterOnFeedback,
]

if __name__ == '__main__':
    print(f"Running {len(strategies)} strategies, {n_iterations_per_word} trials on each word.")
    stats_list = Parallel(n_jobs=-1)(delayed(run)()for run in build_runners(strategies, n_iterations_per_word))
    
    print(f"Merging {len(stats_list)} results together")
    stats = reduce(
        lambda s1, s2: s1.merge(s2),
        stats_list
    )
    
    print("Writing output")
    with open("results.json", "w") as ostream:
        json.dump(stats.dict(), ostream)
