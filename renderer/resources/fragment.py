from typing import List, Tuple

from .common import SignalId

__all__ = [
    'ResourceGridFragment',
    'T_PRB',
    'T_SUBCARRIER',
    'NrSignalsCommon'
]

T_SUBCARRIER = T_PRB = Tuple[int, ...]


class ResourceGridFragment:
    def __init__(self, port: int, signal: SignalId, symbol: int, prbs: T_PRB, subcarriers: T_SUBCARRIER):
        """
        Resource Grid Occuration for specific signal/channel
        :param port: which port to fill
        :param signal: channel/signal ID
        :param symbol: ofdm symbols occured by signal
        :param prbs: PRBs occured by signal
        :param subcarriers: subcarriers per PRB occured by signal
        """
        self.port = port
        self.symbol = symbol
        self.prbs = prbs
        self.subcarriers = subcarriers
        self.id = signal

    def __str__(self) -> str:
        return 'Signal {} occured on port {}, symbol {}, subcarriers {} of prbs {}'.format(str(self.id), self.port, self.symbol,
                                                                                           self.subcarriers, self.prbs)


class NrSignalsCommon:
    def __init__(self, slot: int):
        self.slot = slot

    def get_resource_grid_fragments(self) -> List[ResourceGridFragment]: ...

# EOF


# EOF
