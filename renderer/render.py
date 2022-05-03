from typing import List

import numpy as np
from matplotlib import pyplot as plt

from .resources import NUM_OF_SUBCARRIER_PER_PRB, NUM_OF_SYMBOL_PER_SLOT_EXTEND_CP, NUM_OF_SYMBOL_PER_SLOT_NORMAL_CP
from .resources.colors import PREDEFINED_COLORS
from .resources.fragment import NrSignalsCommon
from .resources.grid import NrNumerology, NrSlotResourceGrid


class NrPhysicalResourceRenderer:
    def __init__(self, slots: int, bandwidth: int, extended_cp: bool = False):
        self.slots = slots
        self.bandwidth = bandwidth
        self.symbols_per_slot = NUM_OF_SYMBOL_PER_SLOT_EXTEND_CP if extended_cp else NUM_OF_SYMBOL_PER_SLOT_NORMAL_CP
        self.grids: List[NrSlotResourceGrid] = []
        self.figure = plt.figure()
        self.axes = self.figure.subplots(ncols=self.slots)
        self._reset(extended_cp)

    def _reset(self, extended_cp: bool = False):
        if not isinstance(self.axes, np.ndarray): self.axes = [self.axes]

        for slot in range(self.slots):
            ax = self.axes[slot]
            ax.set_xlim(0, self.symbols_per_slot)
            ax.set_ylim(0, self.bandwidth * NUM_OF_SUBCARRIER_PER_PRB)
            ax.set_xticks(range(0, self.symbols_per_slot, 1))
            ax.set_yticks(range(0, self.bandwidth * NUM_OF_SUBCARRIER_PER_PRB, 1))
            ax.set_xticklabels(labels='')
            ax.set_yticklabels(labels='')
            ax.tick_params(which='major', bottom=False, left=False)
            ax.grid(which='major', color='black', linestyle='-', linewidth=1)
            self.grids.append(NrSlotResourceGrid(self.bandwidth, ax, NrNumerology.NUMEROLOGY_0, extended_cp))

    def fill_signal(self, signal: NrSignalsCommon):
        self.grids[signal.slot].fill(signal)

    def plot(self, *, port=0):
        for grid in self.grids:
            grid.plot(port, colors=PREDEFINED_COLORS)

        plt.show()
