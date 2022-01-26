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

# Strategy collections
ALL_STRATEGIES = [
    # StrategyMinMaxFeedbackMatchesV2,
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
]

ALL_STRATEGY_NAMES = [s.__name__ for s in ALL_STRATEGIES]

STRATEGY_LOOKUP = dict(zip(ALL_STRATEGY_NAMES, ALL_STRATEGIES))
