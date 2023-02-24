from typing import NamedTuple

import numpy as np


class ScaleParams(NamedTuple):
    mu: np.array
    std: np.array
    eps: float

    def scale(self, data, idx=None):
        if idx is None:
            return (data - self.mu) / (self.std + self.eps)
        else:
            return (data - self.mu[idx]) / (self.std[idx] + self.eps)

    def descale(self, data, idx=None):
        if idx is None:
            return (data * (self.std + self.eps)) + self.mu
        else:
            return (data * (self.std[idx] + self.eps)) + self.mu[idx]

    def to_json(self):
        return {"mu": self.mu.tolist(), "std": self.std.tolist(), "eps": self.eps}
