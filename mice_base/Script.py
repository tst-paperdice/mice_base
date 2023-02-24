import json
from enum import Enum
from typing import List, NamedTuple, Optional

from typing_extensions import TypedDict


class Origin(str, Enum):
    CLIENT = "client"
    SERVER = "server"

class Protocol(str, Enum):
    TCP = "tcp"
    UDP = "udp"

class ScriptEntry(NamedTuple):
    id: str  # id, should be unique across both origins
    origin: Origin  # client or server, indicating who sends this packet
    size: int  # size of packet in bytes - should be inclusive of Ethernet and TCP/UDP headers
    entropy: float  # desired entropy, to 4-digits or whatever's feasible
    protocol: Protocol  # TCP or UDP
    flags: int  # TCP flags encoded as a byte
    dependence: str  # id of packet that _must be sent/received_ before we can send this
    delay: int  # milliseconds to delay from when we are otherwise going to send this packet
    sample: Optional[str]

    @classmethod
    def from_json(cls, s: str):
        data = json.loads(s)
        if 'sample' not in data:
            data['sample'] = None

        return ScriptEntry(**data)

    def to_json(self) -> str:
        return self._asdict()
