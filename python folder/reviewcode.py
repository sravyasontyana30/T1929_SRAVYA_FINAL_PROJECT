
import csv

class Diagnostic:
    VALID_TYPES = {"RPM", "EngineLoad", "CoolantTemp"}

    def __init__(self, diag_type, value):
        if diag_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid diagnostic type: {diag_type}")
        if not isinstance(value, (int, float)):
            raise ValueError("Diagnostic value must be numeric")
        self.type = diag_type
        self.value = value

class Car:
    SEVERE_STRESS_THRESHOLD = 40

    def __init__(self, car_id):
        self.car_id = car_id
        self.diagnostics = {}

    def update_diagnostic(self, diag_type, value):
        self.diagnostics[diag_type] = Diagnostic(diag_type, value)

    def has_all_diagnostics(self):
        return all(t in self.diagnostics for t in Diagnostic.VALID_TYPES)

    def get_performance_score(self):
        try:
            rpm = self.diagnostics["RPM"].value
            engine_load = self.diagnostics["EngineLoad"].value
            coolant_temp = self.diagnostics["CoolantTemp"].value
        except KeyError:
            return None
        score = 100 - (rpm/100 + engine_load*0.5 + (coolant_temp-90)*2)
        return score

class GarageMonitor:
    def __init__(self):
        self.cars = {}

    def add_diagnostic(self, car_id, diag_type, value):
        if car_id not in self.cars:
            self.cars[car_id] = Car(car_id)
        self.cars[car_id].update_diagnostic(diag_type, value)

    def get_car_statuses(self):
        statuses = {}
        for car_id, car in self.cars.items():
            score = car.get_performance_score()
            if not car.has_all_diagnostics():
                alert = "Sensor Failure Detected"
            elif score is not None and score < Car.SEVERE_STRESS_THRESHOLD:
                alert = "Severe Engine Stress"
            else:
                alert = None
            statuses[car_id] = {
                "score": score,
                "alert": alert,
                "diagnostics": car.diagnostics
            }
        return statuses

def parse_csv_file(filename):
    monitor = GarageMonitor()
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if not row or len(row) != 3:
                    print(f"Malformed line skipped: {row}")
                    continue
                car_id, diag_type, value = [x.strip() for x in row]
                if diag_type not in Diagnostic.VALID_TYPES:
                    print(f"Invalid diagnostic type skipped: {row}")
                    continue
                try:
                    value = float(value)
                except ValueError:
                    print(f"Non-numeric value skipped: {row}")
                    continue
                monitor.add_diagnostic(car_id, diag_type, value)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    return monitor

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python reviewcode.py <diagnostics.csv>")
        return
    filename = sys.argv[1]
    monitor = parse_csv_file(filename)
    if not monitor:
        return
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