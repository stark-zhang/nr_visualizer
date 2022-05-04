from enum import IntEnum

# about frame structures
BASIC_SUBCARRIER_FREQ = 15  # in kHz
NUM_OF_SUBCARRIER_PER_PRB = 12
NUM_OF_SYMBOL_PER_SLOT_NORMAL_CP = 14
NUM_OF_SYMBOL_PER_SLOT_EXTEND_CP = 12
NUM_OF_ANTEENA_PORT = 32
MAX_BANDWIDTH_FR1 = 100  # in MHz
MAX_BANDWIDTH_FR2 = 400


class SignalId(IntEnum):
    Unused = 0,

    # 0x10xx for Downlink Channels
    PBCH = 0x1001,
    PDCCH = 0x1002,
    PDCCH_Unused = 0x1003,
    PDSCH = 0x1004,
    PDSCH_Unused = 0x1005,

    # 0x11xx for Downlink Reference Signals
    PSS = 0x1101,
    SSS = 0x1102,
    PTRS = 0x1103,
    NZP_CSI_RS = 0x1104,
    ZP_CSI_RS = 0x1105,
    RIM_RS = 0x1106,
    PRS = 0x1107,
    # DMRS_MARK = 0x0010
    DMRS_PBCH = 0x1111,
    DMRS_PDCCH = 0x1112,
    DMRS_PDSCH = 0x1113,

    # 0x20xx for Uplink Channels

    # 0x21xx for Uplink Reference Signals

    # 0x30xx for other channels and signals


class SignalIdHelper:
    Downlink_CH = 0x1000
    Downlink_RS = 0x1100
    Uplink_CH = 0x2000
    Uplink_RS = 0x2100
    DeModulation_Mark = 0x0010

    @classmethod
    def is_downlink(cls, signal: SignalId) -> bool:
        return signal & cls.Downlink_CH != 0

    @classmethod
    def is_downlink_channel(cls, channel: SignalId) -> bool:
        return (channel & cls.Downlink_CH != 0) and (channel & cls.Downlink_RS == 0)

    @classmethod
    def is_downlink_rs(cls, signal: SignalId) -> bool:
        return not cls.is_downlink_channel(signal)

    @classmethod
    def is_dmrs(cls, signal: SignalId) -> bool:
        return signal & cls.DeModulation_Mark != 0

# EOF
