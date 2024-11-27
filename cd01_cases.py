from p_drop import *
from fittings import *

# AMT Previous Case - Suction Loss
# Fittings (additional are K values only, not Crane)
relative_roughness1 = 1         # From Crane TP 410, A-26
fittings1 = get_fittings(relative_roughness1)
additional_fittings = []

# Pipe sections
pipe1 = PipeSection(2, 2, 2, fittings1)
pipeline = [pipe1, ]

def example_ballast_calculation():
    # Example parameters for seawater at 20°C
    seawater_density = 1025  # kg/m³
    seawater_viscosity = 0.001075  # Pa·s
    
    # Define pipe sections with different diameters
    pipe_sections = [
        PipeSection(
            diameter=0.3,    # 300mm pipe
            length=20,       # 20m length
            fittings_k=[0.5, 0.5],  # Two elbows
            elevation_change=2
        ),
        PipeSection(
            diameter=0.25,   # 250mm pipe
            length=15,       # 15m length
            fittings_k=[10],  # One gate valve
            elevation_change=1.5
        ),
        PipeSection(
            diameter=0.2,    # 200mm pipe
            length=15,       # 15m length
            fittings_k=[0.5],  # One elbow
            elevation_change=1.5
        )
    ]
    
    parameters = {
        'pipe_sections': pipe_sections,
        'flow_rate': 0.2,      # 0.2 m³/s
        'fluid_density': seawater_density,
        'fluid_viscosity': seawater_viscosity,
        'pipe_roughness': 0.00015  # Commercial steel
    }
    
    results = calculate_pressure_drop(**parameters)
    return results