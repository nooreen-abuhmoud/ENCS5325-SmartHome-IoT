import glob
import re
import csv
import statistics
from pathlib import Path

RESULTS = Path("results")
SIM_TIME = 100.0          # seconds
PAYLOAD_BYTES = 50        # fixed in Experiment 1

runs = []

for path in sorted(RESULTS.glob("Scalability_N*-#*.sca")):
    m = re.search(r"Scalability_N(\d+)-#(\d+)\.sca$", path.name)
    if not m:
        continue

    N = int(m.group(1))
    seed = int(m.group(2))

    sent = 0
    received = None
    delay_mean_s = None

    sensor_energy_j = 0.0
    gateway_energy_j = 0.0

    lines = path.read_text(errors="ignore").splitlines()

    i = 0
    while i < len(lines):
        line = lines[i]

        # Packets sent by active sensor applications
        ms = re.match(
            r"scalar ScalabilityNetwork\.sensor\[\d+\]\.app\[0\] packetSent:count ([\d.eE+-]+)",
            line
        )
        if ms:
            sent += int(float(ms.group(1)))

        # Packets received by monitoring server
        mr = re.match(
            r"scalar ScalabilityNetwork\.monitoringServer\.app\[0\] packetReceived:count ([\d.eE+-]+)",
            line
        )
        if mr:
            received = int(float(mr.group(1)))

        # Mean end-to-end delay
        if line.startswith(
            "statistic ScalabilityNetwork.monitoringServer.app[0] endToEndDelay:stats"
        ):
            j = i + 1
            while j < len(lines) and not lines[j].startswith(("statistic ", "scalar ", "par ")):
                if lines[j].startswith("field mean "):
                    delay_mean_s = float(lines[j].split()[-1])
                    break
                j += 1

        # Active sensor energy consumption
        me = re.match(
            r"scalar ScalabilityNetwork\.sensor\[\d+\]\.energyStorage residualEnergyCapacity:last ([\d.eE+-]+)",
            line
        )
        if me:
            # IdealEpEnergyStorage starts at 0 and decreases
            sensor_energy_j += -float(me.group(1))

        # Gateway energy consumption
        mg = re.match(
            r"scalar ScalabilityNetwork\.controller\.energyStorage residualEnergyCapacity:last ([\d.eE+-]+)",
            line
        )
        if mg:
            gateway_energy_j = -float(mg.group(1))

        i += 1

    received = received or 0

    pdr = (received / sent * 100.0) if sent else 0.0
    lost = sent - received
    loss_pct = (lost / sent * 100.0) if sent else 0.0

    delay_ms = delay_mean_s * 1000.0 if delay_mean_s is not None else float("nan")

    # Average application throughput over whole simulation
    throughput_bps = received * PAYLOAD_BYTES * 8 / SIM_TIME

    total_energy_j = sensor_energy_j + gateway_energy_j
    energy_per_packet_mj = (
        total_energy_j / received * 1000.0 if received else float("nan")
    )

    runs.append({
        "N": N,
        "Seed": seed,
        "Sent": sent,
        "Received": received,
        "Lost": lost,
        "PDR_percent": pdr,
        "Loss_percent": loss_pct,
        "Mean_Delay_ms": delay_ms,
        "Throughput_bps": throughput_bps,
        "Sensor_Energy_J": sensor_energy_j,
        "Gateway_Energy_J": gateway_energy_j,
        "Energy_per_packet_mJ": energy_per_packet_mj,
    })

# Save all 25 runs
run_csv = RESULTS / "experiment1_runs.csv"
with run_csv.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=runs[0].keys())
    writer.writeheader()
    writer.writerows(runs)

# Aggregate five seeds for each N
summary = []

def mean(xs):
    return statistics.mean(xs)

def sd(xs):
    return statistics.stdev(xs) if len(xs) > 1 else 0.0

for N in sorted(set(r["N"] for r in runs)):
    group = [r for r in runs if r["N"] == N]

    pdrs = [r["PDR_percent"] for r in group]
    losses = [r["Loss_percent"] for r in group]
    delays = [r["Mean_Delay_ms"] for r in group]
    throughputs = [r["Throughput_bps"] for r in group]
    energies = [r["Energy_per_packet_mJ"] for r in group]

    row = {
        "N": N,
        "Runs": len(group),
        "PDR_mean_percent": mean(pdrs),
        "PDR_std": sd(pdrs),
        "Loss_mean_percent": mean(losses),
        "Loss_std": sd(losses),
        "Delay_mean_ms": mean(delays),
        "Delay_std_ms": sd(delays),
        "Throughput_mean_bps": mean(throughputs),
        "Throughput_std_bps": sd(throughputs),
        "Energy_per_packet_mean_mJ": mean(energies),
        "Energy_per_packet_std_mJ": sd(energies),
    }
    summary.append(row)

summary_csv = RESULTS / "experiment1_summary.csv"
with summary_csv.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=summary[0].keys())
    writer.writeheader()
    writer.writerows(summary)

print()
print("========== Experiment 1 Summary ==========")
print(
    f"{'N':>4} {'PDR %':>10} {'Loss %':>10} "
    f"{'Delay ms':>12} {'Throughput':>14} {'Energy/pkt':>14}"
)

for r in summary:
    print(
        f"{r['N']:>4} "
        f"{r['PDR_mean_percent']:>9.3f} "
        f"{r['Loss_mean_percent']:>9.3f} "
        f"{r['Delay_mean_ms']:>11.3f} "
        f"{r['Throughput_mean_bps']:>12.2f} "
        f"{r['Energy_per_packet_mean_mJ']:>12.3f}"
    )

print()
print("Created:")
print(run_csv)
print(summary_csv)
