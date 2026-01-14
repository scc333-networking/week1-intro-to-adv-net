from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.nodelib import LinuxBridge


class LabTopology(Topo):
    """Two hosts connected to a single switch."""

    def build(self):
        # Create a single switch
        s1 = self.addSwitch("s1")

        # Create two hosts
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")

        # Connect hosts to the switch
        self.addLink(h1, s1)
        self.addLink(h2, s1)


# Expose topology for `	mn --custom topology.py --topo LabTopology --controller none --mac --arp --switch lxbr --link tc`
topos = {
    "LabTopology": (lambda: LabTopology()),
}


def run():
    """Spin up the network, run a quick test, then drop into CLI."""
    net = Mininet(topo=LabTopology(), link=TCLink,
                  controller=None, autosetup=True, switch=LinuxBridge)
    net.start()

    # Quick connectivity test
    net.pingAll()

    # Interactive CLI for exploration
    CLI(net)

    # Clean up
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    run()
