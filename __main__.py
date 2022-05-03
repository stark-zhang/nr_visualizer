from renderer.render import NrPhysicalResourceRenderer
from signals import ChannelStateIndicatorRs

if __name__ == '__main__':
    csi_rs = ChannelStateIndicatorRs(16, 1, '0010', 0, 2, 1, 2, sym2=9)

    renderer = NrPhysicalResourceRenderer(2, 2)
    renderer.fill_signal(csi_rs)
    renderer.plot(port=31)

# EOF
