from collections import Counter
from functools import lru_cache

# MICE
from .WindowFeature import windowize
from ..fe_types import FlowID, Pkt
from .PerPacketFeature import PerPacketFeature

# scapy
import scapy.layers.inet

# scipy
from scipy.stats import entropy


class Entropy(PerPacketFeature):
    name = "Entropy"

    @staticmethod
    def entropy(bytelist) -> float:
        return entropy(list(Counter(bytelist).values()), base=2)

    @staticmethod
    @lru_cache(maxsize=2048)
    def _max_entropy(win_size) -> float:
        return Entropy.entropy([i % 256 for i in range(win_size)])

    @staticmethod
    def min() -> float:
        return 0.0

    @staticmethod
    def max() -> float:
        return 8.0  # TODO: should this return self._max_entropy() ?

    @staticmethod
    def get_value(fid: FlowID, pkt: Pkt) -> float:
        if pkt.haslayer(scapy.layers.inet.TCP):
            return Entropy.entropy(pkt.payload[scapy.layers.inet.TCP].original)
        elif pkt.haslayer(scapy.layers.inet.UDP):
            return Entropy.entropy(pkt.payload[scapy.layers.inet.UDP].original)
        else:
            return 0.0


Entropies = windowize(Entropy)


def _entropies_max(winsize: int):
    return [0, 0] + [Entropy.max() for idx in range(winsize - 2)]


Entropies.max = _entropies_max
