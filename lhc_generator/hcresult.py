"""
Developed as part of the NES RoboLab Project at Technische Universität Dresden.
By Frank Busse in 2016.
"""

from enum import Enum


class HCResult(Enum):
    """ Return codes for the Hamming code interface"""
    valid = 1
    corrected = 2
    uncorrectable = 3
