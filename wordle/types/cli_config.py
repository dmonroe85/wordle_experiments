from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class CliConfig:
    n_trials_per_answer: int
    n_answers_to_test: Optional[int]
    parallelism: int
    dry_run: bool
    max_guesses:int
    batch_size: int
    strategy_names: List[str]