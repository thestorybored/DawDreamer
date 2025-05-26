#!/usr/bin/env python3
"""
Plugin Discovery and Parameter Testing Script
Part of Story 0.2: Plugin Environment Testing
"""

import os
import dawdreamer as daw


def test_plugin_loading():
    """Test loading available plugins and extracting parameters."""
    
    # Available test plugins
    plugin_paths = [
        'plugins/TAL-NoiseMaker.vst3',
        'plugins/RoughRider3.vst3', 
        'plugins/ValhallaFreqEcho.vst3',
        'plugins/TAL-NoiseMaker.component',
        'plugins/RoughRider3.component'
    ]
    
    engine = daw.RenderEngine(44100, 512)
    working_plugins = []
    
    print("=== DawDreamer Plugin Discovery Test ===")
    print(f"Audio Engine: {engine}")
    print()
    
    for i, path in enumerate(plugin_paths):
        if os.path.exists(path):
            try:
                plugin_name = f"test_plugin_{i}"
                plugin = engine.make_plugin_processor(plugin_name, path)
                
                print(f"✓ Successfully loaded: {path}")
                
                # Test parameter extraction
                params = plugin.get_parameters_description()
                print(f"  Parameters found: {len(params)}")
                
                if len(params) > 0:
                    # Show first few parameters
                    for j, param in enumerate(params[:3]):
                        name = param.get('name', 'Unnamed')
                        if name:  # Skip empty names
                            print(f"    [{j}] {name}: {param.get('text', 'N/A')}")
                    
                    if len(params) > 3:
                        print(f"    ... and {len(params) - 3} more parameters")
                
                # Test parameter range extraction
                if len(params) > 0:
                    range_info = plugin.get_parameter_range(0)
                    print(f"  Range info for param 0: {range_info}")
                
                # Test parameter value operations
                if len(params) > 0:
                    original_value = plugin.get_parameter(0)
                    print(f"  Original value: {original_value}")
                    
                working_plugins.append({
                    'path': path,
                    'plugin': plugin,
                    'param_count': len(params)
                })
                
                print()
                
            except Exception as e:
                print(f"✗ Failed to load {path}: {e}")
                print()
        else:
            print(f"- Plugin not found: {path}")
            print()
    
    print(f"=== Summary ===")
    print(f"Working plugins: {len(working_plugins)}")
    for p in working_plugins:
        print(f"  - {p['path']}: {p['param_count']} parameters")
    
    return working_plugins


def test_parameter_operations(plugin_info):
    """Test parameter operations on a loaded plugin."""
    
    if not plugin_info:
        print("No working plugins available for parameter testing")
        return
    
    print("\n=== Parameter Operation Tests ===")
    
    # Use the first working plugin
    test_plugin = plugin_info[0]
    plugin = test_plugin['plugin']
    path = test_plugin['path']
    
    print(f"Testing with: {path}")
    
    try:
        # Get all parameters
        params = plugin.get_parameters_description()
        
        if len(params) == 0:
            print("No parameters available for testing")
            return
        
        # Find a good parameter to test (not empty name, automatable)
        test_param_idx = 0
        for i, param in enumerate(params):
            if param.get('name') and param.get('isAutomatable', True):
                test_param_idx = i
                break
        
        test_param = params[test_param_idx]
        print(f"Testing parameter {test_param_idx}: {test_param.get('name', 'Unnamed')}")
        
        # Test get/set parameter
        original_value = plugin.get_parameter(test_param_idx)
        print(f"  Original value: {original_value}")
        
        # Test parameter text
        param_text = plugin.get_parameter_text(test_param_idx)
        print(f"  Parameter text: {param_text}")
        
        # Test parameter name
        param_name = plugin.get_parameter_name(test_param_idx)
        print(f"  Parameter name: {param_name}")
        
        # Test patch operations
        patch = plugin.get_patch()
        print(f"  Full patch has {len(patch)} entries")
        
        print("✓ All parameter operations successful")
        
    except Exception as e:
        print(f"✗ Parameter operation failed: {e}")


def main():
    """Main test function."""
    
    # Change to tests directory if not already there
    if not os.path.exists('plugins'):
        print("Error: plugins directory not found. Run this from the tests/ directory.")
        return
    
    # Test plugin loading
    working_plugins = test_plugin_loading()
    
    # Test parameter operations if we have working plugins
    if working_plugins:
        test_parameter_operations(working_plugins)
    else:
        print("No plugins loaded successfully - parameter testing skipped")
    
    print("\n=== Plugin Discovery Test Complete ===")


if __name__ == "__main__":
    main()