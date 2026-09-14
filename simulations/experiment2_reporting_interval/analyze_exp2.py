import re
import csv
import statistics
from pathlib import Path

RESULTS = Path("results")
SIM_TIME = 600.0
PAYLOAD_BYTES = 50

runs = []

for path in RESULTS.glob("Reporting_T*-#*.sca"):
    m = re.search(r"Reporting_T(\d+)-#(\d+)\.sca$", path.name)
    if not m:
        continue

    T = int(m.group(1))
    seed = int(m.group(2))

    sent = 0
    received = 0
    delay_mean_s = None

    sensor_energy_j = 0.0
    gateway_energy_j = 0.0

    lines = path.read_text(errors="ignore").splitlines()

    i = 0
    while i < len(lines):
        line = lines[i]

        # Packets sent by the 12 active sensors
        ms = re.match(
            r"scalar ReportingIntervalNetwork\.sensor\[\d+\]\.app\[0\] packetSent:count ([\d.eE+-]+)",
            line
        )
        if ms:
            sent += int(float(ms.group(1)))

        # Packets received at monitoring server
        mr = re.match(
            r"scalar ReportingIntervalNetwork\.monitoringServer\.app\[0\] packetReceived:count ([\d.eE+-]+)",
            line
        )
        if mr:
            received = int(float(mr.group(1)))

        # Mean end-to-end delay
        if line.startswith(
            "statistic ReportingIntervalNetwork.monitoringServer.app[0] endToEndDelay:stats"
        ):
            j = i + 1
            while j < len(lines) and not lines[j].startswith(
                ("statistic ", "scalar ", "par ")
            ):
                if lines[j].startswith("field mean "):
                    delay_mean_s = float(lines[j].split()[-1])
                    break
                j += 1

        # Sensor energy
        me = re.match(
            r"scalar ReportingIntervalNetwork\.sensor\[\d+\]\.energyStorage residualEnergyCapacity:last ([\d.eE+-]+)",
            line
        )
        if me:
            sensor_energy_j += -float(me.group(1))

        # Gateway energy
        mg = re.match(
            r"scalar ReportingIntervalNetwork\.controller\.energyStorage residualEnergyCapacity:last ([\d.eE+-]+)",
            line
        )
        if mg:
            gateway_energy_j = -float(mg.group(1))

        i += 1

    lost = sent - received
    pdr = received / sent * 100 if sent else 0
    loss_pct = lost / sent * 100 if sent else 0

    delay_ms = delay_mean_s * 1000 if delay_mean_s is not None else float("nan")

    throughput_bps = received * PAYLOAD_BYTES * 8 / SIM_TIME

    total_energy_j = sensor_energy_j + gateway_energy_j

    energy_per_packet_mj = (
        total_energy_j / received * 1000
        if received else float("nan")
    )

    runs.append({
        "T_s": T,
        "Seed": seed,
        "Sent": sent,
        "Received": received,
        "Lost": lost,
        "PDR_percent": pdr,
        "Loss_percent": loss_pct,
        "Mean_Delay_ms": delay_ms,
        "Throughput_bps": throughput_bps,
        "Total_Energy_J": total_energy_j,
        "Energy_per_packet_mJ": energy_per_packet_mj,
    })

runs.sort(key=lambda x: (x["T_s"], x["Seed"]))

# Save all 25 runs
runs_csv = RESULTS / "experiment2_runs.csv"
with runs_csv.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=runs[0].keys())
    writer.writeheader()
    writer.writerows(runs)

def mean(values):
    return statistics.mean(values)

def sd(values):
    return statistics.stdev(values) if len(values) > 1 else 0.0

summary = []

for T in sorted(set(r["T_s"] for r in runs)):
    group = [r for r in runs if r["T_s"] == T]

    row = {
        "T_s": T,
        "Runs": len(group),

        "PDR_mean_percent": mean([r["PDR_percent"] for r in group]),
        "PDR_std": sd([r["PDR_percent"] for r in group]),

        "Loss_mean_percent": mean([r["Loss_percent"] for r in group]),
        "Loss_std": sd([r["Loss_percent"] for r in group]),

        "Delay_mean_ms": mean([r["Mean_Delay_ms"] for r in group]),
        "Delay_std_ms": sd([r["Mean_Delay_ms"] for r in group]),

        "Throughput_mean_bps": mean([r["Throughput_bps"] for r in group]),
        "Throughput_std_bps": sd([r["Throughput_bps"] for r in group]),

        "Total_Energy_mean_J": mean([r["Total_Energy_J"] for r in group]),
        "Total_Energy_std_J": sd([r["Total_Energy_J"] for r in group]),

        "Energy_per_packet_mean_mJ": mean(
            [r["Energy_per_packet_mJ"] for r in group]
        ),
        "Energy_per_packet_std_mJ": sd(
            [r["Energy_per_packet_mJ"] for r in group]
        ),
    }

    summary.append(row)

summary_csv = RESULTS / "experiment2_summary.csv"
with summary_csv.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=summary[0].keys())
    writer.writeheader()
    writer.writerows(summary)

print()
print("============= Experiment 2 Summary =============")
print(
    f"{'T(s)':>6} "
    f"{'PDR %':>9} "
    f"{'Loss %':>9} "
    f"{'Delay ms':>11} "
    f"{'Energy J':>11} "
    f"{'Energy/pkt':>13}"
)

for r in summary:
    print(
        f"{r['T_s']:>6} "
        f"{r['PDR_mean_percent']:>9.3f} "
        f"{r['Loss_mean_percent']:>9.3f} "
        f"{r['Delay_mean_ms']:>11.3f} "
        f"{r['Total_Energy_mean_J']:>11.4f} "
        f"{r['Energy_per_packet_mean_mJ']:>13.3f}"
    )

print()
print("Created:")
print(runs_csv)
print(summary_csv)
