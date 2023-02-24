from functools import lru_cache
from statistics import mean, stdev, variance
from typing import List

# MICE
from ..fe_types import FlowID, Pkts, FeatureVal
from ..BaseFeatures.Directions import Directions
from ..BaseFeatures.WindowFeature import WindowFeature
from ..BaseFeatures.random_round import random_round
from .summary import summary
from ..BaseFeatures.Entropies import Entropy
from .topN import topN
from .hist import hist


class BurstDepths(WindowFeature):
    """
    A per-packet count of how many "packet deep" they are into a burst
    a.k.a since the last reverse packet, how many packets in this direction have come before this packet
    """

    @staticmethod
    @lru_cache(maxsize=128)
    def get_value(fid: FlowID, pkts: Pkts, win_size: int) -> List[FeatureVal]:
        since_fwd = 0
        since_bwd = 0
        burst_depths: List[int] = [0.0] * win_size
        directions = Directions.get_value(fid, pkts, win_size)
        for idx, direction in enumerate(directions):
            if direction > 0:
                burst_depths[idx] = since_bwd
                since_bwd -= 1
                since_fwd = 0
            elif direction < 0:
                burst_depths[idx] = since_fwd
                since_fwd += 1
                since_bwd = 0

        return burst_depths

    @staticmethod
    @lru_cache(maxsize=128)
    def get_names(win_size: int) -> List[str]:
        return [f"p{idx}_BurstDepth" for idx in range(win_size)]

    @staticmethod
    @lru_cache(maxsize=128)
    def min(winsize: int) -> List[FeatureVal]:
        return [0.0] * winsize

    @staticmethod
    @lru_cache(maxsize=128)
    def max(winsize: int) -> List[FeatureVal]:
        # if pkts.data[0].haslayer(scapy.layers.inet.TCP):  # Always need a SYN, SYN-ACK
        #     return [0.0, 0.0] + list(range(winsize - 2))
        # else:
        return list(range(winsize))

    @staticmethod
    def clip(win_size: int) -> float:
        return [random_round] * win_size


MaxBurstdepths = summary(BurstDepths, max)
MinBurstdepths = summary(BurstDepths, min)
SumBurstdepths = summary(BurstDepths, sum)
MeanBurstdepths = summary(BurstDepths, mean)
StdevBurstdepths = summary(BurstDepths, stdev)
VarianceBurstdepths = summary(BurstDepths, variance)
EntropyBurstdepths = summary(BurstDepths, Entropy.entropy)
TopBurstDepths = topN(BurstDepths, 5)
HistBurstdepths = hist(BurstDepths, list(range(0, 10, 1)))
