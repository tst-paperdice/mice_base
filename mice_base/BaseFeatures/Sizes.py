from typing import Optional
from functools import lru_cache

# scapy
import scapy.layers.inet

# MICE
from .WindowFeature import windowize
from .random_round import random_round
from ..fe_types import FlowID, Pkt
from .PerPacketFeature import PerPacketFeature


class Size(PerPacketFeature):
    """Size of the packet payload

    TODO: verify this description
    """

    name = "Size"

    @staticmethod
    def min() -> int:
        return 0

    @staticmethod
    def max() -> int:
        return 1440

    @staticmethod
    def get_value(fid: Optional[FlowID], pkt: Pkt) -> int:
        # TODO: would be nice to decouple this from scapy, but not sure it's worth the effort.
        if pkt.haslayer(scapy.layers.inet.IP):
            if pkt.haslayer(scapy.layers.inet.TCP):
                return (
                    pkt[scapy.layers.inet.IP].len - pkt[scapy.layers.inet.TCP].dataofs
                )
            elif pkt.haslayer(scapy.layers.inet.UDP):
                UDP_HEADER_SIZE = 8
                return pkt[scapy.layers.inet.UDP].len - UDP_HEADER_SIZE
        else:
            return 0

    @staticmethod
    def clip(val: float) -> float:
        return random_round(val)


Sizes = windowize(Size)


@staticmethod
@lru_cache(maxsize=128)
def _sizes_max(winsize: int):
    return [0, 0] + [Size.max() for idx in range(winsize - 2)]


Sizes.max = _sizes_max
