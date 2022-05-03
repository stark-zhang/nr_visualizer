from enum import IntEnum
from typing import Dict

import numpy as np
from matplotlib.axes import Axes

from .common import NUM_OF_ANTEENA_PORT, NUM_OF_SUBCARRIER_PER_PRB, NUM_OF_SYMBOL_PER_SLOT_EXTEND_CP, NUM_OF_SYMBOL_PER_SLOT_NORMAL_CP, SignalId
from .fragment import NrSignalsCommon

__all__ = [
    'NrNumerology',
    'NrSlotResourceGrid',
]


class NrNumerology(IntEnum):
    NUMEROLOGY_0 = 0,
    NUMEROLOGY_1 = 1,
    NUMEROLOGY_2 = 2,
    NUMEROLOGY_3 = 3,
    NUMEROLOGY_4 = 4,
    NUMEROLOGY_5 = 5,


class NrSlotResourceGrid:
    def __init__(self, num_of_prbs: int, ax: Axes, numerology: NrNumerology, extended_cp: bool = False):
        self.bandwidth = num_of_prbs
        self.symbols = NUM_OF_SYMBOL_PER_SLOT_EXTEND_CP if extended_cp else NUM_OF_SYMBOL_PER_SLOT_NORMAL_CP
        self.numerology = numerology
        self.grids = np.ndarray(shape=(NUM_OF_ANTEENA_PORT, self.bandwidth * NUM_OF_SUBCARRIER_PER_PRB, self.symbols), dtype=np.int16)
        self.grids.fill(SignalId.Unused)
        self.ax = ax

    def fill(self, signal: NrSignalsCommon):
        for frag in signal.get_resource_grid_fragments():
            for prb in frag.prbs:
                for subcarrier in frag.subcarriers:
                    self.grids[frag.port][subcarrier + prb * NUM_OF_SUBCARRIER_PER_PRB][frag.symbol] = frag.id

    def plot(self, port: int = 0, *, colors: Dict[SignalId, str]):
        for l in range(self.grids.shape[1]):
            for k in range(self.grids.shape[2]):
                self.ax.broken_barh(
                    [(k, k + 1)], (l, l + 1), facecolor=colors[self.grids[port][l][k]]
                )
# EOF
