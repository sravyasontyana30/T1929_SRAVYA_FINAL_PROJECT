import threading
import time
import random
from garage_monitor import GarageMonitor

class ThreadSafeGarageMonitor(GarageMonitor):
    """
    Extends GarageMonitor with a threading.Lock for safe concurrent updates.
    """
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()

    def add_diagnostic(self, car_id, diag_type, value):
        with self.lock:
            super().add_diagnostic(car_id, diag_type, value)

    def get_car_statuses(self):
        with self.lock:
            return super().get_car_statuses()

def simulate_updates(monitor, car_id, updates, delay=0.01):
    for diag_type, value in updates:
        monitor.add_diagnostic(car_id, diag_type, value)
        time.sleep(delay)

def run_simulation(threaded=True, num_cars=5, num_updates=100):
    monitor = ThreadSafeGarageMonitor() if threaded else GarageMonitor()
    cars = [f"Car{i+1}" for i in range(num_cars)]
    diag_types = ["RPM", "EngineLoad", "CoolantTemp"]
    threads = []
    start = time.time()
    for car_id in cars:
        updates = [(random.choice(diag_types), random.uniform(1000, 7000)) for _ in range(num_updates)]
        if threaded:
            t = threading.Thread(target=simulate_updates, args=(monitor, car_id, updates))
            threads.append(t)
            t.start()
        else:
            simulate_updates(monitor, car_id, updates, delay=0)
    if threaded:
        for t in threads:
            t.join()
    elapsed = time.time() - start
    return elapsed, monitor.get_car_statuses()

def main():
    print("Running single-threaded simulation...")
    single_time, single_status = run_simulation(threaded=False)
    print(f"Single-threaded time: {single_time:.4f} seconds")
    print("Running multi-threaded simulation...")
    multi_time, multi_status = run_simulation(threaded=True)
    print(f"Multi-threaded time: {multi_time:.4f} seconds")
    print("\nSample car status (multi-threaded):")
    for car_id, status in list(multi_status.items())[:2]:
        print(f"{car_id}: {status}")

if __name__ == "__main__":
    main()
