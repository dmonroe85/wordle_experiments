import random
from typing import Callable, Iterable, List, Optional, Type

from .game import run_game
from ..util import load_answers, load_non_answers
from ..types import Strategy, Stats, Word


def runner(
    strategy: Strategy,
    answer: Word,
    max_guesses: int,
) -> Callable[[], Stats]:
    def run() -> Stats:
        game_stats = run_game(strategy, answer, max_guesses)
        return game_stats

    return run


def batch_runner(runners: List[Callable[[], Stats]]) -> Callable[[], Stats]:
    def run() -> Stats:
        stats = Stats()
        for runner in runners:
            run_stats = runner()
            stats.merge(run_stats)
        return stats
    return run


def build_batch_runs(
    strategy_classes: List[Type[Strategy]],
    n_iterations: int,
    n_answers_to_test: Optional[int],
    max_guesses: int,
    batch_size: int,
) -> Iterable[Callable[[], Stats]]:
    answer_list = load_answers()
    non_answers = load_non_answers()
    full_wordlist = answer_list + non_answers

    n_answers = n_answers_to_test or len(answer_list)
    answers_to_test = random.choices(answer_list, k=n_answers)

    batch = []
    for idx, answer in enumerate(answers_to_test):
        print(f"Answer={answer.text}, #{idx}")
        for _ in range(n_iterations):
            random.shuffle(full_wordlist)
            for strategy_class in strategy_classes:
                strategy = strategy_class(full_wordlist)
                batch.append(runner(strategy, answer, max_guesses))
                if len(batch) == batch_size:
                    yield batch_runner(batch)
                    batch = []
    yield batch_runner(batch)
