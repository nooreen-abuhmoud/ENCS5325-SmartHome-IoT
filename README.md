
# ENCS5325 Smart-Home IoT Network

**Smart-Home IoT Network Design and Performance Evaluation Using OMNeT++**

Course: **ENCS5325 - Wireless Sensor Networks and Internet of Things**  
Electrical and Computer Engineering - Birzeit University  
Summer 2026

## Project Overview

This project evaluates the performance of a smart-home IoT network using **OMNeT++ 6.3.0** and **INET 4.6.0**.

The study investigates how the following factors affect network performance:

- Number of active IoT devices
- Sensor reporting interval
- Background traffic load
- Critical event traffic
- Application communication strategy
- Application payload size
- IEEE 802.15.4 / 6LoWPAN fragmentation pressure

The main performance metrics are:

- Packet Delivery Ratio (PDR)
- Packet loss
- End-to-end delay
- Throughput
- Energy consumption
- Energy per delivered packet

---

## Simulation Environment

| Item | Configuration |
|---|---|
| Simulator | OMNeT++ 6.3.0 |
| Framework | INET 4.6.0 |
| Wireless access | IEEE 802.15.4 |
| Transport protocol | UDP |
| Simulated network layer | IPv4 |
| Core connection | PPP/IP |
| Main repetitions | 5 independent seeds |

---

## Network Architecture

The smart-home devices communicate over the constrained IEEE 802.15.4 access network through an IoT gateway to a core-side monitoring server.

```text
Smart-Home Sensors / Actuators
              |
      IEEE 802.15.4
              |
          IoT Gateway
              |
          PPP / IP
              |
      Monitoring Server
```

Two traffic classes are evaluated:

1. **Periodic monitoring traffic** for normal sensor measurements.
2. **Event-driven critical traffic** representing an urgent smoke alarm.

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
```

A complete **IPv6/6LoWPAN adaptation layer is not simulated**.

The packet-size study therefore separates:

- **Simulator-derived results** from the OMNeT++/INET IPv4/UDP model.
- **Analytical 6LoWPAN fragmentation estimates** based on RFC 4944 and RFC 6282.

The reported FRAG1/FRAGN-style fragment counts are analytical approximations and are not claimed as simulator-generated traces.

---

# Experiments

## Experiment 1 - Network Scalability

The number of active periodic-reporting sensors is varied while payload size and reporting interval remain fixed.

**Parameters**

- Active nodes: `5, 10, 20, 30, 40`
- Payload: `50 B`
- Reporting interval: `10 s`
- Duration: `100 s`
- Repetitions: `5 per network size`

**Main result**

PDR remained **100%** for all tested network sizes.

Mean end-to-end delay increased only slightly:

- `5.365 ms` at N = 5
- `5.565 ms` at N = 40

No significant congestion was observed up to 40 active sensors under the tested baseline workload.

Results: [`simulations/experiment1_scalability/results/`](simulations/experiment1_scalability/results/)

---

## Experiment 2 - Reporting Interval and Energy Trade-off

The reporting interval is varied to study the trade-off between data freshness and energy consumption.

**Parameters**

- Active nodes: `12`
- Payload: `50 B`
- Reporting interval: `1, 5, 10, 30, 60 s`
- Duration: `600 s`
- Repetitions: `5 per interval`

**Main result**

Mean total energy consumption decreased from:

- `16.1473 J` at T = 1 s
- to `0.3055 J` at T = 60 s

This corresponds to approximately a **98.1% reduction in total energy consumption**.

Reliability remained almost perfect throughout the sweep.

Results: [`simulations/experiment2_reporting_interval/results/`](simulations/experiment2_reporting_interval/results/)

---

## Experiment 3 - Critical Event Under Background Traffic

A critical smoke alarm is generated while ordinary sensors continue producing periodic background traffic.

**Parameters**

- Background-load levels: `N = 5, 10, 20, 30, 40`
- Background payload: `50 B`
- Background interval: `10 s`
- Critical payload: `20 B`
- Critical event time: `50 s`
- Duration: `100 s`
- Repetitions: `5 per load level`

The project-defined critical-event latency requirement is:

```text
End-to-end critical-event latency < 100 ms
```

**Main result**

- Critical delivery: **100%**
- Critical loss: **0%**
- Maximum observed critical-event delay: approximately **5.58 ms**

All completed runs satisfied the 100 ms latency requirement.

Results: [`simulations/experiment3_critical_event/results/`](simulations/experiment3_critical_event/results/)

---

## Experiment 4 - Application Communication Strategy

Two application communication strategies are compared on the same smart-home topology.

### Request/Response

The monitoring server polls each sensor and receives a response.

```text
Monitoring Server
       |
    Request
       v
     Sensor
       |
    Response
       v
Monitoring Server
```

This provides **CoAP-like request/response behavior**.

### Publish/Subscribe-Like

Sensors publish updates directly to a subscriber at the monitoring server.

```text
Sensor
   |
Publication
   v
