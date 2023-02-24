from functools import lru_cache
import math
from typing import List, Optional

# MICE
from ..fe_types import FlowID, Pkts, FeatureVal
from ..BaseFeatures.WindowFeature import WindowFeature
from ..BaseFeatures.random_round import random_round
from ..BaseFeatures.Sizes import Sizes, Size
from ..BaseFeatures.Entropies import Entropies


def hist(feature, buckets):
    class Hist(WindowFeature):
        @staticmethod
        @lru_cache(maxsize=128)
        def min(winsize: int) -> List[FeatureVal]:
            return [0.0] * len(buckets)

        @staticmethod
        @lru_cache(maxsize=128)
        def max(winsize: int) -> List[FeatureVal]:
            return [winsize] * len(buckets)

        @staticmethod
        @lru_cache(maxsize=128)
        def get_value(fid: Optional[FlowID], pkts: Pkts, win_size: int) -> List[float]:
            results = [0.0] * len(buckets)
            data = sorted(feature.get_value(fid, pkts, win_size))
            keys = buckets + [math.inf]
            cur_idx = 0
            upper_idx = keys[cur_idx + 1]
            for val in data:
                while val > upper_idx and cur_idx < len(keys) - 2:
                    cur_idx += 1
                    upper_idx = keys[cur_idx + 1]

                results[cur_idx] += 1

            return results

        @staticmethod
        @lru_cache(maxsize=128)
        def get_names(win_size: int) -> List[str]:
            return [
                f"Hist{feature.get_names(win_size)[0][3:]}{bucket}"
                for bucket in buckets
            ]

        @staticmethod
        def clip(win_size: int) -> float:
            return [random_round] * len(buckets)

    return Hist


k = 5
HistSizes = hist(Sizes, list(range(0, Size.max(), k)))
HistEntropies = hist(Entropies, list(range(0, 8, 1)))
