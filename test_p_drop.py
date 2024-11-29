import pytest
from p_drop import calculate_pressure_drop
from PipeSection import PipeSection

def test_basic_pressure_drop():
    """Test a simple single-section pipe with known values."""
    # Single straight pipe section, horizontal
    pipe_sections = [
        PipeSection(
            diameter=0.1,    # 100mm pipe
            length=10,       # 10m length
            fittings_k=[0],  # No fittings
            elevation_change=0  # Horizontal
        )
    ]
    
    parameters = {
        'pipe_sections': pipe_sections,
        'flow_rate': 0.01,           # 10 L/s
        'fluid_density': 1000,       # Water
        'fluid_viscosity': 0.001,    # Water at 20°C
        'pipe_roughness': 0.00015    # Commercial steel
    }
    
    results = calculate_pressure_drop(**parameters)
    
    assert results['total_pressure_drop'] > 0
    assert len(results['sections']) == 1
    assert results['sections'][0]['flow_regime'] == 'Turbulent'

def test_zero_flow():
    """Test that zero flow gives zero pressure drop."""
    pipe_sections = [
        PipeSection(
            diameter=0.1,
            length=10,
            fittings_k=[0],
            elevation_change=0
        )
    ]
    
    parameters = {
        'pipe_sections': pipe_sections,
        'flow_rate': 0,
        'fluid_density': 1000,
        'fluid_viscosity': 0.001,
        'pipe_roughness': 0.00015
    }
    
    results = calculate_pressure_drop(**parameters)
    
    assert results['total_pressure_drop'] == 0
    assert results['sections'][0]['pressure_drop_friction'] == 0
    assert results['sections'][0]['pressure_drop_fittings'] == 0

def test_elevation_only():
    """Test that elevation change gives correct hydrostatic pressure."""
    pipe_sections = [
        PipeSection(
            diameter=0.1,
            length=10,
            fittings_k=[0],
            elevation_change=1  # 1m elevation change
        )
    ]
    
    parameters = {
        'pipe_sections': pipe_sections,
        'flow_rate': 0,
        'fluid_density': 1000,
        'fluid_viscosity': 0.001,
        'pipe_roughness': 0.00015,
        'gravity': 9.81
    }
    
    results = calculate_pressure_drop(**parameters)
    expected_pressure = 1000 * 9.81 * 1  # ρgh
    
    assert abs(results['sections'][0]['pressure_drop_elevation'] - expected_pressure) < 0.1

def test_laminar_flow():
    """Test that low Reynolds number gives laminar flow."""
    pipe_sections = [
        PipeSection(
            diameter=0.1,
            length=1,
            fittings_k=[0],
            elevation_change=0
        )
    ]
    
    parameters = {
        'pipe_sections': pipe_sections,
        'flow_rate': 0.0001,  # Very low flow rate
        'fluid_density': 1000,
        'fluid_viscosity': 0.001,
        'pipe_roughness': 0.00015
    }
    
    results = calculate_pressure_drop(**parameters)
    assert results['sections'][0]['flow_regime'] == 'Laminar'

def test_input_validation():
    """Test that invalid inputs raise appropriate exceptions."""
    pipe_sections = [
        PipeSection(
            diameter=-0.1,  # Invalid negative diameter
            length=10,
            fittings_k=[0],
            elevation_change=0
        )
    ]
    
    parameters = {
        'pipe_sections': pipe_sections,
        'flow_rate': 0.01,
        'fluid_density': 1000,
        'fluid_viscosity': 0.001,
        'pipe_roughness': 0.00015
    }
    
    with pytest.raises(ValueError):
        calculate_pressure_drop(**parameters)

def test_multi_section():
    """Test multiple pipe sections in series."""
    pipe_sections = [
        PipeSection(
            diameter=0.1,
            length=10,
            fittings_k=[0],
            elevation_change=0
        ),
        PipeSection(
            diameter=0.08,
            length=10,
            fittings_k=[0],
            elevation_change=0
        )
    ]
    
    parameters = {
        'pipe_sections': pipe_sections,
        'flow_rate': 0.01,
        'fluid_density': 1000,
        'fluid_viscosity': 0.001,
        'pipe_roughness': 0.00015
    }
    
    results = calculate_pressure_drop(**parameters)
    
    assert len(results['sections']) == 2
    assert results['sections'][1]['pressure_drop_friction'] > results['sections'][0]['pressure_drop_friction']
    assert results['total_pressure_drop'] == sum(section['total_section_pressure_drop'] 
                                               for section in results['sections'])

def test_fitting_losses():
    """Test that fitting losses are calculated correctly."""
    pipe_sections = [
        PipeSection(
            diameter=0.1,
            length=10,
            fittings_k=[0.5],  # Single fitting with K=0.5
            elevation_change=0
        )
    ]
    
    parameters = {
        'pipe_sections': pipe_sections,
        'flow_rate': 0.01,
        'fluid_density': 1000,
        'fluid_viscosity': 0.001,
        'pipe_roughness': 0.00015
    }
    
    results = calculate_pressure_drop(**parameters)
    assert results['sections'][0]['pressure_drop_fittings'] > 0

if __name__ == '__main__':
    pytest.main([__file__])