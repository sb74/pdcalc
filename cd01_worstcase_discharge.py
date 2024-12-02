from p_drop import *
from fittings import *
from display_results import *
from PipeSection import PipeSection
from typing import Dict, Any
import pandas as pd
from plot_system_curve import *

# Define system parameters
fluid_density = 1028    # kg/m³ (seawater at 5°C)
fluid_viscosity = 0.00155  # Pa·s
pipe_roughness = 0.0000457  # m (commercial steel)
design_flow = 0.277    # m³/s

# Define pipe sections
pipe_sections = [
    PipeSection(
        diameter=0.3366,  # m
        length=22,        # m
        fittings_k=[1.19, 0.595, 0.595, 0.119, 0.3808],
        elevation_change=0
    )
]

# Package parameters for calculations
parameters = {
    'pipe_sections': pipe_sections,
    'flow_rate': design_flow,
    'fluid_density': fluid_density,
    'fluid_viscosity': fluid_viscosity,
    'pipe_roughness': pipe_roughness
}

# Run calculations and display results
results = calculate_pressure_drop(**parameters)
display_results(results, fluid_density)
plot_system_curve(results, parameters)