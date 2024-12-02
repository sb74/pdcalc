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
    # Assuming worst case at 5degC
    seawater_density = 1028
    seawater_viscosity = 0.00155
    
    pipe_sections = [
        PipeSection(
            diameter=0.3366,
            length=6,
            fittings_k=[0.05, 0.216, 0.3375],
            elevation_change=0
        ),
        PipeSection(
            diameter=0.3872,
            length=119,
            fittings_k=[1.904, 1.36, 0.784, 0.4352, 1.36],
            elevation_change=0
        )
    ]
    
    parameters = {
        'pipe_sections': pipe_sections,
        'flow_rate': 0.277,
        'fluid_density': seawater_density,
        'fluid_viscosity': seawater_viscosity,
        'pipe_roughness': 0.0000457
    }
    
    return calculate_pressure_drop(**parameters)

if __name__ == "__main__":
    results = suction_loss_worst_case()
    display_results(results, 1028)