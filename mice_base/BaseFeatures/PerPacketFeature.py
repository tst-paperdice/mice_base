from abc import ABC, abstractmethod

from ..fe_types import FlowID, Pkt


class PerPacketFeature(ABC):
    @staticmethod
    @abstractmethod
    def min():
        """The minimum value possible for this feature.
        # TODO: is this the max theoretical value of the feature, or the max observed value in the data set?
        """
        pass

    @staticmethod
    @abstractmethod
    def max():
        """The maximum value possible for this feature.
        # TODO: is this the min theoretical value of the feature, or the min observed value in the data set?
        """
        pass

    @staticmethod
    @abstractmethod
    def get_value(fid: FlowID, pkt: Pkt):
        pass

    @staticmethod
    @abstractmethod
    def clip(val: float) -> float:
        # TODO: is this method just intended to convert from float to int?
        pass

    # @property
    # @abstractmethod
    # def name(self) -> str:
    #     """The name of the feature to be used in the label of the resulting dataset.

    #     Returns:
    #         str: The name of the feature
    #     """
    #     pass
