from functools import lru_cache
from statistics import mean, stdev, variance
from typing import List, Optional

# MICE
from ..BaseFeatures.WindowFeature import WindowFeature
from ..fe_types import FlowID, FeatureVal, Pkts
from ..BaseFeatures.Sizes import Sizes
from ..BaseFeatures.Entropies import Entropy, Entropies


def summary(feature, func, max=0.0):
    class Summary(WindowFeature):
        @staticmethod
        @lru_cache(maxsize=128)
        def min(winsize: int) -> List[FeatureVal]:
            return [0.0]

        @staticmethod
        @lru_cache(maxsize=128)
        def max(winsize: int) -> List[FeatureVal]:
            return [max]

        @staticmethod
        @lru_cache(maxsize=128)
        def get_value(fid: Optional[FlowID], pkts: Pkts, win_size: int) -> List[float]:
            try:
                return [func([float(v) for v in feature.get_value(fid, pkts)])]
            except:
                return [0.0]

        @staticmethod
        @lru_cache(maxsize=128)
        def get_names(win_size: int) -> List[str]:
            return [f"{func.__name__.capitalize()}{feature.get_names(win_size)[0][3:]}"]

        @staticmethod
        def clip(win_size: int) -> float:
            return [lambda x: x]

    return Summary


# Summarized features
MaxSizes = summary(Sizes, max)
MinSizes = summary(Sizes, min)
SumSizes = summary(Sizes, sum)
MeanSizes = summary(Sizes, mean)
StdevSizes = summary(Sizes, stdev)
VarianceSizes = summary(Sizes, variance)
EntropySizes = summary(Sizes, Entropy.entropy)
MaxEntropies = summary(Entropies, max)
MinEntropies = summary(Entropies, min)
SumEntropies = summary(Entropies, sum)
MeanEntropies = summary(Entropies, mean)
StdevEntropies = summary(Entropies, stdev)
VarianceEntropies = summary(Entropies, variance)
EntropyEntropies = summary(Entropies, Entropy.entropy)
