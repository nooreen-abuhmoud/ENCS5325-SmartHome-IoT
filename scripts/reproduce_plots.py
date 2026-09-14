import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reproduced_plots"
OUT.mkdir(exist_ok=True)


def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def numbers(rows, key):
    return [float(r[key]) for r in rows]


def finish(filename, xlabel, ylabel, title):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=200)
    plt.close()


# ============================================================
# Experiment 1 - Scalability
# ============================================================

p = ROOT / "simulations/experiment1_scalability/results/experiment1_summary.csv"
d = read_csv(p)

x = numbers(d, "N")

plt.figure()
plt.plot(x, numbers(d, "PDR_mean_percent"), marker="o", label="PDR")
plt.plot(x, numbers(d, "Loss_mean_percent"), marker="s", label="Loss")
plt.legend()
finish("exp1_pdr_loss.png", "Active sensors (N)", "Percent (%)",
       "Experiment 1: PDR and Packet Loss")

plt.figure()
plt.errorbar(
    x,
    numbers(d, "Delay_mean_ms"),
    yerr=numbers(d, "Delay_std_ms"),
    marker="o",
    capsize=4
)
finish("exp1_delay.png", "Active sensors (N)", "Delay (ms)",
       "Experiment 1: End-to-End Delay")

plt.figure()
plt.plot(x, numbers(d, "Throughput_mean_bps"), marker="o")
finish("exp1_throughput.png", "Active sensors (N)", "Throughput (bps)",
       "Experiment 1: Application Throughput")

plt.figure()
plt.errorbar(
    x,
    numbers(d, "Energy_per_packet_mean_mJ"),
    yerr=numbers(d, "Energy_per_packet_std_mJ"),
    marker="o",
    capsize=4
)
finish("exp1_energy_per_packet.png", "Active sensors (N)",
       "Energy per delivered packet (mJ)",
       "Experiment 1: Energy per Delivered Packet")


# ============================================================
# Experiment 2 - Reporting Interval
# ============================================================

p = ROOT / "simulations/experiment2_reporting_interval/results/experiment2_summary.csv"
d = read_csv(p)

x = numbers(d, "T_s")

plt.figure()
plt.errorbar(
    x,
    numbers(d, "PDR_mean_percent"),
    yerr=numbers(d, "PDR_std"),
    marker="o",
    capsize=4
)
plt.ylim(99.98, 100.005)
finish("exp2_pdr.png", "Reporting interval T (s)", "PDR (%)",
       "Experiment 2: PDR vs Reporting Interval")

plt.figure()
plt.errorbar(
    x,
    numbers(d, "Delay_mean_ms"),
    yerr=numbers(d, "Delay_std_ms"),
    marker="o",
    capsize=4
)
finish("exp2_delay.png", "Reporting interval T (s)", "Delay (ms)",
       "Experiment 2: End-to-End Delay")

plt.figure()
plt.plot(x, numbers(d, "Total_Energy_mean_J"), marker="o")
finish("exp2_total_energy.png", "Reporting interval T (s)",
       "Total energy (J)",
       "Experiment 2: Total Energy Consumption")

plt.figure()
plt.errorbar(
    x,
    numbers(d, "Energy_per_packet_mean_mJ"),
    yerr=numbers(d, "Energy_per_packet_std_mJ"),
    marker="o",
    capsize=4
)
finish("exp2_energy_per_packet.png", "Reporting interval T (s)",
       "Energy per packet (mJ)",
       "Experiment 2: Energy per Delivered Packet")


# ============================================================
# Experiment 3 - Critical Event
# ============================================================

p = ROOT / "simulations/experiment3_critical_event/results/experiment3_summary.csv"
d = read_csv(p)

x = numbers(d, "Sensors")

plt.figure()
plt.errorbar(
    x,
    numbers(d, "Delay_mean_ms"),
    yerr=numbers(d, "Delay_std_ms"),
    marker="o",
    capsize=4,
    label="Mean ± SD"
)
plt.plot(
    x,
    numbers(d, "Delay_max_ms"),
    marker="s",
    linestyle="--",
    label="Maximum"
)
plt.legend()
finish("exp3_critical_delay.png", "Background active sensors (N)",
       "Critical-event delay (ms)",
       "Experiment 3: Critical-Event Delay")


# ============================================================
# Experiment 4 - Application Strategy
# ============================================================

p = ROOT / "simulations/experiment4_application_strategy/results/experiment4_summary.csv"
d = read_csv(p)

x = numbers(d, "T_s")

plt.figure()
plt.errorbar(
    x,
    numbers(d, "RR_RTT_mean_ms"),
    yerr=numbers(d, "RR_RTT_std_ms"),
    marker="o",
    capsize=4,
    label="Request/Response RTT"
)
plt.errorbar(
    x,
    numbers(d, "PUB_Delay_mean_ms"),
    yerr=numbers(d, "PUB_Delay_std_ms"),
    marker="s",
    capsize=4,
    label="Publish one-way delay"
)
plt.legend()
finish("exp4_latency_comparison.png", "Interval T (s)",
       "Application-visible latency (ms)",
       "Experiment 4: Application Strategy Latency")

plt.figure()
plt.plot(
    x,
    numbers(d, "RR_AppPackets_mean"),
    marker="o",
    label="Request/Response"
)
plt.plot(
    x,
    numbers(d, "PUB_AppPackets_mean"),
    marker="s",
    label="Publish/Subscribe-like"
)
plt.legend()
finish("exp4_traffic_cost.png", "Interval T (s)",
       "Application packets per run",
       "Experiment 4: Application-Level Traffic Cost")


# ============================================================
# Experiment 5 - Packet Size
# ============================================================

p = ROOT / "simulations/experiment5_packet_size/results/experiment5_summary.csv"
d = read_csv(p)

x = numbers(d, "Payload_B")

plt.figure()
plt.errorbar(
    x,
    numbers(d, "Delay_mean_ms"),
    yerr=numbers(d, "Delay_std_ms"),
    marker="o",
    capsize=4,
    label="Mean ± SD"
)
plt.plot(
    x,
    numbers(d, "Delay_max_observed_ms"),
    marker="s",
    linestyle="--",
    label="Maximum"
)
plt.legend()
finish("exp5_delay.png", "Application payload (B)", "Delay (ms)",
       "Experiment 5: Payload Size vs Delay")

plt.figure()
plt.errorbar(
    x,
    numbers(d, "PDR_mean_percent"),
    yerr=numbers(d, "PDR_std"),
    marker="o",
    capsize=4
)
finish("exp5_pdr.png", "Application payload (B)", "PDR (%)",
       "Experiment 5: Payload Size vs PDR")

plt.figure()
plt.errorbar(
    x,
    numbers(d, "Energy_per_packet_mean_mJ"),
    yerr=numbers(d, "Energy_per_packet_std_mJ"),
    marker="o",
    capsize=4
)
finish("exp5_energy_per_packet.png", "Application payload (B)",
       "Energy per packet (mJ)",
       "Experiment 5: Payload Size vs Energy")

plt.figure()
plt.errorbar(
    x,
    numbers(d, "Throughput_mean_bps"),
    yerr=numbers(d, "Throughput_std_bps"),
    marker="o",
    capsize=4
)
finish("exp5_throughput.png", "Application payload (B)",
       "Throughput (bps)",
       "Experiment 5: Payload Size vs Throughput")


print(f"Plots generated successfully in: {OUT}")
