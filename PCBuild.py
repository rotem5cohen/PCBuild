# PCBuild.py
from typing import Dict, List
from PCComponent import PCComponent, CPU, MotherBoard, GPU, Case, PSU, RAM, Cooler, Storage
from ValidationRule import (ValidationRule, MotherBoardCompatibilityRule,
                            CaseClearanceRule, CoolerClearanceRule,
                            PowerSupplyRule, StorageCompatibilityRule)


class PCBuild:
    def __init__(self):
        self.components: Dict[str, PCComponent] = {}

        self.rules: List[ValidationRule] = [
            MotherBoardCompatibilityRule(),
            CaseClearanceRule(),
            CoolerClearanceRule(),
            PowerSupplyRule(),
            StorageCompatibilityRule()
        ]

    def add_component(self, component: PCComponent, custom_key: str = None):

        key = custom_key if custom_key else component.component_type

        self.components[key] = component
        print(f"Added {component.component_type}: {component.brand} {component.model}")

    def validate_all(self) -> List[str]:
        all_errors = []

        if not self.components:
            return ["Error: Build is empty. Please add components first."]

        for rule in self.rules:
            errors = rule.validate(self.components)
            all_errors.extend(errors)

        return all_errors

    def print_build_summary(self):
        print("\n--- Current PC Build Summary ---")
        total_price = 0
        total_power = 0

        for key, comp in self.components.items():
            print(f"[{key}] {comp.brand} {comp.model} - ${comp.price}")
            total_price += comp.price
            total_power += comp.power_draw_w

        print("-" * 30)
        print(f"Total Price: ${total_price:.2f}")
        print(f"Total Power Draw: {total_power}W (Before PSU Efficiency)")
        print("-" * 30)