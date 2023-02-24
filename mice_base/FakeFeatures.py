"""
  Module to hold definitions for features, their constraints, and interdependencies

  These classes are NOT meant to create objects for each feature value
"""
import itertools as it
import math
from abc import ABC, abstractmethod
from collections import Counter
from functools import lru_cache
from random import random
from statistics import mean, stdev, variance

import numpy as np
import scapy.layers.inet
from scipy.stats import entropy

import BaseFeatures.Size
from base.ScaleParams import ScaleParams
from fe_types import *


def binary_entropy(bytelist) -> float:
    return entropy(list(Counter(bytelist).values()), base=2)

def random_round(val: float) -> int:
    return math.floor(val + random())

class DataType(Enum):
    DIRS = 1
    SIZES = 2
    ENTROPIES = 3
    
class BaseData(NamedTuple):
    """Triple list of directions, sizes, and entropies.
    """
    directions: List[int]
    sizes: List[int]
    entropies: List[float]

    def to_array(self):
        return np.array(list(it.chain(*self)))

    def scale(self, scaler: ScaleParams):
        scaled = scaler.scale(self.to_array())
        divisions = len(scaled) // 3
        return BaseData(
            scaled[0:divisions].tolist(),
            scaled[divisions : 2 * divisions].tolist(),
            scaled[2 * divisions :].tolist(),
        )
    
    def descale(self, scaler: ScaleParams):
        descaled = scaler.descale(self.to_array())
        divisions = len(descaled) // 3
        return BaseData(
            descaled[0:divisions].tolist(),
            descaled[divisions : 2 * divisions].tolist(),
            descaled[2 * divisions :].tolist(),
        )

    @classmethod
    def from_array(cls, arr):
        divisions = len(arr) // 3
        return BaseData(
            arr[0:divisions].tolist(),
            arr[divisions : 2 * divisions].tolist(),
            arr[2 * divisions :].tolist(),
        )
    
class FakeWindowFeature(ABC):
    @staticmethod
    @abstractmethod
    def get_value(data: BaseData) -> List[float]:
        pass

    @staticmethod
    @abstractmethod
    def get_names(win_size: int) -> List[str]:
        pass
    
def windowize(name, dataType: DataType):
    class WindowizedFeature(FakeWindowFeature):
        @staticmethod
        def get_value(data: BaseData) -> List[float]:
            if dataType == DataType.DIRS:
                return data.directions
            elif dataType == DataType.SIZES:
                return data.sizes
            elif dataType == DataType.ENTROPIES:
                return data.entropies
            else:
                raise NotImplementedError()
            
        @staticmethod
        def get_names(win_size: int) -> List[str]:
            return [f"p{idx}_{name}" for idx in range(win_size)]

    return WindowizedFeature
        
Directions = windowize("Direction", DataType.DIRS)
Sizes = windowize("Size", DataType.SIZES)
Entropies = windowize("Entropy", DataType.ENTROPIES)



class DirSignBurstBytes(FakeWindowFeature):
    @staticmethod
    def get_value(data: BaseData) -> List[float]:
        directions = Directions.get_value(data)
        burst_bytes = [0.0] * len(directions)
        sizes = Sizes.get_value(data)

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
    def get_names(win_size: int) -> List[str]:
        return [f"b{idx}_DirSignBurstBytes" for idx in range(win_size)]


class TotalFwdBytes(FakeWindowFeature):
    @staticmethod
    def get_value(data: BaseData) -> List[float]:
        return [
            sum([val for val in DirSignSizes.get_value(data) if val > 0])
        ]

    @staticmethod
    def get_names(win_size: int) -> List[str]:
        return [f"TotalFwdBytes"]


class TotalBwdBytes(FakeWindowFeature):
    @staticmethod
    def get_value(data: BaseData) -> List[float]:
        return [
            sum(
                [-val for val in DirSignSizes.get_value(data) if val < 0]
            )
        ]

    @staticmethod
    def get_names(win_size: int) -> List[str]:
        return [f"TotalBwdBytes"]





def hist(feature, buckets):
    class Hist(FakeWindowFeature):
        @staticmethod
        def get_value(data: BaseData) -> List[float]:
            results = [0.0] * len(buckets)
            data = sorted(feature.get_value(data))
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
        def get_names(win_size: int) -> List[str]:
            return [
                f"Hist{feature.get_names(win_size)[0][3:]}{bucket}"
                for bucket in buckets
            ]

        @staticmethod
        def clip(win_size: int) -> float:
            return [random_round] * len(buckets)

    return Hist


# Summarized features
MaxSizes = summary(Sizes, max)
MinSizes = summary(Sizes, min)
SumSizes = summary(Sizes, sum)
MeanSizes = summary(Sizes, mean)
StdevSizes = summary(Sizes, stdev)
VarianceSizes = summary(Sizes, variance)
EntropySizes = summary(Sizes, binary_entropy)
TopSizes = topN(Sizes, 5)

k = 5
HistSizes = hist(Sizes, list(range(0, Sizes.max(), k)))

MaxEntropies = summary(Entropies, max)
MinEntropies = summary(Entropies, min)
SumEntropies = summary(Entropies, sum)
MeanEntropies = summary(Entropies, mean)
StdevEntropies = summary(Entropies, stdev)
VarianceEntropies = summary(Entropies, variance)
EntropyEntropies = summary(Entropies, binary_entropy)
TopEntropies = topN(Entropies, 5)
HistEntropies = hist(Entropies, list(range(0, 8, 1)))



MaxDirSignBurstBytes = summary(DirSignBurstBytes, max)
MinDirSignBurstBytes = summary(DirSignBurstBytes, min)
SumDirSignBurstBytes = summary(DirSignBurstBytes, sum)
MeanDirSignBurstBytes = summary(DirSignBurstBytes, mean)
StdevDirSignBurstBytes = summary(DirSignBurstBytes, stdev)
VarianceDirSignBurstBytes = summary(DirSignBurstBytes, variance)
EntropyDirSignBurstBytes = summary(DirSignBurstBytes, binary_entropy)
TopDirSignBurstBytes = topN(DirSignBurstBytes, 5)
HistDirSignBurstBytes = hist(DirSignBurstBytes, list(range(-10_000, 10_000, 2_000)))


def dewindow_name(feature_name: str) -> str:
    return "".join(feature_name.split("_")[1:])


def window_name(window_id: WindowID, feature_name: str) -> str:
    return f"{window_id}_{feature_name}"
