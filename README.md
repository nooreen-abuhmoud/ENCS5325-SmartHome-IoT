# ENCS5325 Smart-Home IoT Network

Smart-Home IoT Network Design and Performance Evaluation Using OMNeT++.

This project was developed for **ENCS5325 - Wireless Sensor Networks and Internet of Things** at Birzeit University.

The objective is to evaluate how network size, reporting interval, background traffic, application communication strategy, and packet size affect the performance of a smart-home IoT network.

---

## Simulation Environment

- **Simulator:** OMNeT++ 6.3.0
- **Framework:** INET 4.6.0
- **Wireless access technology:** IEEE 802.15.4
- **Application transport:** UDP
- **Simulated network layer:** IPv4
- **Core connection:** PPP/IP
- **Random repetitions:** 5 independent seeds for the main experiments

The constrained smart-home devices communicate through an IoT gateway to a core-side monitoring server.

---

## Important Simulation Boundary

The implemented end-to-end simulation uses:

```text
Application
    |
   UDP
    |
  IPv4
    |
IEEE 802.15.4
    |
 IoT Gateway
    |
 PPP / IP Core
    |
Monitoring Server

A complete IPv6/6LoWPAN adaptation layer is not simulated.

The packet-size study therefore contains two clearly separated types of evidence:

Simulator-derived results from the current OMNeT++/INET IPv4/UDP model.
Analytical 6LoWPAN fragmentation estimates based on RFC 4944 and RFC 6282.

FRAG1/FRAGN counts are analytical approximations and are not claimed as simulator-generated traces.

Smart-Home Scenario

The model contains:

Smart-home sensor nodes
Actuator nodes
One IoT gateway
One core monitoring server
IEEE 802.15.4 constrained wireless access
PPP/IP core-side connection

Two major traffic classes are evaluated:

Periodic Monitoring Traffic

Sensors periodically report measurements to the monitoring server.

Typical baseline settings:

Payload: 50 bytes
Reporting interval: 10 seconds
Critical Event Traffic

A smoke sensor generates an urgent alarm while normal periodic traffic continues in the background.

Typical critical-event settings:

Critical payload: 20 bytes
Critical event time: 50 s
Critical-event latency target: less than 100 ms
Experiments
Experiment 1 - Network Scalability

The number of active sensor nodes is varied while packet size and reporting interval remain fixed.

Parameters
N = 5, 10, 20, 30, 40
Payload = 50 B
Reporting interval = 10 s
Simulation duration = 100 s
Seeds = 5 per network size
Metrics
Packet Delivery Ratio (PDR)
Packet loss
End-to-end delay
Application throughput
Energy per delivered packet
Main Result

PDR remained 100% for all tested network sizes.

Mean delay increased only slightly from approximately:

5.365 ms at N = 5
to
5.565 ms at N = 40

No significant congestion was observed up to 40 active sensors under the tested baseline workload.

Results:

simulations/experiment1_scalability/results/
Experiment 2 - Reporting Interval and Energy Trade-off

This experiment studies the relationship between reporting frequency, network performance, and energy consumption.

Parameters
N = 12
Payload = 50 B
T = 1, 5, 10, 30, 60 s
Simulation duration = 600 s
Seeds = 5 per interval
Metrics
PDR
Packet loss
End-to-end delay
Total energy consumption
Energy per delivered packet
Throughput
Main Result

Increasing the reporting interval from 1 s to 60 s reduced total energy consumption from approximately:

16.1473 J
to
0.3055 J

This corresponds to approximately a 98.1% reduction in total energy consumption.

Reliability remained almost perfect throughout the interval sweep.

Results:

simulations/experiment2_reporting_interval/results/
Experiment 3 - Critical Event Under Background Traffic

A smoke alarm is generated while ordinary sensors continue sending periodic monitoring traffic.

Parameters
Background nodes:
N = 5, 10, 20, 30, 40

Background payload = 50 B
Background interval = 10 s

Critical payload = 20 B
Critical event time = 50 s

Simulation duration = 100 s
Seeds = 5 per load level
Metrics
Critical-event delivery rate
Critical-event packet loss
Mean critical-event delay
Standard deviation
Minimum delay
Maximum delay
Main Result

All critical events were delivered successfully:

Critical delivery rate = 100%
Critical packet loss = 0%

The maximum observed critical-event delay was approximately:

5.58 ms

This remained far below the project-defined requirement of:

100 ms

Results:

simulations/experiment3_critical_event/results/
Experiment 4 - Application Communication Strategy

Two application communication strategies are compared on the same smart-home topology.

Strategy A - Request/Response

The monitoring server polls the sensors and waits for responses.

Implementation:

Monitoring Server
    |
UdpBasicApp
    |
 Request
    v
 Sensor UdpEchoApp
    |
 Response
    v
Monitoring Server

This represents CoAP-like request/response behavior.

Strategy B - Publish/Subscribe-Like

Sensors periodically publish data directly to a subscriber at the monitoring server.

Implementation:

Sensor UdpBasicApp
      |
 Publication
      v
Monitoring Server UdpSink

This represents MQTT-like publish/subscribe traffic behavior at the application level.

Parameters
N = 12
Payload = 50 B

T = 1, 5, 10, 30, 60 s

Simulation duration = 600 s
Seeds = 5 per strategy and interval
Main Result

Request/response generated twice as many application packets as the publish/subscribe-like strategy.

Example at T = 1 s:

Request/Response:     14,376 packets
Publish/Subscribe:     7,188 packets

Therefore, the publish/subscribe-like strategy reduced application-level traffic by approximately 50% for the same update interval.

Request/response latency is measured as RTT, while publish/subscribe latency is measured as one-way delay. These latency values should therefore not be interpreted as directly equivalent metrics.

Results:

simulations/experiment4_application_strategy/results/
Experiment 5 - Packet Size and 6LoWPAN-Inspired Study

The final experiment evaluates how payload size affects:

Reliability
Delay
Throughput
Energy consumption
Simulated Payloads
20 B
50 B
80 B
100 B
150 B
250 B
500 B

Parameters:

N = 12
Reporting interval = 10 s
Simulation duration = 600 s
Seeds = 5 per payload
Simulated Results

Mean packet delay increased from approximately:

4.443 ms at 20 B

to:

36.691 ms at 500 B

PDR remained 100% through 250 B and decreased slightly to approximately:

99.639%

at 500 B.

Energy per delivered packet also increased substantially as payload size increased.

Results:

simulations/experiment5_packet_size/results/
Analytical 6LoWPAN Fragmentation Study

The assignment-required payload sizes were also evaluated analytically:

Application Payload	Estimated Fragments
20 B	1
50 B	1
100 B	2
200 B	3
400 B	6

These values are analytical estimates based on IEEE 802.15.4 frame constraints and 6LoWPAN compression/fragmentation assumptions.

More fragments increase:

Wireless airtime
End-to-end delay
Energy consumption
Exposure to retransmissions
Probability that at least one frame requires retransmission

The analytical study is intentionally separated from the OMNeT++ simulation results.

Project Structure
ENCS5325-SmartHome-IoT/
│
├── Makefile
├── README.md
│
├── simulations/
│   │
│   ├── baseline/
│   │   ├── Ieee802154Showcase.ned
│   │   ├── omnetpp.ini
│   │   └── startopology.xml
│   │
│   ├── experiment1_scalability/
│   │   ├── Ieee802154Showcase.ned
│   │   ├── omnetpp.ini
│   │   ├── analyze_exp1.py
│   │   └── results/
│   │
│   ├── experiment2_reporting_interval/
│   │   ├── Ieee802154Showcase.ned
│   │   ├── omnetpp.ini
│   │   ├── analyze_exp2.py
│   │   └── results/
│   │
│   ├── experiment3_critical_event/
│   │   ├── Ieee802154Showcase.ned
│   │   ├── omnetpp.ini
│   │   └── results/
│   │
│   ├── experiment4_application_strategy/
│   │   ├── Ieee802154Showcase.ned
│   │   ├── omnetpp.ini
│   │   └── results/
│   │
│   ├── experiment5_packet_size/
│   │   ├── Ieee802154Showcase.ned
│   │   ├── omnetpp.ini
│   │   └── results/
│   │
│   └── smart_home_v1/
│
└── OMNeT++ project configuration files
Result Files

Processed simulation results are included as CSV files.

Examples:

experiment1_runs.csv
experiment1_summary.csv

experiment2_runs.csv
experiment2_summary.csv

experiment3_critical_raw.csv
experiment3_summary.csv

experiment4_rr_raw.csv
experiment4_pub_raw.csv
experiment4_summary.csv

experiment5_raw.csv
experiment5_summary.csv

Final plots used in the analysis are also included in the corresponding results/ directories.

Raw OMNeT++ .sca, .vec, and .vci files are excluded from Git because they can be regenerated from the simulation configurations.

Reproducibility
Required Software

The project was developed and tested with:

OMNeT++ 6.3.0
INET Framework 4.6.0

The project should be executed inside an OMNeT++ environment where INET 4.6.0 is available.

The simulations contain their corresponding:

.ned
.ini
.xml

configuration files.

The main experiment configurations are located in each experiment directory.

For example:

simulations/experiment1_scalability/omnetpp.ini
simulations/experiment2_reporting_interval/omnetpp.ini
simulations/experiment3_critical_event/omnetpp.ini
simulations/experiment4_application_strategy/omnetpp.ini
simulations/experiment5_packet_size/omnetpp.ini

Experiment 3 includes configurations for:

Critical_N5
Critical_N10
Critical_N20
Critical_N30
Critical_N40

Experiment 4 includes request/response configurations:

RR_T1
RR_T5
RR_T10
RR_T30
RR_T60

and publish/subscribe-like configurations:

PUB_T1
PUB_T5
PUB_T10
PUB_T30
PUB_T60

Processed results were exported from OMNeT++ statistical outputs using opp_scavetool and further processed using Python scripts.

Key Findings

The main engineering conclusions from the project are:

The IEEE 802.15.4 smart-home network maintained 100% PDR up to 40 active nodes under the tested baseline workload.
Increasing the reporting interval strongly reduced total energy consumption.
Critical smoke-alarm traffic maintained 100% delivery and remained well below the 100 ms project latency target.
Publish/subscribe-like communication reduced application-level traffic by 50% compared with request/response polling for the same update interval.
Increasing packet size increased delay and energy cost and increased fragmentation pressure on constrained IEEE 802.15.4 links.
Application traffic policy and packet size are important design factors in constrained IoT networks.
Limitations

The results should be interpreted within the following model boundaries:

IPv4/UDP is used in the implemented simulation.
Full IPv6/6LoWPAN adaptation-layer behavior is not simulated.
6LoWPAN fragmentation results are analytical approximations.
The constrained part of the topology contains one IEEE 802.15.4 wireless access hop before the wired core.
Energy results depend on the INET radio and energy models used in the simulation.
Five random seeds are used for the main comparisons and do not represent every possible wireless condition.
References
ENCS5325 Project Specification, Smart-Home IoT Network Design and Performance Evaluation Using OMNeT++, Summer 2026.
INET IEEE 802.15.4 Smart Home Showcase
https://inet.omnetpp.org/docs/showcases/wireless/ieee802154/doc/
OMNeT++ Documentation
https://docs.omnetpp.org/
INET Framework Documentation
https://doc.omnetpp.org/inet/api-current/neddoc/
INET IEEE 802.15.4 User Guide
https://inet.omnetpp.org/docs/users-guide/ch-802154.html
INET Power Consumption Modeling
https://inet.omnetpp.org/docs/users-guide/ch-power.html
INET Applications
https://inet.omnetpp.org/docs/users-guide/ch-apps.html
INET UdpEchoApp
https://doc.omnetpp.org/inet/api-current/neddoc/inet.applications.udpapp.UdpEchoApp.html
IETF RFC 4944 - Transmission of IPv6 Packets over IEEE 802.15.4 Networks
https://www.rfc-editor.org/rfc/rfc4944.html
IETF RFC 6282 - Compression Format for IPv6 Datagrams over IEEE 802.15.4-Based Networks
https://www.rfc-editor.org/rfc/rfc6282.html
Course

ENCS5325 - Wireless Sensor Networks and Internet of Things
Electrical and Computer Engineering
Birzeit University
Summer 2026
EOF
