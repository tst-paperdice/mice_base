from functools import lru_cache
from typing import List, Optional

# MICE
from ..fe_types import FlowID, Pkts, FeatureVal
from ..BaseFeatures.WindowFeature import WindowFeature
from ..BaseFeatures.Sizes import Sizes
from ..BaseFeatures.Entropies import Entropy, Entropies


def topN(feature, n=5, bottom=False):
    class TopN(WindowFeature):
        @staticmethod
        def _get_top_n(data):
            if bottom:
                data.sort()
                return data[:n]
            else:
                data.sort()
                return data[-n:]

        @staticmethod
        @lru_cache(maxsize=128)
        def min(winsize: int) -> List[FeatureVal]:
            if bottom:
                return _get_top_n([feature.max() for idx in range(winsize)])
            else:
                return _get_top_n([feature.min() for idx in range(winsize)])

        @staticmethod
        @lru_cache(maxsize=128)
        def max(winsize: int) -> List[FeatureVal]:
            # TODO
            if bottom:
                return _get_top_n([feature.min() for idx in range(winsize)])
            else:
                return _get_top_n([feature.max() for idx in range(winsize)])

        @staticmethod
        @lru_cache(maxsize=128)
        def get_value(fid: Optional[FlowID], pkts: Pkts, win_size: int) -> List[float]:
            result = [0.0] * n
            data = TopN._get_top_n(
                [float(v) for v in feature.get_value(fid, pkts, win_size)]
            )
            for idx, value in enumerate(data):
                result[idx] = value

            return result

        @staticmethod
        @lru_cache(maxsize=128)
        def get_names(win_size: int) -> List[str]:
            return [f"Top{idx}{feature.get_names(win_size)[0][3:]}" for idx in range(n)]

        @staticmethod
        def clip(win_size: int) -> float:
            return [feature.clip] * n

    return TopN


TopSizes = topN(Sizes, 5)
TopEntropies = topN(Entropies, 5)
