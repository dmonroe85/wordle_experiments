# Strategy implementations
from .strategy_filter_on_feedback import StrategyFilterOnFeedback
from .strategy_matched_feedback import StrategyMatchedFeedback
from .strategy_random_with_replacement import StrategyRandomWithReplacement
from .strategy_random_without_replacement import StrategyRandomWithoutReplacement
from .strategy_max_character_frequency import StrategyMaxCharacterFrequency
from .strategy_minmax_feedback_matches import (
    StrategyMinMaxFeedbackMatches,
    StrategyMinMaxFeedbackMatchesV2,
)
from .strategy_max_entropy import StrategyMaxEntropy
from .strategy_smallest_feedback_partition import (
    StrategySmallestFeedbackPartition,
    StrategySmallestFeedbackPartitionV2,
)
from .strategy_first_guess import (
    StrategyFirstGuessAdieu,
    StrategyFirstGuessArise,
    StrategyFirstGuessAudio,
    StrategyFirstGuessBoozy,
    StrategyFirstGuessGypsy,
    StrategyFirstGuessRaise,
    StrategyFirstGuessRoate,
    StrategyFirstGuessSerai,
    StrategyFirstGuessSoare,
)
from .strategy_25_characters import (
    Strategy25Characters0,
    Strategy25Characters1,
    Strategy25Characters2,
    Strategy25Characters3,
    Strategy25Characters4,
)

# Strategy collections
ALL_STRATEGIES = [
    # StrategyMinMaxFeedbackMatchesV2,
    Strategy25Characters0,
    Strategy25Characters1,
    Strategy25Characters2,
    Strategy25Characters3,
    Strategy25Characters4,
    StrategyFilterOnFeedback,
    StrategyFirstGuessAdieu,
    StrategyFirstGuessArise,
    StrategyFirstGuessAudio,
    StrategyFirstGuessBoozy,
    StrategyFirstGuessGypsy,
    StrategyFirstGuessRaise,
    StrategyFirstGuessRoate,
    StrategyFirstGuessSerai,
    StrategyFirstGuessSoare,
    StrategyMatchedFeedback,
    StrategyMaxCharacterFrequency,
    StrategyMaxEntropy,
    StrategyMinMaxFeedbackMatches,
    StrategyRandomWithoutReplacement,
    StrategyRandomWithReplacement,
    StrategySmallestFeedbackPartition,
    StrategySmallestFeedbackPartitionV2,
]

ALL_STRATEGY_NAMES = [s.__name__ for s in ALL_STRATEGIES]

STRATEGY_LOOKUP = dict(zip(ALL_STRATEGY_NAMES, ALL_STRATEGIES))

STRATEGIES_THAT_USE_FEEDBACK_CACHE = [
    StrategyMinMaxFeedbackMatches,
    StrategyMinMaxFeedbackMatchesV2,
]

STRATEGIES_THAT_USE_ORDERED_CACHE = [
    StrategySmallestFeedbackPartition,
    StrategySmallestFeedbackPartitionV2,
    Strategy25Characters0,
    Strategy25Characters1,
    Strategy25Characters2,
    Strategy25Characters3,
    Strategy25Characters4,
]
