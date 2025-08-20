import sys
from garage_monitor import GarageMonitor
from diagnostic import Diagnostic

def parse_csv_line(line):
    parts = [p.strip() for p in line.strip().split(",")]
    if len(parts) != 3:
        return None
    car_id, diag_type, value = parts
    if diag_type not in Diagnostic.VALID_TYPES:
        return None
    try:
        value = float(value)
    except ValueError:
        return None
    return car_id, diag_type, value

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <diagnostics.csv>")
        return
    filename = sys.argv[1]
    monitor = GarageMonitor()
    with open(filename) as f:
        for line in f:
            if not line.strip():
                continue
            parsed = parse_csv_line(line)
            if parsed is None:
                print(f"Malformed line skipped: {line.strip()}")
                continue
            car_id, diag_type, value = parsed
            monitor.add_diagnostic(car_id, diag_type, value)
    statuses = monitor.get_car_statuses()
    for car_id, status in statuses.items():
        print(f"Car: {car_id}")
        if status["score"] is None:
            print("  Performance Score: INVALID")
        else:
            print(f"  Performance Score: {status['score']:.2f}")
        if status["alert"]:
            print(f"  ALERT: {status['alert']}")
        print(f"  Diagnostics: {status['diagnostics']}")

if __name__ == "__main__":
    main()
