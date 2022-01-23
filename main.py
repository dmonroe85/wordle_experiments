from typing import List, Optional

import typer

from wordle.app import run
from wordle.strategies import ALL_STRATEGY_NAMES


def main(
    n_trials: int = 10,
    n_answers: Optional[int] = None,
    parallelism: int = -1,
    strategies: Optional[List[str]] = None,
    dry_run: bool = False,
):
    strategies_to_run = strategies or ALL_STRATEGY_NAMES
    run(n_trials, n_answers, parallelism, strategies_to_run, dry_run)


if __name__ == "__main__":
    typer.run(main)
