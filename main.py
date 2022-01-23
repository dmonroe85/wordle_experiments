from typing import List, Optional

import typer

from wordle.app import run
from wordle.strategies import ALL_STRATEGY_NAMES
from wordle.types import CliConfig


def main(
    n_trials: int = 4,
    n_answers: Optional[int] = None,
    parallelism: int = -1,
    dry_run: bool = False,
    max_guesses: int = 6,
    batch_size: int = 10,
    strategy: Optional[List[str]] = None,
):
    conf = CliConfig(
        n_trials_per_answer=n_trials,
        n_answers_to_test=n_answers,
        parallelism=parallelism,
        dry_run=dry_run,
        max_guesses=max_guesses,
        batch_size=batch_size,
        strategy_names=strategy or ALL_STRATEGY_NAMES,
    )
    run(conf)


if __name__ == "__main__":
    typer.run(main)
