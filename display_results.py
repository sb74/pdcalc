from typing import Dict, Any
import pandas as pd

def display_results(results: Dict[str, Any]) -> None:
    """
    Display pressure drop calculation results in a clear, formatted manner.
    
    Args:
        results: Dictionary containing calculation results
    """
    # Total pressure drops
    total_pressure_pa = results['total_pressure_drop']
    total_pressure_bar = total_pressure_pa / 1e5
    
    print("\nSUMMARY:")
    print(f"Total System Pressure Drop: {total_pressure_pa:.2f} Pa ({total_pressure_bar:.2f} bar)")
    
    # Create DataFrame for section breakdown
    sections_data = []
    for section in results['sections']:
        sections_data.append({
            'Section': section['section_number'],
            'Diameter (m)': section['diameter'],
            'Velocity (m/s)': section['velocity'],
            'Reynolds': f"{section['reynolds_number']:.2e}",
            'Flow Regime': section['flow_regime'],
            'Friction Loss (Pa)': f"{section['pressure_drop_friction']:.2f}",
            'Fitting Loss (Pa)': f"{section['pressure_drop_fittings']:.2f}",
            'Elevation Loss (Pa)': f"{section['pressure_drop_elevation']:.2f}",
            'Total Loss (Pa)': f"{section['total_section_pressure_drop']:.2f}",
            'Total Loss (bar)': f"{section['total_section_pressure_drop']/1e5:.3f}"
        })
    
    df = pd.DataFrame(sections_data)
    
    print("\nDETAILED BREAKDOWN:")
    print(df.to_string(index=False))
    
    # Optional: Save results to CSV
    # df.to_csv('pressure_drop_results.csv', index=False)