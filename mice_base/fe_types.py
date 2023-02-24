from enum import Enum
from typing import (
    Any,
    List,
    Union,
    Tuple,
    Type,
    NamedTuple,
    Iterable,
    Dict,
    Callable,
    Optional,
)
from dataclasses import dataclass

import scapy
import scapy.layers
import scapy.layers.l2
from pandas import Series

# from simple_classifiers import PCAPClassifier

FeatureVal = Union[float, int]

# Feature class format:
#     ```
#     class FeatureName(NamedTuple):
#         val_name: str
#         agg_name: str
#
#         def __repr__(self):
#             return f"{self.val_name}_{self.agg_name}"
#     ```


class Proto(int, Enum):
    OTHER = 0
    TCP = 6
    UDP = 17


Feature = Tuple[str, FeatureVal]
Value = Any
Values = List[Value]
# FlowID = Tuple[str, str, str, str, int]  # SrcPI DstIP SrcPort DstPort Protocol
class FlowID(NamedTuple):
    sip: str  # Source IP address
    dip: str  # Destination IP address
    sport: str  # Source port
    dport: str  # Destination port
    proto: int  # Protocol, either UDP, TCP, or other (TODO: should type be Proto instead of int?)


# @dataclass(frozen=True, eq=True)
# class FlowID:
#     sip: str    # Source IP address
#     dip: str    # Destination IP address
#     sport: str  # Source port
#     dport: str  # Destination port
#     proto: int  # Protocol, either UDP, TCP, or other (TODO: should type be Proto instead of int?)


Pkt = Type[scapy.layers.l2.Ether]


class Pkts(NamedTuple):
    name: str
    data: List[Any]

    def __hash__(self):
        return hash(self.name)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    # def __contains__(self, item):
    #     return self.data.__contains__(item)


"""A flow as defined by a flow ID and a list of packets within the flow"""
# TODO: update to named tuple?
Flow = Tuple[
    FlowID,  # The ID of the flow.
    List[
        Pkt
    ],  # A list of all the packets within the flow. TODO: are these expected to be in a certain order?
]

"""A list of flows."""
Flows = List[Flow]

WindowID = str

"""A window (i.e. a contiguous subset) of packets within a flow."""
# TODO: is this even used?
class Window(NamedTuple):
    id: WindowID  # TODO: can this be generated dynamically?
    start: int
    end: int
    fid: FlowID
    data: Pkts


"""Classifier, Train, Test."""


class CTT(NamedTuple):
    clf: Any  # TODO: fix this type. fe_types probably shouldn't know anything about classifiers PCAPClassifier  # model
    train: Iterable[Iterable[int]]  # confusion matrix
    test: Iterable[Iterable[int]]  # confusion matrix


# TODO: probably move poison related things to into some other poison-specific repo.
Poison = Dict[str, Callable[[Series], Value]]


class PoisonTT(NamedTuple):
    poison: Poison
    t0: float
    t1: float
    t0_clf: CTT
    t1_clf: CTT
