# Automotive Diagnostics Project

## Introduction

The Automotive Diagnostics project is a modular, object-oriented Python application designed to simulate real-world automotive diagnostic monitoring. It demonstrates how to structure Python code using classes and modules, making it an excellent case study for learning OOP and modular programming in Python.

**Purpose:**
- Teach modular Python and object-oriented programming (OOP) concepts using an automotive diagnostics scenario.
- Provide hands-on experience with file parsing, data validation, and error handling.

**Key Features:**
- Reads and validates diagnostic data from a CSV file.
- Calculates a performance score for each car based on diagnostic values.
- Detects and alerts for severe engine stress and sensor failures.
- Handles malformed or missing data gracefully with clear error messages.

## Explanation of Classes & Functions

### Diagnostic
- **Purpose:** Stores individual diagnostic data for a car.
- **Attributes:**
  - `type`: The type of diagnostic ("RPM", "EngineLoad", "CoolantTemp").
  - `value`: The numeric value of the diagnostic.
- **Validation:** Ensures only valid types and numeric values are accepted.

### Car
- **Purpose:** Holds all diagnostics for a single car and computes its performance score.
- **Key Methods:**
  - `update_diagnostic(diag_type, value)`: Adds or updates a diagnostic for the car.
  - `get_performance_score()`: Calculates the car's performance score using the formula:
    
    `score = 100 - (rpm/100 + engineLoad*0.5 + (coolantTemp-90)*2)`
    
    Returns `None` if any required diagnostic is missing.
  - `has_all_diagnostics()`: Checks if all required diagnostics are present.

### GarageMonitor
- **Purpose:** Manages multiple cars, updates diagnostics, and checks for issues.
- **Key Methods:**
  - `add_diagnostic(car_id, diag_type, value)`: Adds or updates a diagnostic for a specific car.
  - `get_car_statuses()`: Returns each car's score, alerts (e.g., "Severe Engine Stress", "Sensor Failure Detected"), and diagnostics.

### main.py
- **Purpose:** Entry point for the application.
- **Key Functions:**
  - `parse_csv_line(line)`: Parses and validates a line from the CSV file.
  - `main()`: Loads diagnostics from the CSV, updates the garage, and prints each car's status and alerts in a readable format.

## How to Use
1. Place your diagnostic data in a CSV file (e.g., `diagnostics.csv`) with lines like:
   ```
   Car1,RPM,6500
   Car1,CoolantTemp,120
   Car1,EngineLoad,95
   Car2,RPM,3000
   Car2,CoolantTemp,95
   Car2,EngineLoad,60
   ```
2. Run the program:
   ```
   python main.py diagnostics.csv
   ```
3. Review the output for each car's performance score and any alerts.

---
This project is ideal for beginners and educators looking to understand and teach modular Python programming with a practical, real-world example.
