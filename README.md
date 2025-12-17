# Introduction to Advanced Networking
In this coursework, we will explore the different elements that make up a modern computer network and guide you through building and configuring your very own network.

Think about your home network: you’ve got a Wi-Fi modem or router that connects your laptop, phone, TV, and maybe even your fridge (because why not) to the internet ([Figure 1](#home-topo)).

![Typical Home Network Topology](.resources/home-topo.png "Typical Home Network Topology"){width="2in"}
<!-- [home-topo]: home-topo.png "Typical Home Network Topology" -->

But have you ever wondered:
- How does your modem know which data belongs to which device?
- How does it forward your Netflix traffic to the internet while sending a Zoom call to your laptop at the same time?
- What magic is happening inside that little plastic box with too many blinking lights?
    
Well… quite a lot!
Your Wi-Fi modem is doing multiple jobs at once, such as:
- Routing: deciding where packets should go
- Switching: connecting devices inside your home network
- Network Address Translation (NAT): letting many devices share one public IP
- DNS Forwarding: helping translate website names into IP addresses
- Firewalling: keeping unwanted traffic out
By the end of this coursework, you’ll understand these components and even configure some of them yourself.

# Tools you will use

This coursework uses a combination of powerful tools designed for learning and experimenting with networks:
- Mininet
    - Used to create virtual network topologies
    - Allows you to instantiate hosts, switches, and links
    - Ideal for testing and experimenting in a contained environment
- P4
    - A protocol-independent language for programming how packets are processed
    - Lets you define custom behaviour inside routers and switches
    - Open-source, high-level, and used widely in software-defined networking research
- Python
    - The interactive language used to script Mininet and P4 interactions
    - Great for automation, controller development, and quickly testing network logic

# Understanding the Functionality of a Home Wi-Fi Modem

As mentioned, a home wifi modem consists of multiple separate components that perform different functions. Most home networks follow a star topology, where multiple devices connect to a central Wi-Fi modem — just like the one shown in [Figure 1](#home-topo).

Although it looks simple from the outside, your home router is quietly multitasking like a networking superhero. It:
- Manages wireless connections
- Acts as a Layer 2 switch for wired devices
- Performs routing between your home network (LAN) and the internet (WAN)
- Runs NAT so all your devices can share one public IP
- Handles DNS forwarding
- Implements firewall rules to protect your network

Understanding these functions gives you a strong foundation before we jump into designing and customizing networks using Mininet and P4.

To gain deeper insight into how each of these components works, we will disaggregate the Wi-Fi modem and examine each function individually. [Figure 2](#home-dis-topo) illustrates the different components and shows how they would be positioned in the network topology once separated.

![Disaggregated Home Network Topology](.resources/home-dis-topo.png "Disaggregated Home Network Topology"){width="5in"}
<!-- [home-dis-topo]: home-dis-topo.png "Disaggregated Home Network Topology" -->

We will begin by exploring Mininet by creating a simple topology with a single switch and using it to understand how a switch operates.

# Task 0: Opening the Dev Container
This is the first time you will need to work exclusively within the devcontainer environment. Mininet and Wireshark require root priviledges to execute certain commands, and the devcontainer is pre-configured to allow you to run these commands without any additional setup.

In order to open the code in a devcontainer, you should select the options `Open In devcontainer` when opening the folder in VSCode. If you missed the option when openning the project, you can still setup the devcontainer. Use the key combination of Ctrl+Shift+P to open the command palette and then select **Dev Containers: Open Folder in Container...**. Both options are depicted in the screenshots below.

![Figure 3: Open devcontainer from popup](.resources/devcontainer-open-boot.png){width="5in"}

![Figure 4: Open devcontainer from action menu](.resources/devcontainer-menu.png){width="5in"}

If you have opened correctly the devcontainer, you should see the following prompt when opening a new terminal in VSCode:

![Figure 5: Devcontainer terminal prompt](.resources/devcontainer-prompt.png){width="5in"}


# Task 1: Working with mininet
<!-- How to use mininet -->
**NOTE**: Run the command `xhost +` in a terminal on your lab machine (i.e., *not* in the devcontainer or a host in the mininet topology, a terminal on the actual lab machine) before starting Wireshark or xterm in the devcontainer. This command allows GUI applications running inside the devcontainer to be displayed on your host machine.

## What is Mininet?
Mininet is a powerful network emulator that allows you to create and test virtual network topologies on a single machine. It uses lightweight virtualization to run multiple hosts, switches, and links, all within a single Linux host. This makes it an ideal tool for learning about networking concepts, testing network applications, and experimenting with network protocols. Each host behaves like a real machine, capable of running TCP/IP stacks, executing real programs (web servers, ping, iperf, SSH), and having its own network addresses and interfaces.

## What is a Switch and what does it do?
A switch operates at Layer 2 (the Data Link layer) of the OSI model. Its main role is to connect multiple devices to each other using physical Ethernet links.

Instead of blindly broadcasting data to every device, a switch behaves intelligently. It reads MAC addresses and forwards packets only to the correct destination, improving speed and efficiency.

The MAC layer (also called the Ethernet layer) forms the outermost layer of a network packet within a local network. This is the layer the switch examines to decide where each packet should go.

### 📨 Analogy: The Office Mailroom
Think of a switch like an office mailroom:
- Every employee has a desk number (MAC address)
- The mailroom reads the desk number on each envelope
- Mail is delivered only to the correct desk, not to everyone

This is exactly how a switch ensures packets reach the right device.

## How Do We Use Mininet to Reproduce the Functionality of a Switch?
In this part of the coursework, we will focus on the highlighted component of the home Wi-Fi modem topology discussed earlier — the switch — as shown in [Figure 6](#home-topo-highlight). 
With mininet, we can reproduce this in two ways, using the command line or using python scripts. We will explore both one by one.
Mininet allows us to recreate real network behaviour in software, making it the perfect tool for experimenting without needing physical hardware. Using Mininet, we can build a simple network where multiple hosts are connected to a switch and observe how packets are forwarded between them.
There are two main ways to create this topology in Mininet:
- Using the Mininet Command Line Interface (CLI)
    - Quick and easy
    - Great for learning, testing, and experimenting
- Using Python Scripts
    - More flexible and powerful
    - Allows automation and repeatable experiments
    - Commonly used for larger or more complex topologies

![Figure 6: Typical Home Network Topology - focus Switch](.resources/home-topo-switch-focus.png){width="5in"}


We will explore both approaches step by step, starting with the command line and then moving on to Python scripting. This will help you understand not only how a switch works, but also how Mininet represents and manages network devices behind the scenes.
By the end of this section, you’ll be comfortable creating a basic switch-based topology and observing how data flows through it — just like in a real network.

### Quick Start: Switches with the Mininet CLI
Lets load using Mininet a simple topology on our devcontainer environment consisting of two hosts connected to a single switch. Open a terminal in the devcontainer and run the following command in the VSCode terminal. The command executes Mininet, creates the topology and give you access to the Mininet terminal from which you can run multiple commands.

```bash
mn --topo single,2 --link tc --mac --switch lxbr --controller none
```
![Figure 7: Mininet command explanation](.resources/mininet-cmd.png)

Once the topology is created, you should see the Mininet prompt:

```bash
mininet >
```

You can enter commands at this prompt to interact with the Mininet environment. The Mininet prompt offers a few simple commands to inspect the topology of your experiment. Try to run the following commands to inspect the network:

```
mininet> nodes
mininet> net
mininet> dump
```

The `nodes` command lists all the nodes (hosts and switches) in the topology. The `net` command shows the connections between the nodes, and the `dump` command provides detailed information about each node, including its IP address and MAC address.

You can also run commands on individual hosts by prefixing the command with the host name. For example, to test connectivity between the two hosts, you can use the `ping` command:

```
mininet> h1 ping -c 3 h2
```

The previous command will execute the program ping on host h1, send 3 ICMP echo requests to host `h2` and display the round-trip time (RTT) for each packet.

```
mininet > xterm h1 h2
```

![Figure 4: 231 mininet devcontainer](./.resources/mininet-intro-screenshot.png){width="6in"}

Each host in the network will have a set of network interfaces and a network configuration, in the form of unique IP and MAC addresses, on each interface. A network interface is important for a host to connect to the network. In our example, host `h1` will have single interface (`h1-eth0`) You can also inspect the interfaces of each host, using the built-in Linux network configuration tools. For example, you can use the iproute2 tool called `ip`. The program allows to inspect the addresses assigned to each interface (`ip addr show`), the IP routes (`ip route show`) and the interfaces (`ip dev show`). By running the commands `h1 ip addr show` and `h2 ip addr show`, you should see that each host has a single interface (eth0) with a unique IP address. You can also run the command `ip addr show`, in the xterm terminal you create in the previous step on each host. 



### Automating Switch Topologies with Python
Mininet offers a Python API to create topologies. The lab template provides you with a very basic topology file (`./topology.py`) that, through Mininet, will produce an emulated network consisting of 2 host connected via two seperate links to a switch ([Figure 8](#topology)). But what exactly does all that mean?

![Figure 8: Topology](.resources/switch-topo.png)

<!-- ![Figure 6: Mininet Topology file and related API calls](.resources/topo.png) -->

There are 3 fundamental components to a Mininet topology: *Hosts*, *Switches* and *Links*. In later stages we will discuss additional custom components, such as routers, but for now we will focus on these 3.

The topology in the lab template code defines a custom class that extends the `Topo` class in Mininet. This class contains the logic to create the nodes and links that make up the topology. The documentation for the `Topo` class can be found [here](http://mininet.org/api/classmininet_1_1topo_1_1Topo.html), and it allows to add each of these components via the `addHost`, `addSwitch` and `addLink` methods. We will discuss these methods in more detail in Stage 4 and we will use them to implement custom topologies.


| **Method**                      | **Description**                                                           |
| ------------------------------- | ------------------------------------------------------------------------- |
| `addHost(name, **opts)`         | Adds a host to the topology with the given name and options.              |
| `addSwitch(name, **opts)`       | Adds a switch to the topology with the given name and options.            |
| `addLink(node1, node2, **opts)` | Adds a link between two nodes (hosts or switches) with the given options. |
|                                 |

As you might have guessed, the provided topology file generates the same topology as the one created by the command `mn --topo single,2 --mac --switch lxbr --controller none`. To run the provided topology, execute the following command in a terminal:

```bash
mn --custom ./topology.py --link tc --topo tutorialTopology --mac --switch lxbr --controller none
```

This command tells Mininet to use the custom topology defined in `topology.py` and to create a network with the specified parameters. Once the topology is created, you should see the Mininet prompt again. You can use the same commands as before to inspect the network and test connectivity between the hosts.


# Task 2: Testing the functionality of a switch in Mininet
In order to make sure that our switch is working properly, we need to make sure that our hosts can communicate with each other. In the previous task, we used two different ways to bring up a small part of the home network topology. in this task, we will establish and ensure connectivity between those components. This can be done by examining the traffic between the two hosts.

We can observe the sequence of messages exchanged between two protocol entities, delve down into the details of protocol operation, and cause protocols to perform certain actions and then observe these actions and their consequences. For this stage, we will use the popular network protocol analyzer Wireshark to capture and interactively browse the traffic running on a computer network.

In computer networks, a packet serves as a fundamental unit of data that facilitates communication between devices. In the next section, we will leartn about packets.

## What is a packet?

You can imagine a packet as a small, self-contained parcel carrying information across the vast landscape of the Internet.

Unlike traditional methods where a continuous stream of data is transmitted, the Internet relies on a concept known as packet switching. In this paradigm, large volumes of data are broken down into manageable pieces or "packets" before being sent across the network. Each packet, akin to an organised postcard, contains the actual data and essential information such as the source and destination addresses (i.e., IP addresses).

As these packets traverse the network, they follow diverse routes to reach their destination. This dynamic approach enhances efficiency and robustness, as multiple packets can travel concurrently without relying on a fixed path. Upon reaching their destination, the packets are reassembled, reconstructing the original message or data.

## How can you view incoming and outgoing packets on your computer?

A **packet sniffer** is the basic tool for observing incoming and outgoing packets. As the name suggests, a packet sniffer captures ("sniffs") messages being sent and received from or by your computer; it will also typically store and display the contents of the various protocol fields in these captured messages. A packet sniffer is passive: it observes messages being sent and received by applications and protocols running on your computer but never sends packets.  Similarly, received packets are never explicitly addressed to the packet sniffer. Instead, a packet sniffer gets a *copy* of packets sent or received from/by application and protocols executing on your machine.

Figure 8 shows the structure of a packet sniffer. At the right of Figure 8 are the protocols (in this case, Internet protocols) and applications (such as a web browser or email client) that usually run on your computer. The packet sniffer, shown within the dashed rectangle in Figure 8, is an addition to the usual software in your computer and consists of two parts:

![Figure 9: Packet sniffer structure](.resources/packet-sniffer.jpg){width="4.325937226596675in"
height="1.703124453193351in"}

* The **packet capture library** receives a copy of every packet that is sent from or received by your computer over a given interface (e.g., Ethernet card or Wi-Fi). As discussed above, messages exchanged by protocols such as HTTP (to be covered on Thursday of Week 12) are eventually encapsulated in packets that are transmitted over physical media such as an Ethernet cable or a Wi-Fi radio. Capturing the packets thus gives you all the messages sent/received from/by all the applications executing on your computer.

* The second component of a packet sniffer is the **packet analyser**, which displays the contents of all fields within a protocol message.  To do so, the packet analyser must "understand" the structure of all messages exchanged by protocols. For example, suppose we are interested in displaying the various fields in messages exchanged by the HTTP protocol in Figure 1. The packet analyser understands the format of Ethernet frames and can identify the IP datagram within an Ethernet frame. It also understands the IP datagram format, so that it can extract the TCP segment within the IP datagram.

Finally, it understands the TCP segment structure, so it can extract the HTTP message contained in the TCP segment. Finally, it understands the HTTP protocol and so, for example, knows that the first bytes of an HTTP message will contain the string "GET," "POST," or "HEAD," as shown later in Figure 5 below.

In 333 labs, we will use the [Wireshark packet sniffer](http://www.wireshark.org/) for these labs, allowing us to display the contents of messages being sent/received from/by protocols at different levels of the protocol stack. (Technically speaking, Wireshark is a packet analyser that uses a packet capture library on your computer).

Also, technically speaking, Wireshark captures link-layer frames as shown in Figure 1, but uses the generic term "packet" to refer to link-layer frames, network-layer datagrams, transport-layer segments, and application-layer messages, so we'll use the less-precise "packet" term here to go along with Wireshark convention). Wireshark is a free network protocol analyser that runs on Windows, Mac, and Linux/Unix computers. It's an ideal packet analyser for our labs -- it is stable, has a large user base and well-documented support that includes:

* a [user guide](http://www.wireshark.org/docs/wsug_html_chunked/)
* a [man pages](http://www.wireshark.org/docs/man-pages/)
* a [detailedFAQ](http://www.wireshark.org/faq.html)
* Rich functionality that includes the capability to analyze hundreds of protocols, and a well-designed user interface. 
  
It operates in computers using Ethernet, serial (PPP), 802.11 (WiFi) wireless LANs, and many other link-layer technologies.

### Part 0: Running Wireshark

> **NOTE**: Run the command `xhost +` in a terminal on your lab machine (i.e., *not* in the devcontainer or a host in the mininet topology, a terminal on the actual lab machine) before starting Wireshark or xterm in the devcontainer. This command allows GUI applications running inside the devcontainer to be displayed on your host machine.

You can start Wireshark on a the node h1 of your topology by open an xterm (i.e., `> xterm h1`) and then entering the command `wireshark` in the terminal.

![Figure 10: Running wireshark from the SCC.333 DevContainer.](.resources/mininet-wireshark.png){width="3.158688757655293in"
height="2.0781244531933507in"}

When you run the Wireshark program, you'll get a startup screen that looks like the one below. Different versions of Wireshark will have different startup screens -- so don't panic if yours doesn't look exactly like the screen below! The Wireshark documentation states "As Wireshark runs on many different platforms with many different window managers, different styles applied and there are different versions of the underlying GUI toolkit used, your screen might look different from the provided screenshots. But as there are no real differences in functionality these screenshots should still be well understandable." Well said.

![Figure 11: Initial Wireshark Screen](.resources/wireshark-gui.png){width="4.875404636920385in" height="3.4843744531933507in"}

There's not much that's very interesting on this screen. But note that under the Capture section, there is a list of so-called interfaces.  In the SCC 231 DevContainer we focus on one interface -- "h1-eth0", (shaded in blue in Figure 10) which is the interface for Ethernet access. All packets to/from this container will pass through the Ethernet interface, so it's here where we'll want to capture packets. Double-click on this interface to begin packet capture.

Now let's take Wireshark out for a spin! If you click on one of these interfaces to start packet capture (i.e., for Wireshark to begin capturing all packets being sent to/from that interface), a screen like the one below will be displayed, showing information about the captured packets. Once you start packet capture, you can stop it by using the Capture pull- down menu and selecting Stop (or by clicking on the red square button next to the Wireshark fin in Figure 9). To test this, you can sent a few packets from host h1 to host h2 by running the command `h1 ping -c 5 h2`.

![Figure 12: Wireshark window, during and after capture](.resources/wireshark-explain.jpg){width="6.6in" height="3.4in"}

This looks more interesting! The Wireshark interface has five major components:

* The **command menus** are standard pull-down menus located at the top of the Wireshark window (and on a Mac at the top of the screen as well; the screenshot in Figure 3 is from a Mac). Of interest to us now are the File and Capture menus. The File menu allows you to save captured packet data or open a file containing previously captured packet data and exit the Wireshark application. The Capture menu allows you to begin packet capture.
* The **packet-listing window** displays a one-line summary for each packet captured, including the packet number (assigned by Wireshark; note that this is *not* a packet number contained in any protocol's header), the time at which the packet was captured, the packet's source and destination addresses, the protocol type, and protocol-specific information contained in the packet. The packet listing can be sorted according to any of these categories by clicking on a column name. The protocol type field lists the highest-level protocol that sent or received this packet, i.e., the protocol that is the source or ultimate sink for this packet.
* The **packet-header details window** provides details about the packet selected (highlighted) in the packet-listing window. (To select a packet in the packet- listing window, place the cursor over the packet's one-line summary in the packet- listing window and click with the left mouse button.). These details include information about the Ethernet frame (assuming the packet was sent/received over an Ethernet interface) and IP datagram that contains this packet. The amount of Ethernet and IP-layer detail displayed can be expanded or minimized by clicking on the plus/minus boxes or right/downward-pointing triangles to the left of the Ethernet frame or IP datagram line in the packet details window. If the packet has been carried over TCP or UDP, TCP or UDP details will also be displayed, which can similarly be expanded or minimized. Finally, details about the highest-level protocol that sent or received this packet are also provided.
* The **packet-contents window** displays the entire contents of the captured frame, in both ASCII and hexadecimal format.
* Towards the top of the Wireshark graphical user interface, is the **packet display filter field,** into which a protocol name or other information can be entered in order to filter the information displayed in the packet-listing window (and hence the packet-header and packet-contents windows). In the example below, we'll use the packet-display filter field to have Wireshark hide (not display) packets except those that correspond to HTTP messages.



# Task 3: Building your very own switch with P4!