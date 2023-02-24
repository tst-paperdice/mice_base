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


class DirSignBurstBytes(WindowFeature):
    @staticmethod
    @lru_cache(maxsize=128)
    def get_value(fid: FlowID, pkts: Pkts, win_size: int) -> List[FeatureVal]:
        burst_bytes = [0.0] * win_size
        directions = Directions.get_value(fid, pkts, win_size)
        sizes = Sizes.get_value(fid, pkts, win_size)

        cur_dir = 0
        cur_sum = 0
        burst_count = 0
        for idx, direction in enumerate(directions):
            if direction == cur_dir:
                cur_sum += sizes[idx]
            else:
                if cur_dir != 0:
                    burst_bytes[burst_count] = cur_dir * cur_sum
                    burst_count += 1

                cur_sum = sizes[idx]
                cur_dir = direction

        return burst_bytes

    @staticmethod
    @lru_cache(maxsize=128)
    def get_names(win_size: int) -> List[str]:
        return [f"b{idx}_DirSignBurstBytes" for idx in range(win_size)]

    @staticmethod
    @lru_cache(maxsize=128)
    def min(winsize: int) -> List[FeatureVal]:
        return [-1 * idx * Size.max() for idx in range(winsize)]

    @staticmethod
    @lru_cache(maxsize=128)
    def max(winsize: int) -> List[FeatureVal]:
        # if pkts.data[0].haslayer(scapy.layers.inet.TCP):  # Always need a SYN, SYN-ACK
        #     return [0.0, 0.0] + [idx * Size.max() for idx in range(winsize - 2)]
        # else:
        return [idx * Size.max() for idx in range(winsize)]

    @staticmethod
    def clip(win_size: int) -> float:
        return Sizes.clip(win_size)


MaxDirSignBurstBytes = summary(DirSignBurstBytes, max)
MinDirSignBurstBytes = summary(DirSignBurstBytes, min)
SumDirSignBurstBytes = summary(DirSignBurstBytes, sum)
MeanDirSignBurstBytes = summary(DirSignBurstBytes, mean)
StdevDirSignBurstBytes = summary(DirSignBurstBytes, stdev)

VarianceDirSignBurstBytes = summary(DirSignBurstBytes, variance)
EntropyDirSignBurstBytes = summary(DirSignBurstBytes, Entropy.entropy)
TopDirSignBurstBytes = topN(DirSignBurstBytes, 5)
HistDirSignBurstBytes = hist(DirSignBurstBytes, list(range(-10_000, 10_000, 2_000)))
