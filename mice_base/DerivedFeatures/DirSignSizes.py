from functools import lru_cache
from typing import List, Callable

# MICE
from ..BaseFeatures.Sizes import Size, Sizes
from ..BaseFeatures.Directions import Directions
from ..BaseFeatures.WindowFeature import WindowFeature
from ..fe_types import FlowID, Pkts


class DirSignSizes(WindowFeature):
    @staticmethod
    @lru_cache(maxsize=128)
    def min(winsize: int) -> List[float]:
        dirs = Directions.min(winsize)
        sizes = Sizes.max(winsize)
        return [dirs[idx] * sizes[idx] for idx in range(winsize)]

    @staticmethod
    @lru_cache(maxsize=128)
    def max(winsize: int) -> List[float]:
        dirs = Directions.max(winsize)
        sizes = Sizes.max(winsize)
        return [dirs[idx] * sizes[idx] for idx in range(winsize)]

    @staticmethod
    @lru_cache(maxsize=128)
    def get_value(fid: FlowID, pkts: Pkts, win_size: int) -> List[float]:
        data = [0.0] * win_size
        dirs = Directions.get_value(fid, pkts, win_size)
        sizes = Sizes.get_value(fid, pkts, win_size)
        for idx, _ in enumerate(pkts.data):
            data[idx] = dirs[idx] * sizes[idx]
        return data

    @staticmethod
    @lru_cache(maxsize=128)
    def get_names(win_size: int) -> List[str]:
        return [f"p{idx}_DirSignSize" for idx in range(win_size)]

    @staticmethod
    def clip(win_size: int) -> List[Callable]:
        return [Size.clip] * win_size
