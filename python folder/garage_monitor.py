from car import Car


class GarageMonitor:
    """
    @brief Manages multiple cars, updates diagnostics, and checks for issues.
    """

    def __init__(self):
        """
        @brief GarageMonitor constructor.
        """
        self.cars = {}

    def add_diagnostic(self, car_id, diag_type, value):
        """
        @brief Adds or updates a diagnostic for a specific car.
        @param car_id Car identifier.
        @param diag_type Diagnostic type.
        @param value Numeric value.
        """
        if car_id not in self.cars:
            self.cars[car_id] = Car(car_id)
        self.cars[car_id].update_diagnostic(diag_type, value)

    def get_car_statuses(self):
        """
        @brief Returns each car's score, alerts, and diagnostics.
        @return Dictionary of car statuses.
        """
        statuses = {}
        for car_id, car in self.cars.items():
            score = car.get_performance_score()
            if not car.has_all_diagnostics():
                alert = "Sensor Failure Detected"
            elif score is not None and score < 40:
                alert = "Severe Engine Stress"
            else:
                alert = None
            statuses[car_id] = {
                "score": score,
                "alert": alert,
                "diagnostics": car.diagnostics
            }
        return statuses
