from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.util import LinuxBridge


class LabTopology(Topo):
	"""Two hosts connected to a single switch."""

	def build(self):
		# Create a single switch
		s1 = self.addSwitch("s1")

		# Create two hosts
		homePC = self.addHost("homePC", ip="192.168.1.2/24")
		tablet = self.addHost("tablet", ip="192.168.1.3/24")
		phone = self.addHost("phone", ip="192.168.1.4/24")

		

		# Connect hosts to the switch
		self.addLink(homePC, s1)
		self.addLink(tablet, s1)
		self.addLink(phone, s1)
		
# Expose topology for `mn --custom topology.py --topo simple`
topos = {
	"simple": (lambda: LabTopology()),
}


def run():
	"""Spin up the network, run a quick test, then drop into CLI."""
	net = Mininet(topo=LabTopology(), link=TCLink, controller=None, autosetup=True, switch=LinuxBridge)
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

