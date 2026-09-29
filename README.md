# PC Hardware Compatibility Engine

An extensible, object-oriented validation engine designed to verify PC hardware compatibility. This project simulates the core algorithmic logic behind platforms like PCPartPicker, focusing on clean architecture, efficient data structures, and highly scalable design.

##  Architecture & Design Principles

The engine is built with maintainability and scalability in mind, heavily relying on **SOLID principles**:

*   **Open/Closed Principle:** Validation logic is entirely decoupled from the hardware component data. Hardware limits are tested via an abstract `ValidationRule` class. New compatibility checks (e.g., thermal limits, PCIe lane allocation) can be added simply by extending this base class, without modifying existing logic.
*   **Polymorphism & Duck Typing:** The validation engine processes components dynamically based on their attributes (e.g., `power_connectors`) rather than rigid type-checking. This allows seamless integration of future component categories.
*   **Centralized State Management:** A `PCBuild` controller acts as the central orchestrator, managing component state and executing the validation pipeline.

##  Algorithmic Efficiency & Data Structures

To ensure optimal performance during the validation pipeline, specific data structures were selected over standard iterations:

*   **O(1) Lookups:** Utilized Python `Set` structures for mapping motherboard sockets, supported RAM types, and physical form factors. This reduces time complexity during cross-component compatibility scans.
*   **Dynamic Aggregation (Hash Maps):** Power supply constraints (total wattage, PCIe 8-pin, SATA power) are aggregated dynamically using `Dictionary` structures. This eliminates the need for deeply nested loops when counting required physical connectors across the entire build.

##  Quick Start

### 1. Define Components
Components are instantiated as objects containing only logic-relevant physical and electrical constraints.

```python
from PCComponent import CPU, GPU, MotherBoard, Case, PSU
from PCBuild import PCBuild

cpu = CPU(brand="Intel", model="Core i5-14600K", price=1350, power_draw_w=125, socket="LGA 1700")
gpu = GPU(brand="AMD", model="Radeon RX 9070 XT", price=2800, power_draw_w=275, length_mm=320, power_connectors={"8-pin PCIe": 2})

my_build = PCBuild()
my_build.add_component(cpu)
my_build.add_component(gpu)

# Executes all active ValidationRules (Power, Clearance, Socket compatibility)
errors = my_build.validate_all()

if not errors:
    print("Build is 100% compatible!")
else:
    for err in errors:
        print(f"Error: {err}")
