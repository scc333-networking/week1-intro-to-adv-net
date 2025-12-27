all: topo

topo: topology.py
    mn --custom ./topology.py --link tc --topo simple --mac --switch lxbr --controller none --arp

clean:
	mn -c