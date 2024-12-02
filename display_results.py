from typing import Dict, Any
import pandas as pd

def display_results(results: Dict[str, Any], fluid_density: float, gravity: float = 9.81) -> None:
    """
    Display head loss and pressure drop calculation results.
    
    Args:
        results: Dictionary containing calculation results in meters of head
        fluid_density: Density of fluid in kg/m³
        gravity: Acceleration due to gravity in m/s² (default 9.81)
    """
    # Total head loss and pressure
    total_head = results['total_head_loss']
    total_pressure_bar = total_head * fluid_density * gravity / 1e5
    
    print("\nSUMMARY:")
    print(f"Total System Head Loss: {total_head:.2f} m")
    print(f"Total System Pressure Drop: {total_pressure_bar:.2f} bar")
    
    # Create DataFrame for section breakdown
    sections_data = []
    for section in results['sections']:
        # Calculate bar directly
        pressure_friction = section['head_loss_friction'] * fluid_density * gravity / 1e5
        pressure_fittings = section['head_loss_fittings'] * fluid_density * gravity / 1e5
        pressure_elevation = section['elevation_change'] * fluid_density * gravity / 1e5
        total_pressure = section['total_section_head_loss'] * fluid_density * gravity / 1e5
        
        sections_data.append({
            'Section': section['section_number'],
            'Diameter (m)': section['diameter'],
            'Velocity (m/s)': section['velocity'],
            'Reynolds': f"{section['reynolds_number']:.2e}",
            'Flow Regime': section['flow_regime'],
            'Loss (m)': f"{section['head_loss_friction']:.2f}",
            'Loss (bar)': f"{pressure_friction:.3f}",
            'Fitting (m)': f"{section['head_loss_fittings']:.2f}",
            'Fitting (bar)': f"{pressure_fittings:.3f}",
            'Elevation (m)': f"{section['elevation_change']:.2f}",
            'Elevation (bar)': f"{pressure_elevation:.3f}",
            'Total (m)': f"{section['total_section_head_loss']:.2f}",
            'Total (bar)': f"{total_pressure:.3f}"
        })
    
    df = pd.DataFrame(sections_data)
    
    print("\nDETAILED BREAKDOWN:")
    print(df.to_string(index=False))
    
    # Optional: Save results to CSV
    # df.to_csv('hydraulic_results.csv', index=False)