from abc import ABC, abstractmethod
from typing import Dict, List
from PCComponent import PCComponent
from PCComponent import Case, GPU, MotherBoard, CPU, RAM, Cooler, Storage, PSU


class ValidationRule(ABC):

    @abstractmethod
    def validate(self, build_components: Dict[str, PCComponent]) -> List[str]:
        pass

class CoolerClearanceRule(ValidationRule):
    def validate(self, build_components: Dict[str, PCComponent]) -> List[str]:
        errors = []

        pc_case: Case = build_components.get("Case")
        cooler: Cooler = build_components.get("Cooler")

        if not pc_case or not cooler:
            return errors

        if cooler.height_mm is not None:
            if cooler.height_mm > pc_case.max_cpu_cooler_height_mm:
                errors.append(
                    f"Cooler height ({cooler.height_mm}mm) exceeds case limit "
                    f"({pc_case.max_cpu_cooler_height_mm}mm)."
                )

        if cooler.radiator_size_mm is not None:
            if cooler.radiator_size_mm > pc_case.max_radiator_mm:
                errors.append(
                    f"Radiator size ({cooler.radiator_size_mm}mm) is too large "
                    f"for case limit ({pc_case.max_radiator_mm}mm)."
                )

        return errors


class PowerSupplyRule(ValidationRule):
    def validate(self, build_components: Dict[str, PCComponent]) -> List[str]:
        errors = []

        psu: PSU = build_components.get("PSU")
        if not psu:
            return errors

        total_power_draw = 0
        required_connectors: Dict[str, int] = {}

        for component in build_components.values():
            total_power_draw += component.power_draw_w

            if hasattr(component, "power_connectors"):
                for connector_type, count in component.power_connectors.items():
                    required_connectors[connector_type] = required_connectors.get(connector_type, 0) + count

        safe_wattage_limit = psu.wattage_w * 0.90

        if total_power_draw > safe_wattage_limit:
            errors.append(
                f"Total power draw ({total_power_draw}W) exceeds safe PSU limit "
                f"({safe_wattage_limit}W out of {psu.wattage_w}W)."
            )

        for connector_type, required_count in required_connectors.items():
            available_count = psu.available_connectors.get(connector_type, 0)

            if required_count > available_count:
                errors.append(
                    f"Not enough {connector_type} cables. "
                    f"Required: {required_count}, Available: {available_count}."
                )

        return errors


class MotherboardCompatibilityRule(ValidationRule):
    def validate(self, build_components: Dict[str, PCComponent]) -> List[str]:
        errors = []

        mb: Motherboard = build_components.get("Motherboard")
        if not mb:
            return errors

        cpu: CPU = build_components.get("CPU")
        ram: RAM = build_components.get("RAM")
        cooler: Cooler = build_components.get("Cooler")

        if cpu:
            if cpu.socket != mb.socket:
                errors.append(
                    f"CPU socket ({cpu.socket}) does not match Motherboard socket ({mb.socket})."
                )

        if cooler:
            if mb.socket not in cooler.supported_sockets:
                errors.append(
                    f"Cooler does not support the motherboard socket ({mb.socket})."
                )

        if ram:
            if ram.ram_type != mb.supported_ram_type:
                errors.append(
                    f"RAM type ({ram.ram_type}) is not supported by Motherboard ({mb.supported_ram_type})."
                )

            if ram.modules > mb.ram_slots:
                errors.append(
                    f"Not enough RAM slots on Motherboard. "
                    f"Required: {ram.modules}, Available: {mb.ram_slots}."
                )

        return errors


class CaseClearanceRule(ValidationRule):
    def validate(self, build_components: Dict[str, PCComponent]) -> List[str]:
        errors = []

        pc_case: Case = build_components.get("Case")
        if not pc_case:
            return errors

        gpu: GPU = build_components.get("GPU")
        mb: Motherboard = build_components.get("Motherboard")

        if gpu:
            if gpu.length_mm > pc_case.max_gpu_length_mm:
                errors.append(
                    f"GPU length ({gpu.length_mm}mm) exceeds the maximum allowed "
                    f"in the case ({pc_case.max_gpu_length_mm}mm)."
                )

        if mb:
            if mb.form_factor not in pc_case.supported_form_factors:
                errors.append(
                    f"Motherboard form factor ({mb.form_factor}) is not supported "
                    f"by the case. Supported: {', '.join(pc_case.supported_form_factors)}."
                )

        return errors


class StorageCompatibilityRule(ValidationRule):
    def validate(self, build_components: Dict[str, PCComponent]) -> List[str]:
        errors = []

        mb: Motherboard = build_components.get("Motherboard")
        pc_case: Case = build_components.get("Case")

        m2_count = 0
        sata_count = 0
        bay_2_5_count = 0
        bay_3_5_count = 0

        for component in build_components.values():
            if component.component_type == "Storage":

                if "M.2" in component.form_factor:
                    m2_count += 1
                if "SATA" in component.interface:
                    sata_count += 1

                if "2.5" in component.form_factor:
                    bay_2_5_count += 1
                if "3.5" in component.form_factor:
                    bay_3_5_count += 1

        if mb:
            if m2_count > mb.m2_slots:
                errors.append(
                    f"Not enough M.2 slots on Motherboard. "
                    f"Required: {m2_count}, Available: {mb.m2_slots}."
                )
            if sata_count > mb.sata_ports:
                errors.append(
                    f"Not enough SATA ports on Motherboard. "
                    f"Required: {sata_count}, Available: {mb.sata_ports}."
                )

        if pc_case:
            if bay_2_5_count > pc_case.drive_bays_2_5:
                errors.append(
                    f"Not enough 2.5\" drive bays in Case. "
                    f"Required: {bay_2_5_count}, Available: {pc_case.drive_bays_2_5}."
                )
            if bay_3_5_count > pc_case.drive_bays_3_5:
                errors.append(
                    f"Not enough 3.5\" drive bays in Case. "
                    f"Required: {bay_3_5_count}, Available: {pc_case.drive_bays_3_5}."
                )

        return errors