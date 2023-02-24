import math
from random import random


def random_round(val: float) -> int:
    """Randomly round a number up or down.

    Args:
        val (float): The number to randomly round.

    Returns:
        int: The rounded result.
    """
    return math.floor(val + random())
