#TODO tkinter gui and .exe
#TODO fully Crane-ify
import math
import numpy as np

class PipeSection:
    def __init__(self, diameter, length, fittings_k=None, elevation_change=0):
        """
        Initialize a pipe section with its properties
        """
        self.diameter = diameter
        self.length = length
        self.elevation_change = elevation_change
        self.fittings_k =  fittings_k if fittings_k is not None else []

def calculate_pressure_drop(
    pipe_sections,        # list of PipeSection objects
    flow_rate,            # m³/s
    fluid_density,        # kg/m³
    fluid_viscosity,      # Pa·s
    pipe_roughness,       # meters
    gravity=9.81          # m/s²
    ):
    """
    Calculate pressure drop in a piping system with varying diameters, based on Crane TP 410.
    
    Args:
        pipe_sections: List of PipeSection objects defining the system
        flow_rate: Volumetric flow rate in m³/s
        fluid_density: Density of fluid in kg/m³
        fluid_viscosity: Dynamic viscosity of fluid in Pa·s
        pipe_roughness: Absolute roughness of pipe in meters
        gravity: Acceleration due to gravity in m/s²
    
    Returns:
        Dictionary containing pressure drops and flow characteristics for each section
    """
    total_results = {
        'total_pressure_drop': 0,
        'sections': []
    }
    
    def calculate_friction_factor(reynolds, diameter):
        # Calculate friction factor using implicit iterative colebrook-White equation
        if reynolds < 2000:
            return 64 / reynolds

        def colebrook_white(f):
            return 1/math.sqrt(f) + 2 * math.log10(
                (pipe_roughness/(3.7*diameter)) + (2.51/(reynolds*math.sqrt(f)))
            )
        
        # Solve using Newton-Raphson method
        f = 0.02  # Initial guess
        for _ in range(20):
            f_new = f - colebrook_white(f)/(
                -1/(2*f**(3/2)) - 2.51/(reynolds*f*math.sqrt(f)*math.log(10))
            )
            if abs(f_new - f) < 1e-6:
                break
            f = f_new
        return f
    
    # Calculate pressure drop for each section
    for i, section in enumerate(pipe_sections):
        # Calculate pipe area and velocity for this section
        area = math.pi * (section.diameter/2)**2
        velocity = flow_rate / area
        
        # Calculate Reynolds number
        reynolds = (fluid_density * velocity * section.diameter) / fluid_viscosity
        
        # Get friction factor
        f = calculate_friction_factor(reynolds, section.diameter)
        
        # Calculate major losses (friction) - Darcy Equation
        h_major = f * (section.length/section.diameter) * (velocity**2)/(2*gravity)
        dp_major = h_major * fluid_density * gravity
        
        # Calculate minor losses (fittings)
        k_total = sum(section.fittings_k)
        h_minor = k_total * (velocity**2)/(2*gravity)
        dp_minor = h_minor * fluid_density * gravity
        
        # Calculate elevation pressure change
        dp_elevation = fluid_density * gravity * section.elevation_change
        
        # Calculate total pressure drop for this section
        dp_section = dp_major + dp_minor + dp_elevation
        
        section_results = {
            'section_number': i + 1,
            'diameter': section.diameter,
            'length': section.length,
            'velocity': velocity,
            'reynolds_number': reynolds,
            'friction_factor': f,
            'pressure_drop_friction': dp_major,
            'pressure_drop_fittings': dp_minor,
            'pressure_drop_elevation': dp_elevation,
            'total_section_pressure_drop': dp_section,
            'flow_regime': 'Laminar' if reynolds < 2300 else 'Turbulent'
        }
        
        total_results['sections'].append(section_results)
        total_results['total_pressure_drop'] += dp_section
    
    return total_results