Monitoring Server
```

This provides **MQTT-like publish/subscribe traffic behavior** at the application level.

**Parameters**

- Active sensors: `12`
- Payload: `50 B`
- Interval: `1, 5, 10, 30, 60 s`
- Duration: `600 s`
- Repetitions: `5 per strategy and interval`

**Main result**

At T = 1 s:

| Strategy | Application packets/run |
|---|---:|
| Request/Response | 14,376 |
| Publish/Subscribe-like | 7,188 |

Request/response generated twice as many application packets.

Therefore, publish/subscribe-like communication reduced application-level packet traffic by approximately **50%** for the same update interval.

Request/response latency is measured as **round-trip time (RTT)**, whereas publication latency is a **one-way delay**, so the two latency values are not directly equivalent.

Results: [`simulations/experiment4_application_strategy/results/`](simulations/experiment4_application_strategy/results/)

---

## Experiment 5 - Packet Size Study

The application payload size is varied to study its effect on reliability, delay, throughput, and energy consumption.

**Simulated payloads**

```text
20, 50, 80, 100, 150, 250, 500 B
```

**Parameters**

- Active sensors: `12`
- Reporting interval: `10 s`
- Duration: `600 s`
- Repetitions: `5 per payload`

**Main result**

Mean end-to-end delay increased from approximately:

- `4.443 ms` at 20 B
- to `36.691 ms` at 500 B

PDR remained **100% through 250 B** and decreased slightly to approximately **99.639% at 500 B**.

Energy per delivered packet also increased substantially with increasing payload size.

Results: [`simulations/experiment5_packet_size/results/`](simulations/experiment5_packet_size/results/)

---

# Analytical 6LoWPAN Fragmentation Study

The assignment-required payload sizes were also analyzed using IEEE 802.15.4 and 6LoWPAN fragmentation assumptions.

| Application Payload | Estimated Fragments |
|---:|---:|
| 20 B | 1 |
| 50 B | 1 |
| 100 B | 2 |
| 200 B | 3 |
| 400 B | 6 |

Increasing the number of fragments increases:

- Link-layer transmissions
- Wireless airtime
- Delay
- Energy consumption
- Exposure to retransmissions
- Probability that at least one fragment requires retransmission

These fragment counts are **analytical estimates**, not direct OMNeT++ measurements.

---

# Repository Structure

```text
ENCS5325-SmartHome-IoT/
|
├── simulations/
│   ├── baseline/
│   ├── smart_home_v1/
│   ├── experiment1_scalability/
│   ├── experiment2_reporting_interval/
│   ├── experiment3_critical_event/
│   ├── experiment4_application_strategy/
│   └── experiment5_packet_size/
|
├── ENCS5325_SmartHome_IoT_Presentation.pptx
├── Makefile
├── README.md
└── OMNeT++ project configuration files
```

Each experiment directory contains its corresponding `.ned`, `omnetpp.ini`, topology/configuration files, and processed results.

---

# Data and Results

Processed CSV results and final plots are included in the corresponding experiment directories.

Examples include:

```text
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
```

Raw OMNeT++ `.sca`, `.vec`, and `.vci` files are excluded from Git because they are generated simulation outputs and can be regenerated from the experiment configurations.

---

# Reproducibility

The project was developed using:

```text
OMNeT++ 6.3.0
INET Framework 4.6.0
```

Each experiment has its own `omnetpp.ini` configuration.

Experiment 3 includes configurations for different critical-event background loads.

Experiment 4 includes configurations for both communication strategies and all tested intervals.

Simulation statistics were exported using **opp_scavetool**, and processed results and figures were generated using Python-based analysis where applicable.

---

# Key Findings

1. The network maintained **100% PDR up to 40 active sensors** under the tested baseline workload.

2. Increasing the reporting interval from 1 s to 60 s reduced total energy consumption by approximately **98.1%**.

3. Critical smoke-alarm traffic achieved **100% delivery**, and the maximum observed delay remained far below the 100 ms project target.

4. Publish/subscribe-like communication reduced application-level packet traffic by approximately **50%** compared with request/response polling for the same interval.

5. Larger payloads increased end-to-end delay and energy consumption.

6. Analytical 6LoWPAN results show that larger payloads require more link-layer fragments, increasing airtime, energy cost, and retransmission exposure.

---

# Limitations

The results should be interpreted within the following model boundaries:

- The implemented end-to-end simulation uses IPv4/UDP.
- A complete IPv6/6LoWPAN adaptation layer is not simulated.
- 6LoWPAN fragmentation results are analytical approximations.
- The constrained side contains one IEEE 802.15.4 wireless access hop before the wired core.
- Energy results depend on the selected INET energy and radio models.
- Five independent repetitions provide statistical variation but do not represent every possible wireless condition.

---

# References

1. INET IEEE 802.15.4 Smart Home Showcase  
   https://inet.omnetpp.org/docs/showcases/wireless/ieee802154/doc/

2. OMNeT++ Documentation  
   https://docs.omnetpp.org/

3. INET Framework Documentation  
   https://doc.omnetpp.org/inet/api-current/neddoc/

4. INET IEEE 802.15.4 User Guide  
   https://inet.omnetpp.org/docs/users-guide/ch-802154.html

5. INET Power Consumption Modeling  
   https://inet.omnetpp.org/docs/users-guide/ch-power.html

6. IETF RFC 4944 - IPv6 over IEEE 802.15.4  
   https://www.rfc-editor.org/rfc/rfc4944.html

7. IETF RFC 6282 - IPv6 Header Compression for 6LoWPAN  
   https://www.rfc-editor.org/rfc/rfc6282.html

---

## Course Information

**ENCS5325 - Wireless Sensor Networks and Internet of Things**  
Electrical and Computer Engineering  
Birzeit University  
Summer 2026
