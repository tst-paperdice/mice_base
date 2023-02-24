from abc import ABC, abstractmethod
from functools import lru_cache
from typing import List, Callable, Optional


from ..fe_types import FlowID, Pkts, FeatureVal, WindowID
from .PerPacketFeature import PerPacketFeature


class WindowFeature(ABC):
    @staticmethod
    @abstractmethod
    def min(winsize: int) -> List[float]:
        pass

    @staticmethod
    @abstractmethod
    def max(winsize: int) -> List[float]:
        pass

    @staticmethod
    @abstractmethod
    def get_value(fid: FlowID, pkts: Pkts, win_size: int) -> List[float]:
        pass

    @staticmethod
    @abstractmethod
    def get_names(win_size: int) -> List[str]:
        pass

    @staticmethod
    def clip(win_size: int) -> List[Callable]:
        pass


def windowize(feature: PerPacketFeature):
    class WindowizedFeature(WindowFeature):
        @staticmethod
        @lru_cache(maxsize=128)
        def min(winsize: int) -> List[FeatureVal]:
            return [feature.min() for idx in range(winsize)]

        @staticmethod
        @lru_cache(maxsize=128)
        def max(winsize: int) -> List[FeatureVal]:
            return [feature.max() for idx in range(winsize)]

        @staticmethod
        @lru_cache(maxsize=128)
        def get_value(fid: Optional[FlowID], pkts: Pkts, win_size: int) -> List[float]:
            data = [0.0] * win_size
            for idx, pkt in enumerate(pkts.data):
                data[idx] = feature.get_value(fid, pkt)
            return data

        @staticmethod
        @lru_cache(maxsize=128)
        def get_names(win_size: int) -> List[str]:
            return [f"p{idx}_{feature.name}" for idx in range(win_size)]

        @staticmethod
        def clip(win_size: int) -> List[Callable]:
            return [feature.clip] * win_size

    return WindowizedFeature


def dewindow_name(feature_name: str) -> str:
    return "_".join(feature_name.split("_")[1:])


def window_name(window_id: WindowID, feature_name: str) -> str:
    return f"{window_id}_{feature_name}"
