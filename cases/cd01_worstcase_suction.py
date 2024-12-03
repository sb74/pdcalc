# CD01 PUMP STUDY
# Suction calculation for worst-case ballast tank 8C
from p_drop import *
from fittings import *
from display_results import *
from PipeSection import PipeSection
from typing import Dict, Any
import pandas as pd
from plot_system_curve import *
from calculate_npsha import calculate_npsha

# Define system parameters
fluid_density = 1028        # kg/m³ (seawater at 5°C)
fluid_viscosity = 0.00155   # Pa·s
pipe_roughness = 0.0000457  # m (commercial steel)
design_flow = 0.277         # m³/s

# Define pipe sections
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

# NPSHa calculation
total_suction_loss = sum(section['total_section_head_loss'] for section in results['sections'])
# Flow velocity at pump suction flange
flow_velocity = results['sections'][-1]['velocity']

npsha_results = calculate_npsha(
    atmospheric_pressure_head=10.33,        # Standard atmospheric pressure at sea level
    static_head=0,                          # MODIFY AS REQUIRED
    friction_head_loss=total_suction_loss,  # Total pipe friction and fitting losses
    flow_velocity=flow_velocity,            # Flow velocity at pump suction flange
    vapor_pressure_head=0.238               # Seawater at 5°C (~0.872 kPa)
)