from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterator, List, Dict


@dataclass
class Stats:
    # The data in stats_dict is
    #   {strategy_name: guess_history}
    stats_dict: Dict[str, List[int]] = field(default_factory=lambda: defaultdict(list))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(stats_dict={dict(self.stats_dict)})"

    def add(self, name: str, n_guesses: int):
        self.stats_dict[name].append(n_guesses)

    def add_multiple(self, name: str, n_guesses: List[int]):
        self.stats_dict[name].extend(n_guesses)

    def merge(self, other: "Stats") -> "Stats":
        for strategy_name, guess_history in other.stats_dict.items():
            self.stats_dict[strategy_name] += guess_history
        return self

    def dict(self) -> Dict[str, List[int]]:
        return dict(self.stats_dict)
