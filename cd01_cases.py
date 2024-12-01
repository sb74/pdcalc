from p_drop import *
from fittings import *
from display_results import *
from PipeSection import PipeSection
from typing import Dict, Any
import pandas as pd

def suction_loss_worst_case() -> Dict[str, Any]:
    """
    Calculate worst-case pressure loss for suction line with seawater.
    
    Returns:
        Dict containing calculation results and section-by-section breakdown
    """
    seawater_density = 1025
    seawater_viscosity = 0.001075
    
    pipe_sections = [
        PipeSection(
            diameter=0.3,
            length=20,
            fittings_k=[0.5, 0.5],
            elevation_change=2
        ),
        PipeSection(
            diameter=0.25,
            length=15,
            fittings_k=[10],
            elevation_change=1.5
        ),
        PipeSection(
            diameter=0.2,
            length=15,
            fittings_k=[0.5],
            elevation_change=1.5
        )
    ]
    
    parameters = {
        'pipe_sections': pipe_sections,
        'flow_rate': 0.277,
        'fluid_density': seawater_density,
        'fluid_viscosity': seawater_viscosity,
        'pipe_roughness': 0.00015
    }
    
    return calculate_pressure_drop(**parameters)

if __name__ == "__main__":
    results = suction_loss_worst_case()
    display_results(results)