import math
import numpy as np
from typing import List, Dict, Union
from PipeSection import PipeSection

def calculate_pressure_drop(
    pipe_sections: List['PipeSection'],
    flow_rate: float,            # m³/s
    fluid_density: float,        # kg/m³
    fluid_viscosity: float,      # Pa·s
    pipe_roughness: float,       # meters
    gravity: float = 9.81        # m/s²
    ) -> Dict[str, Union[float, List[Dict]]]:
    """
    Calculate head loss in a piping system with varying diameters, based on Crane TP 410.
    
    Args:
        pipe_sections: List of PipeSection objects defining the system
        flow_rate: Volumetric flow rate in m³/s
        fluid_density: Density of fluid in kg/m³
        fluid_viscosity: Dynamic viscosity of fluid in Pa·s
        pipe_roughness: Absolute roughness of pipe in meters
        gravity: Acceleration due to gravity in m/s²
    
    Returns:
        Dictionary containing head losses and flow characteristics for each section
    """
    total_results = {
        'total_head_loss': 0,
        'sections': []
    }
    
    def calculate_friction_factor(reynolds: float, diameter: float) -> float:
        """
        Calculate friction factor using Colebrook-White equation for turbulent flow
        and analytical solution for laminar flow.
        
        Args:
            reynolds: Reynolds number
            diameter: Pipe diameter in meters
        
        Returns:
            Darcy friction factor
        """
        # Laminar flow
        if reynolds < 2300:
            return 64 / reynolds
            
        # Transitional flow - use linear interpolation
        elif 2300 <= reynolds < 4000:
            f_lam = 64 / 2300
            f_turb = _colebrook_white_turbulent(4000, diameter)
            return f_lam + (f_turb - f_lam) * (reynolds - 2300) / (4000 - 2300)
            
        # Turbulent flow
        else:
            return _colebrook_white_turbulent(reynolds, diameter)
    
    def _colebrook_white_turbulent(reynolds: float, diameter: float) -> float:
        """
        Solve Colebrook-White equation for turbulent flow using the Serghides
        explicit approximation, which is accurate to within 0.0023% of the
        implicit equation.
        
        Args:
            reynolds: Reynolds number
            diameter: Pipe diameter in meters
            
        Returns:
            Darcy friction factor for turbulent flow
        """
        relative_roughness = pipe_roughness / diameter
        
        # Serghides approximation terms
        A = -2 * math.log10(relative_roughness/3.7 + 12/reynolds)
        B = -2 * math.log10(relative_roughness/3.7 + 2.51*A/reynolds)
        C = -2 * math.log10(relative_roughness/3.7 + 2.51*B/reynolds)
        
        # Calculate friction factor
        f = (A - (B-A)**2 / (C-2*B+A))**-2
        
        return f
    
    # Calculate head loss for each section
    for i, section in enumerate(pipe_sections):
        # Calculate pipe area and velocity
        area = math.pi * (section.diameter/2)**2
        velocity = flow_rate / area
        
        # Calculate Reynolds number
        reynolds = (fluid_density * velocity * section.diameter) / fluid_viscosity
        
        # Get friction factor
        f = calculate_friction_factor(reynolds, section.diameter)
        
        # Calculate major losses (friction) - Darcy Equation
        h_major = f * (section.length/section.diameter) * (velocity**2)/(2*gravity)
        
        # Calculate minor losses (fittings)
        k_total = sum(section.fittings_k)
        h_minor = k_total * (velocity**2)/(2*gravity)
        
        # Total head loss for this section including elevation change
        h_section = h_major + h_minor + section.elevation_change
        
        # Determine flow regime with more detailed classification
        if reynolds < 2300:
            flow_regime = 'Laminar'
        elif 2300 <= reynolds < 4000:
            flow_regime = 'Transitional'
        else:
            flow_regime = 'Turbulent'
        
        section_results = {
            'section_number': i + 1,
            'diameter': section.diameter,
            'length': section.length,
            'velocity': velocity,
            'reynolds_number': reynolds,
            'friction_factor': f,
            'head_loss_friction': h_major,
            'head_loss_fittings': h_minor,
            'elevation_change': section.elevation_change,
            'total_section_head_loss': h_section,
            'flow_regime': flow_regime
        }
        
        total_results['sections'].append(section_results)
        total_results['total_head_loss'] += h_section
    
    return total_results