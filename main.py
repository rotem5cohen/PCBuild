# main.py
from PCComponent import CPU, Case, Cooler, MotherBoard, GPU, PSU, RAM, Storage
from PCBuild import PCBuild


def main():
    my_build = PCBuild()

    print("--- Assembling New PC ---\n")

    cpu = CPU(brand="Intel", model="Core i5-14600K", price=1350, power_draw_w=125, socket="LGA 1700")

    mobo = MotherBoard(brand="Gigabyte", model="Z790 AORUS ELITE", price=1200, power_draw_w=30,
                       socket="LGA 1700", form_factor="ATX", supported_ram_type="DDR5",
                       ram_slots=4, pcie_x16_slots=1, m2_slots=4, sata_ports=4)

    ram = RAM(brand="Corsair", model="Vengeance DDR5", price=450, power_draw_w=10,
              ram_type="DDR5", capacity_gb=32, modules=2, speed_mhz=6000)

    cooler = Cooler(brand="Corsair", model="NAUTILUS 360 RS ARGB", price=500, power_draw_w=15,
                    supported_sockets={"LGA 1700", "LGA 1200", "AM5"}, height_mm=None, radiator_size_mm=360)

    gpu = GPU(brand="AMD", model="Radeon RX 9070 XT", price=2800, power_draw_w=275,
              length_mm=320, power_connectors={"8-pin PCIe": 2})

    pc_case = Case(brand="Corsair", model="4500X", price=650,
                   supported_form_factors={"ATX", "Micro-ATX", "Mini-ITX"},
                   max_gpu_length_mm=400, max_radiator_mm=360, max_cpu_cooler_height_mm=170,
                   drive_bays_2_5=2, drive_bays_3_5=2)

    psu = PSU(brand="Corsair", model="RM850x", price=550, wattage_w=850,
              available_connectors={"8-pin PCIe": 4, "24-pin ATX": 1, "4+4-pin EPS": 2, "SATA Power": 4})

    storage = Storage(brand="Samsung", model="990 PRO", price=650, power_draw_w=8, capacity_tb=2.0,
                      form_factor="M.2 2280", interface="NVMe PCIe 4.0", power_connectors={})

    my_build.add_component(cpu)
    my_build.add_component(mobo)
    my_build.add_component(ram)
    my_build.add_component(cooler)
    my_build.add_component(gpu)
    my_build.add_component(pc_case)
    my_build.add_component(psu)
    my_build.add_component(storage, custom_key="Storage_M2_1")

    my_build.print_build_summary()

    print("\n--- Running Validation Engine ---")
    errors = my_build.validate_all()

    if not errors:
        print("SUCCESS: Build is 100% compatible! All checks passed.")
    else:
        print("WARNING: Compatibility issues found:")
        for err in errors:
            print(f"  - {err}")


if __name__ == "__main__":
    main()