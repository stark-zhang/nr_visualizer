import math
from typing import List, Tuple, Union

from renderer import NrSignalsCommon, ResourceGridFragment, T_PRB, T_SUBCARRIER, SignalId

__all__ = ['ChannelStateIndicatorRs']


class ChannelStateIndicatorRsConf:
    def __init__(self, row: int, num_of_k: int, num_of_l: int, row_cdm_index: int, port: int, cdm_group: str, density: Tuple[Union[float, int], ...], l_add: bool = False):
        self.row = row
        self.num_of_k = num_of_k
        self.num_of_l = num_of_l
        self.row_cdm_index = row_cdm_index
        self.density = density
        self.port = port
        self.l_add = l_add
        self.cdm_group = cdm_group


CSI_RS_LOCATIONS = {
    # see TS 38.211 Table 7.4.1.5.3-1 CSI-RS locations within a slot
    0x01: ChannelStateIndicatorRsConf(1, 1, 1, 1, 1, 'noCDM', (3,)),
    0x02: ChannelStateIndicatorRsConf(2, 1, 1, 1, 1, 'noCDM', (1, 0.5)),
    0x03: ChannelStateIndicatorRsConf(3, 1, 1, 1, 2, 'fd-CDM2', (1, 0.5)),
    0x04: ChannelStateIndicatorRsConf(4, 1, 1, 1, 4, 'fd-CDM2', (1,)),
    0x05: ChannelStateIndicatorRsConf(5, 1, 1, 1, 4, 'fd-CDM2', (1,), True),
    0x06: ChannelStateIndicatorRsConf(6, 4, 1, 1, 8, 'fd-CDM2', (1,)),
    0x07: ChannelStateIndicatorRsConf(7, 2, 1, 1, 8, 'fd-CDM2', (1,), True),
    0x08: ChannelStateIndicatorRsConf(8, 2, 1, 1, 8, 'cdm4-FD2-TD2', (1,)),
    0x09: ChannelStateIndicatorRsConf(9, 6, 1, 1, 12, 'fd-CDM2', (1,)),
    0x0A: ChannelStateIndicatorRsConf(10, 3, 1, 1, 12, 'cdm4-FD2-TD2', (1,)),
    0x0B: ChannelStateIndicatorRsConf(11, 4, 1, 2, 16, 'fd-CDM2', (1, 0.5), True),
    0x0C: ChannelStateIndicatorRsConf(12, 4, 1, 1, 16, 'cdm4-FD2-TD2', (1, 0.5)),
    0x0D: ChannelStateIndicatorRsConf(13, 3, 2, 2, 24, 'fd-CDM2', (1, 0.5), True),
    0x0E: ChannelStateIndicatorRsConf(14, 3, 2, 1, 24, 'cdm4-FD2-TD2', (1, 0.5)),
    0x0F: ChannelStateIndicatorRsConf(15, 3, 1, 1, 24, 'cdm8-FD2-TD4', (1, 0.5)),
    0x10: ChannelStateIndicatorRsConf(16, 4, 2, 4, 32, 'fd-CDM2', (1, 0.5), True),
    0x11: ChannelStateIndicatorRsConf(17, 4, 2, 1, 32, 'cdm4-FD2-TD2', (1, 0.5)),
    0x12: ChannelStateIndicatorRsConf(18, 4, 1, 1, 32, 'cdm8-FD2-TD4', (1, 0.5)),
}


