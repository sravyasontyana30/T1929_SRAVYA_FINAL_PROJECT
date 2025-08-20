import unittest
from diagnostic import Diagnostic
from car import Car
from garage_monitor import GarageMonitor
import tempfile
import os
import csv

class TestDiagnostics(unittest.TestCase):
    def test_diagnostic_valid(self):
        d = Diagnostic("RPM", 5000)
        self.assertEqual(d.type, "RPM")
        self.assertEqual(d.value, 5000)

    def test_diagnostic_invalid_type(self):
        with self.assertRaises(ValueError):
            Diagnostic("INVALID", 100)

    def test_diagnostic_invalid_value(self):
        with self.assertRaises(ValueError):
            Diagnostic("RPM", "not_a_number")

class TestCar(unittest.TestCase):
    def setUp(self):
        self.car = Car("Car1")

    def test_severe_engine_stress(self):
        self.car.update_diagnostic("RPM", 6500)
        self.car.update_diagnostic("EngineLoad", 95)
        self.car.update_diagnostic("CoolantTemp", 120)
        score = self.car.get_performance_score()
        self.assertLess(score, 40)

    def test_sensor_failure(self):
        self.car.update_diagnostic("RPM", 6500)
        self.car.update_diagnostic("EngineLoad", 95)
        # Missing CoolantTemp
        self.assertFalse(self.car.has_all_diagnostics())
        self.assertIsNone(self.car.get_performance_score())

    def test_boundary_score_40(self):
        # Find values that yield exactly 40: 100 - (rpm/100 + load*0.5 + (coolantTemp-90)*2) = 40
        # Let's set coolantTemp=90, so (coolantTemp-90)*2 = 0
        # 100 - (rpm/100 + load*0.5) = 40 => rpm/100 + load*0.5 = 60
        # Try rpm=2000, load=80: 2000/100=20, 80*0.5=40, 20+40=60
        self.car.update_diagnostic("RPM", 2000)
        self.car.update_diagnostic("EngineLoad", 80)
        self.car.update_diagnostic("CoolantTemp", 90)
        score = self.car.get_performance_score()
        self.assertEqual(score, 40)

class TestGarageMonitor(unittest.TestCase):
    def setUp(self):
        self.garage = GarageMonitor()

    def test_average_score(self):
        # Car1: score=70
        self.garage.add_diagnostic("Car1", "RPM", 1000)  # 1000/100=10
        self.garage.add_diagnostic("Car1", "EngineLoad", 40)  # 40*0.5=20
        self.garage.add_diagnostic("Car1", "CoolantTemp", 90)  # (90-90)*2=0
        # score1 = 100 - (10+20+0) = 70
        # Car2: score=30
        self.garage.add_diagnostic("Car2", "RPM", 3000)  # 3000/100=30
        self.garage.add_diagnostic("Car2", "EngineLoad", 60)  # 60*0.5=30
        self.garage.add_diagnostic("Car2", "CoolantTemp", 95)  # (95-90)*2=10
        # score2 = 100 - (30+30+10) = 30
        statuses = self.garage.get_car_statuses()
        scores = [s["score"] for s in statuses.values() if s["score"] is not None]
        avg = sum(scores) / len(scores)
        self.assertEqual(avg, 50)

    def test_empty_csv_raises(self):
        # Simulate empty CSV file
        from reviewcode import parse_csv_file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, newline='') as tmp:
            tmp.write("")
            tmp_path = tmp.name
        try:
            monitor = parse_csv_file(tmp_path)
            statuses = monitor.get_car_statuses() if monitor else {}
            self.assertEqual(len(statuses), 0)
        finally:
            os.remove(tmp_path)

if __name__ == "__main__":
    unittest.main()
