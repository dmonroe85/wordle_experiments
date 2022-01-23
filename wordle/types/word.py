from collections import Counter
from dataclasses import dataclass


@dataclass
class Word:
    text: str

    def __post_init__(self):
        self.char_counts = Counter(self.text)

