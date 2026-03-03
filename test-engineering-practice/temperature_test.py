import csv
import os
import random
from datetime import datetime

MIN_OK = 49.5
MAX_OK = 52.0
DURATION_MINUTES = 60
INTERVAL_MINUTES = 1

def simulate_temperature(minute: int) -> float:
    """
    Simulate a temperature reading.
    Mostly stays around 50, but sometimes drifts.
    """
    base = 50.0
    noise = random.uniform(-1.5, 1.5)          # normal noise
    occasional_drift = 0.0

    # every ~15 minutes, add a small drift chance
    if minute % 15 == 0 and minute != 0:
        occasional_drift = random.uniform(-2.0, 2.0)

    return base + noise + occasional_drift

def ensure_logs_dir() -> str:
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    return logs_dir

def run_test() -> int:
    logs_dir = ensure_logs_dir()
    log_path = os.path.join(logs_dir, "temperature_log.csv")

    readings = []
    now = datetime.now().isoformat(timespec="seconds")

    with open(log_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["run_started_at", now])
        writer.writerow(["minute", "temperature_c", "in_range"])

        for minute in range(0, DURATION_MINUTES, INTERVAL_MINUTES):
            temp = round(simulate_temperature(minute), 2)
            in_range = MIN_OK <= temp <= MAX_OK
            readings.append((minute, temp, in_range))
            writer.writerow([minute, temp, in_range])

    temps = [t for _, t, _ in readings]
    out_of_range = [(m, t) for m, t, ok in readings if not ok]

    min_temp = min(temps)
    max_temp = max(temps)

    passed = (len(out_of_range) == 0)

    print("=== Temperature Stability Test Summary ===")
    print(f"Log file: {log_path}")
    print(f"Duration: {DURATION_MINUTES} minutes, Interval: {INTERVAL_MINUTES} minute")
    print(f"Allowed range: {MIN_OK}°C .. {MAX_OK}°C")
    print(f"Min observed: {min_temp}°C")
    print(f"Max observed: {max_temp}°C")
    print(f"Out-of-range count: {len(out_of_range)}")
    print(f"RESULT: {'PASS ✅' if passed else 'FAIL ❌'}")

    # return code: 0 = pass, 1 = fail (useful for CI later)
    return 0 if passed else 1

if __name__ == "__main__":

    raise SystemExit(run_test())
