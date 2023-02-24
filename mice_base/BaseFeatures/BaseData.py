import numpy as np
import itertools as it
from ..ScaleParams import ScaleParams
from typing import (
    List,
    NamedTuple
)


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
            scaled[divisions: 2 * divisions].tolist(),
            scaled[2 * divisions:].tolist(),
        )

    def descale(self, scaler: ScaleParams):
        descaled = scaler.descale(self.to_array())
        divisions = len(descaled) // 3
        return BaseData(
            descaled[0:divisions].tolist(),
            descaled[divisions: 2 * divisions].tolist(),
            descaled[2 * divisions:].tolist(),
        )

    @classmethod
    def from_array(cls, arr):
        divisions = len(arr) // 3
        return BaseData(
            arr[0:divisions].tolist(),
            arr[divisions: 2 * divisions].tolist(),
            arr[2 * divisions:].tolist(),
        )
