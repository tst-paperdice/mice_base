# MICE
from .WindowFeature import windowize
from ..fe_types import FlowID, Pkt
from .PerPacketFeature import PerPacketFeature

# scapy
import scapy.layers.inet


class Direction(PerPacketFeature):
    """Direction of the packet, either +1 or -1.
        * +1 if the packet is going from the source to the destination
        * -1 if the packet is going from the destination to the source
    TODO: what are the source and destination in this case? Assuming the client is the source and the server/proxy is the destination?
    """

    name = "Direction"

    @staticmethod
    def min() -> int:
        return -1

    @staticmethod
    def max() -> int:
        return 1

    @staticmethod
    def get_value(fid: FlowID, pkt: Pkt) -> int:
        # ignoring port so we can share logic for UDP and TCP
        # TODO: ^ code does NOT appear to ignore port. Is comment or code correct?
        if not pkt.haslayer(scapy.layers.inet.IP):
            return 0

        if pkt.haslayer(scapy.layers.inet.UDP):
            return (
                +1
                if pkt[scapy.layers.inet.IP].src == fid.sip
                and pkt[scapy.layers.inet.IP].dst == fid.dip
                and pkt[scapy.layers.inet.UDP].sport == fid.sport
                and pkt[scapy.layers.inet.UDP].dport == fid.dport
                else -1
            )
        elif pkt.haslayer(scapy.layers.inet.TCP):
            return (
                +1
                if pkt[scapy.layers.inet.IP].src == fid.sip
                and pkt[scapy.layers.inet.IP].dst == fid.dip
                and pkt[scapy.layers.inet.TCP].sport == fid.sport
                and pkt[scapy.layers.inet.TCP].dport == fid.dport
                else -1
            )
        else:
            return (
                +1
                if pkt[scapy.layers.inet.IP].src == fid.sip
                and pkt[scapy.layers.inet.IP].dst == fid.dip
                else -1
            )

    @staticmethod
    def clip(val: float) -> float:
        return -1 if val < 0 else 1


Directions = windowize(Direction)
