from functools import lru_cache
from typing import List, Callable
from statistics import mean, stdev, variance

# MICE
from ..BaseFeatures.WindowFeature import WindowFeature
from ..fe_types import FlowID, Pkts
from ..BaseFeatures.Directions import Direction
from ..BaseFeatures.random_round import random_round
from .topN import topN
from .hist import hist
from .summary import summary
from ..BaseFeatures.Entropies import Entropy

# TODO: Inter-Arrival Times?
class IATs(WindowFeature):
    @staticmethod
    @lru_cache(maxsize=128)
    def min(winsize: int) -> List[float]:
        return [0.0] * winsize

    @staticmethod
    @lru_cache(maxsize=128)
    def max(winsize: int) -> List[float]:
        return [1.0] * winsize

    @staticmethod
    @lru_cache(maxsize=128)
    def get_value(fid: FlowID, pkts: Pkts, win_size: int) -> List[float]:
        last_fwd = None
        last_bwd = None
        values: List[float] = [0.0] * win_size
        for idx, pkt in enumerate(pkts):
            if Direction.get_value(fid, pkt) > 0:
                if last_fwd is None:
                    last_fwd = pkt.time
                else:
                    new_time = pkt.time
                    values[idx] = new_time - last_fwd
                    last_fwd = new_time
            else:  # Backward
                if last_bwd is None:
                    last_bwd = pkt.time
                else:
                    new_time = pkt.time
                    values[idx] = new_time - last_bwd
                    last_bwd = new_time

        return values

    @staticmethod
    @lru_cache(maxsize=128)
    def get_names(win_size: int) -> List[str]:
        return [f"p{idx}_IAT" for idx in range(win_size)]

    @staticmethod
    def clip(win_size: int) -> float:
        return [random_round] * win_size


MaxIATs = summary(IATs, max)
MinIATs = summary(IATs, min)
SumIATs = summary(IATs, sum)
MeanIATs = summary(IATs, mean)
StdevIATs = summary(IATs, stdev)
VarianceIATs = summary(IATs, variance)
EntropyIATs = summary(IATs, Entropy.entropy)
TopIATs = topN(IATs, 5)
# 10 millisecond windows
HistIATs = hist(IATs, [idx * 0.001 for idx in range(0, 500, 10)])
