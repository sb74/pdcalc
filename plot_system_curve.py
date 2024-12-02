import numpy as np
from matplotlib import pyplot as plt
from p_drop import *
from fittings import *
from display_results import *
from PipeSection import PipeSection
from typing import Dict, Any

def plot_system_curve(
    results: Dict[str, Any],
    parameters: Dict[str, Any],
    flow_range: tuple = (0.1, 2.0),
    num_points: int = 50,
    show_points: bool = False,
    save_path: str = None
) -> None:
    """
    Calculate and plot system curve for any pipe system.
    """
    # Rest of function remains the same...
    base_flow = parameters['flow_rate']
    
    flow_factors = np.linspace(flow_range[0], flow_range[1], num_points)
    flow_rates = base_flow * flow_factors
    heads = []
    
    for flow in flow_rates:
        parameters['flow_rate'] = flow
        new_results = calculate_pressure_drop(**parameters)
        heads.append(new_results['total_head_loss'])
        
        if show_points:
            print(f"\nFlow Rate: {flow:.3f} m³/s")
            display_results(new_results, parameters['fluid_density'])
    
    parameters['flow_rate'] = base_flow
    
    plt.figure(figsize=(10, 6))
    plt.plot(flow_rates, heads, 'b-', linewidth=2)
    
    design_point_idx = np.where(flow_rates >= base_flow)[0][0]
    plt.plot(base_flow, heads[design_point_idx], 'ro', label='Design Point')
    
    plt.xlabel('Flow Rate (m³/s)')
    plt.ylabel('Total Head Loss (m)')
    plt.title('System Curve')
    plt.grid(True)
    plt.legend()
    
    if save_path:
        plt.savefig(save_path)
    plt.show()