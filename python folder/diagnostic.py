
class Diagnostic:
    """
    @brief Stores individual diagnostic data for a car.

    @var VALID_TYPES
        Set of valid diagnostic types.
    """
    VALID_TYPES = {"RPM", "EngineLoad", "CoolantTemp"}

    def __init__(self, diag_type, value):
        """
        @brief Diagnostic constructor with validation.
        @param diag_type Diagnostic type.
        @param value Numeric value.
        @throws ValueError if diag_type is invalid or value is not numeric.
        """
        if diag_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid diagnostic type: {diag_type}")
        if not isinstance(value, (int, float)):
            raise ValueError("Diagnostic value must be numeric")
        self.type = diag_type
        self.value = value

    def __repr__(self):
        """
        @brief String representation of Diagnostic.
        @return String describing the diagnostic.
        """
        return f"Diagnostic(type={self.type}, value={self.value})"
