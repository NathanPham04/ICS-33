from pathlib import Path
from simulation import *


def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input())


def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()
    simulation = Simulation(input_file_path)
    simulation.read_file()
    simulation.set_device_rules()
    simulation.sort_messages()
    simulation.start_simulation()

if __name__ == '__main__':
    main()