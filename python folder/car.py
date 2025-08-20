from diagnostic import Diagnostic


class Car:
    """
    @brief Holds all diagnostics for a single car and computes its performance score.

    @param car_id The identifier for the car.
    """

    def __init__(self, car_id):
        """
        @brief Car constructor.
        @param car_id The car's identifier.
        """
        self.car_id = car_id
        self.diagnostics = {}

    def update_diagnostic(self, diag_type, value):
        """
        @brief Adds or updates a diagnostic for the car.
        @param diag_type Diagnostic type.
        @param value Numeric value.
        """
        self.diagnostics[diag_type] = Diagnostic(diag_type, value)

    def get_performance_score(self):
        """
        @brief Calculates the car's performance score.
        @return The performance score, or None if any required diagnostic is missing.
        """
        try:
            rpm = self.diagnostics["RPM"].value
            engine_load = self.diagnostics["EngineLoad"].value
            coolant_temp = self.diagnostics["CoolantTemp"].value
        except KeyError:
            return None
        score = 100 - (rpm/100 + engine_load*0.5 + (coolant_temp-90)*2)
        return score

    def has_all_diagnostics(self):
        """
        @brief Checks if all required diagnostics are present.
        @return True if all diagnostics are present, False otherwise.
        """
        return all(t in self.diagnostics for t in Diagnostic.VALID_TYPES)