class ChannelStateIndicatorRs(NrSignalsCommon):
    def __init__(self, conf: int, slot: int, freq_positions: str, start_prb: int, bandwidth: int, density: float, sym1: int, *, sym2: int = -1, zero_powered: bool = False,
                 odd_prb: bool = False, trs: bool = False):
        """
        Channel State Indication Reference Signal in NR downlink PHY
        :param conf: configuration row in TS 38.211 Table 7.4.1.5.3-1
        :param slot: which slot to render
        :param freq_positions: bitmap for offset in PRB
        :param start_prb: start PRB of CSI-RS
        :param bandwidth: the bandwith in prbs of CSI-RS
        :param density: must be one of (0.5, 1, 3), density of CSI-RS in full bandwidth
        :param sym1: the 1st symbol for CSI-RS occuration
        :param sym2: (optional)the 2nd symbol for CSI-RS occuration, for configration row 13, 14, 16, 17, 18
        :param zero_powered: (optional)type of CSI-RS, True for Zero-powered CSI-RS
        :param odd_prb: (optional)for density 0.5, determine CSI-RS would occur on odd PRBs or even PRBs
        :param trs: (optional)tracking reference signal or not
        """
        super().__init__(slot)
        self.conf = CSI_RS_LOCATIONS[conf]
        self.bitmap = int(freq_positions, 2)
        self.sym1 = sym1
        self.sym2 = sym2
        self.start_prb = start_prb
        self.num_of_prbs = bandwidth
        self.density = density
        self.even_or_odd = 1 if odd_prb else 0
        self.zero_powered = zero_powered
        self.trs = trs

    def _get_offset_in_prb(self) -> T_SUBCARRIER:
        offset_in_prb = int(math.log2(self.bitmap))

        # we assume that bitmap is right, graruateed by json validator
        # see TS 38.211 Chapter 7.4.1.5.3
        if self.conf.row == 1:
            ret = [offset_in_prb + 4 * i for i in range(3)]
        elif self.conf.row == 2:
            ret = [offset_in_prb]
        elif self.conf.row == 4:
            ret = [offset_in_prb + 2 * i for i in range(2)]
        else:
            ret = [offset_in_prb + 2 * i for i in range(self.conf.num_of_k)]

        return ret

    def _get_available_prbs(self) -> T_PRB:
        return tuple(range(self.start_prb, self.start_prb + self.num_of_prbs))

    def _get_symbols_in_slot(self) -> T_SUBCARRIER:
        ret = [self.sym1, self.sym1 + 1, self.sym2, self.sym2 + 1]

        if self.conf.num_of_l == 2:
            if self.sym2 < 0: raise ValueError('invalid ofdm symbol {} for CSI-RS!'.format(self.sym2))
            if not self.conf.l_add: ret = ret[::2]
        else:
            if self.conf.l_add:
                ret = ret[:2]
            else:
                ret = ret[:1]

        return ret

    def get_resource_grid_fragments(self) -> List[ResourceGridFragment]:
        ret: List[ResourceGridFragment] = []
        signal_id = SignalId.ZP_CSI_RS if self.zero_powered else SignalId.NZP_CSI_RS

        subcarriers = self._get_offset_in_prb()
        prbs = self._get_available_prbs()
        symbols = self._get_symbols_in_slot()
        port = 0

        # filter the prb if CSI-RS density is 0.5
        if self.density == 0.5: prbs = [prb for prb in prbs if prb % 2 == self.even_or_odd]

        if self.conf.row == 1:
            ret.append(ResourceGridFragment(port, signal_id, symbols[0], prbs, subcarriers))
        elif self.conf.row == 4:
            for k in subcarriers:
                for l in symbols:
                    if port > self.conf.port: raise ValueError('Overflow the maximum port {}!'.format(self.conf.port))
                    ret.append(ResourceGridFragment(port, signal_id, l, prbs, (k, k + 1)))
                    ret.append(ResourceGridFragment(port + 1, signal_id, l, prbs, (k, k + 1)))
                    port += 2
        else:
            for l in symbols:
                for k in subcarriers:
                    if port > self.conf.port: raise ValueError('Overflow the maximum port {}!'.format(self.conf.port))
                    ret.append(ResourceGridFragment(port, signal_id, l, prbs, (k, k + 1)))
                    ret.append(ResourceGridFragment(port + 1, signal_id, l, prbs, (k, k + 1)))
                    port += 2

        return ret

# EOF
