# Strategy implementations
from .strategy_filter_on_feedback import StrategyFilterOnFeedback
from .strategy_matched_feedback import StrategyMatchedFeedback
from .strategy_random_with_replacement import StrategyRandomWithReplacement
from .strategy_random_without_replacement import StrategyRandomWithoutReplacement

# Strategy collections
ALL_STRATEGIES = [
    StrategyRandomWithReplacement,
    StrategyRandomWithoutReplacement,
    StrategyFilterOnFeedback,
    StrategyMatchedFeedback,
]

ALL_STRATEGY_NAMES = [s.__name__ for s in ALL_STRATEGIES]

STRATEGY_LOOKUP = dict(zip(ALL_STRATEGY_NAMES, ALL_STRATEGIES))
