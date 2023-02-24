from functools import lru_cache
from statistics import mean, stdev, variance
from typing import List

# MICE
from ..fe_types import FlowID, Pkts, FeatureVal
from ..BaseFeatures.Directions import Directions
from ..BaseFeatures.WindowFeature import WindowFeature
from .summary import summary
from ..BaseFeatures.Entropies import Entropy
from .topN import topN
from .hist import hist
from ..BaseFeatures.Sizes import Size, Sizes
from .DirSignSizes import DirSignSizes
from .summary import SumSizes
from ..BaseFeatures.random_round import random_round


class TotalBwdBytes(WindowFeature):
    @staticmethod
    @lru_cache(maxsize=128)
    def get_value(fid: FlowID, pkts: Pkts, win_size: int) -> List[FeatureVal]:
        return [
            sum(
                [-val for val in DirSignSizes.get_value(fid, pkts, win_size) if val < 0]
            )
        ]

    @staticmethod
    @lru_cache(maxsize=128)
    def get_names(win_size: int) -> List[str]:
        return [f"TotalBwdBytes"]

    @staticmethod
    @lru_cache(maxsize=128)
    def min(winsize: int) -> List[FeatureVal]:
        return [0.0]

    @staticmethod
    @lru_cache(maxsize=128)
    def max(winsize: int) -> List[FeatureVal]:
        return SumSizes.max(winsize)

    @staticmethod
    def clip(win_size: int) -> float:
        return [random_round]
