import math

def calculate_f_T(relative_roughness):
    """
    Calculate Crane TP-410 f_T coefficient for fittings using relative roughness from Crane TP-410, A-25
    Returns:
        f_T: Coefficient to apply to Crane TP-410 fitting K values
    """

    return 0.25 / (math.log10(relative_roughness / 3.7))**2

def get_fittings(relative_roughness):
    """
    Common fitting K-values (From Crane TP-410, A-28), multiplied by F_t to be accurate.
    """

    fittings = {
    'elbow_90deg_standard': 0.75,
    'elbow_90deg_long_radius': 0.45,
    'elbow_45deg': 0.35,
    'tee_straight_through': 0.4,
    'tee_branch_flow': 1.5,
    'gate_valve_full_open': 0.2,
    'gate_valve_half_open': 5.6,
    'globe_valve_full_open': 10,
    'angle_valve_full_open': 5,
    'swing_check_valve': 2.5,
    'strainer': 2.5
    }
    
    return {k: v * calculate_f_T(relative_roughness) for k, v in fittings.items()}