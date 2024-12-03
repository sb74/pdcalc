import pandas as pd

def calculate_npsha(
    atmospheric_pressure_head: float,   # meters of head
    static_head: float,                 # meters (+ve if liquid above pump, -ve if below)
    friction_head_loss: float,          # meters of head
    flow_velocity: float,               # m/s
    vapor_pressure_head: float          # meters of head
) -> pd.DataFrame:
    """
    Calculate Net Positive Suction Head Available (NPSHA) for a pump system.
    """
    # Calculate velocity head
    velocity_head = (flow_velocity ** 2) / (2 * 9.81)
    
    # Calculate NPSHA in meters
    npsha_meters = (
        atmospheric_pressure_head +
        static_head -
        friction_head_loss +
        velocity_head -
        vapor_pressure_head
    )
    
    # Convert to bar
    npsha_bar = npsha_meters / 10.2
    
    # Create detailed results dataframe
    data = {
        'index': [
            'Atmospheric Pressure Head',
            'Static Head',
            'Friction Head Loss',
            'Velocity Head',
            'Vapor Pressure Head',
            'NPSHA'      
        ],
        'Value (m)': [
            round(atmospheric_pressure_head, 3),
            round(static_head, 3),
            round(-friction_head_loss, 3),
            round(velocity_head, 3),
            round(-vapor_pressure_head, 3),
            round(npsha_meters, 3)
        ],
        'Value (bar)': [
            round(atmospheric_pressure_head/10.2, 3),
            round(static_head/10.2, 3),
            round(-friction_head_loss/10.2, 3),
            round(velocity_head/10.2, 3),
            round(-vapor_pressure_head/10.2, 3),
            round(npsha_bar, 3)
        ]
    }
    
    # Create DataFrame and set index without naming it
    df = pd.DataFrame(data)
    df = df.set_index('index')
    df.index.name = None
    
    # Set display options
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    pd.set_option('display.max_columns', None)
    
    # Print with custom formatting
    print("\nNPSHA Calculation Breakdown:")
    print("=" * 50)
    print(df.iloc[:-1].to_string())
    print("-" * 50)
    print(f"{'NPSHA':<27}{npsha_meters:>9.3f}{npsha_bar:>13.3f}") 
    print("=" * 50)
    
    return df