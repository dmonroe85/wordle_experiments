import random
from typing import Callable, Iterable, List, Type

from .game import run_game
from ..util import load_answers, load_non_answers
from .types import Strategy, Stats, Word


def build_runners(
    strategy_classes: List[Type[Strategy]],
    n_iterations: int,
    n_answers_to_test: Optional[int],
) -> Iterable[Callable[[], Stats]]:
    answer_list = load_answers()
    non_answers = load_non_answers()
    full_wordlist = answer_list + non_answers

    n_answers = n_answers_to_test or len(answer_list)
    answers_to_test = random.choices(answer_list, k=n_answers)

    for answer in answers_to_test:
        print(answer)
        for _ in range(n_iterations):
            for strategy_class in strategy_classes:
                strategy = strategy_class(full_wordlist)
                yield runner(strategy, answer)


def runner(strategy: Strategy, answer: Word) -> Callable[[], Stats]:
    def run() -> Stats:
        game_stats = run_game(strategy, answer)
        return game_stats

    return run
