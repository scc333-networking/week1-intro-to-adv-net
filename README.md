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

## What is a Switch?
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

### Automating Switch Topologies with Python
Mininet offers a Python API to create topologies. The lab template provides you with a very basic topology file (`./topology.py`) that, through Mininet, will produce an emulated network consisting of 2 host connected via two seperate links to a switch ([Figure 8](#topology)). But what exactly does all that mean?

![Figure 8: Topology](.resources/switch-topo.png)

<!-- ![Figure 6: Mininet Topology file and related API calls](.resources/topo.png) -->

There are 3 fundamental components to a Mininet topology: *Hosts*, *Switches* and *Links*. In later stages we will discuss additional custom components, such as routers, but for now we will focus on these 3.

- **Hosts:** act like computers. Hosts have their own terminal window where you can execute commands acting as that host and own interfaces with an IP and MAC addresses (network and link layer addresses respectively).

- **Switches:** are applications that can forward packets. They operate silently and are able to transmit packets efficiently between hosts without any configuration. Switches also have interfaces, but they do not have IP addresses (only MAC addresses).

- **Links:** links act like the cables connecting nodes (hosts and switches) together. When you add a link, the two end-points of the link will have a new interface created automatically.

The topology in the lab template code  defines a custom class that extends the `Topo` class in Mininet. This class contains the logic to create the nodes and links that make up the topology. The documentation for the `Topo` class can be found [here](http://mininet.org/api/classmininet_1_1topo_1_1Topo.html), and it allows to add each of these components via the `addHost`, `addSwitch` and `addLink` methods. We will discuss these methods in more detail in Stage 4 and we will use them to implement custom topologies.


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

# Task 3: Building your very own switch with P4!