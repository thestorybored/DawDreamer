#!/usr/bin/env python3
"""
Baseline Functionality Test Suite
Part of Story 0.3: Testing Infrastructure Setup

This test suite validates that all essential DawDreamer functionality works
as expected and provides a foundation for developing new VST parameter features.
"""

import os
import pytest
import numpy as np
import dawdreamer as daw


class TestBasicFunctionality:
    """Test basic DawDreamer functionality."""
    
    def test_import_dawdreamer(self):
        """Test that dawdreamer imports correctly."""
        assert daw is not None
        assert hasattr(daw, 'RenderEngine')
    
    def test_render_engine_creation(self):
        """Test RenderEngine can be created with standard parameters."""
        engine = daw.RenderEngine(44100, 512)
        assert engine is not None
        
        # Test basic engine methods
        assert hasattr(engine, 'make_plugin_processor')
        assert hasattr(engine, 'load_graph')
        assert hasattr(engine, 'render')
        assert hasattr(engine, 'get_audio')


class TestPluginLoading:
    """Test plugin loading functionality."""
    
    @pytest.fixture
    def engine(self):
        """Create a RenderEngine for testing."""
        return daw.RenderEngine(44100, 512)
    
    def test_vst3_plugin_loading(self, engine):
        """Test loading VST3 plugins."""
        vst3_plugins = [
            'plugins/TAL-NoiseMaker.vst3',
            'plugins/RoughRider3.vst3',
            'plugins/ValhallaFreqEcho.vst3'
        ]
        
        loaded_plugins = []
        for i, plugin_path in enumerate(vst3_plugins):
            if os.path.exists(plugin_path):
                plugin = engine.make_plugin_processor(f'test_vst3_{i}', plugin_path)
                assert plugin is not None
                loaded_plugins.append(plugin)
        
        # We should have at least one working plugin for further tests
        assert len(loaded_plugins) > 0, "No VST3 plugins could be loaded"
    
    def test_plugin_loading_error_handling(self, engine):
        """Test that plugin loading handles errors gracefully."""
        # Try to load a non-existent plugin
        with pytest.raises(Exception):
            engine.make_plugin_processor('invalid', 'non_existent_plugin.vst3')


class TestParameterExtraction:
    """Test parameter extraction functionality."""
    
    @pytest.fixture(scope="class")
    def loaded_plugin(self):
        """Load a working plugin for parameter testing."""
        self.engine = daw.RenderEngine(44100, 512)
        
        # Try to load the first available VST3 plugin with absolute path
        test_plugins = [
            'plugins/RoughRider3.vst3',  # This has fewer parameters, easier to test
            'plugins/ValhallaFreqEcho.vst3',
            'plugins/TAL-NoiseMaker.vst3'
        ]
        
        for plugin_path in test_plugins:
            abs_path = os.path.abspath(plugin_path)
            if os.path.exists(abs_path):
                try:
                    plugin = self.engine.make_plugin_processor('param_test', abs_path)
                    # Keep reference to engine to prevent cleanup
                    plugin._test_engine = self.engine
                    return plugin
                except Exception as e:
                    print(f"Failed to load {abs_path}: {e}")
                    continue
        
        pytest.skip("No working plugins available for parameter testing")
    
    def test_get_parameters_description(self, loaded_plugin):
        """Test getting parameter descriptions."""
        params = loaded_plugin.get_parameters_description()
        
        assert isinstance(params, list)
        assert len(params) > 0, "Plugin should have at least one parameter"
        
        # Check first parameter structure
        first_param = params[0]
        assert isinstance(first_param, dict)
        
        # Required fields
        required_fields = ['index', 'name', 'isAutomatable', 'defaultValue']
        for field in required_fields:
            assert field in first_param, f"Parameter missing required field: {field}"
    
    def test_parameter_range_extraction(self, loaded_plugin):
        """Test getting parameter range information."""
        params = loaded_plugin.get_parameters_description()
        
        if len(params) > 0:
            # Test range extraction for first parameter
            range_info = loaded_plugin.get_parameter_range(0)
            assert isinstance(range_info, dict)
            assert len(range_info) > 0, "Range info should not be empty"
    
    def test_parameter_value_operations(self, loaded_plugin):
        """Test getting and setting parameter values."""
        params = loaded_plugin.get_parameters_description()
        
        if len(params) > 0:
            # Test getting parameter value
            original_value = loaded_plugin.get_parameter(0)
            assert isinstance(original_value, (int, float))
            
            # Test getting parameter name
            param_name = loaded_plugin.get_parameter_name(0)
            assert isinstance(param_name, str)
            
            # Test getting parameter text
            param_text = loaded_plugin.get_parameter_text(0)
            assert isinstance(param_text, str)
    
    def test_patch_operations(self, loaded_plugin):
        """Test getting and setting patch data."""
        # Get current patch
        patch = loaded_plugin.get_patch()
        assert isinstance(patch, list)
        
        params = loaded_plugin.get_parameters_description()
        if len(params) > 0:
            # Patch should have entries for parameters
            assert len(patch) > 0, "Patch should not be empty if plugin has parameters"
            
            # Each patch entry should be a tuple (index, value)
            for entry in patch[:5]:  # Check first 5 entries
                assert isinstance(entry, tuple)
                assert len(entry) == 2
                assert isinstance(entry[0], int)  # index
                assert isinstance(entry[1], (int, float))  # value


class TestAudioProcessing:
    """Test basic audio processing functionality."""
    
    def test_basic_audio_rendering(self):
        """Test basic audio rendering without plugins."""
        engine = daw.RenderEngine(44100, 512)
        
        # Create a simple oscillator
        osc = engine.make_oscillator_processor("osc", 440.0)
        
        # Load graph and render
        engine.load_graph([(osc, [])])
        engine.render(1.0)  # Render 1 second
        
        # Get audio
        audio = engine.get_audio()
        assert audio is not None
        assert isinstance(audio, np.ndarray)
        assert audio.shape[0] == 2  # Stereo
        assert audio.shape[1] > 0  # Should have samples
        
        # Check that we actually got some audio signal
        assert not np.allclose(audio, 0), "Audio should not be silent"
        assert not np.any(np.isnan(audio)), "Audio should not contain NaN"
    
    def test_plugin_audio_processing(self):
        """Test audio processing with a loaded plugin."""
        engine = daw.RenderEngine(44100, 512)
        
        # Try to load an effect plugin
        effect_plugins = [
            'plugins/RoughRider3.vst3',
            'plugins/ValhallaFreqEcho.vst3'
        ]
        
        plugin = None
        for plugin_path in effect_plugins:
            if os.path.exists(plugin_path):
                try:
                    plugin = engine.make_plugin_processor('effect', plugin_path)
                    break
                except Exception:
                    continue
        
        if plugin is None:
            pytest.skip("No effect plugins available for audio processing test")
        
        # Create audio source
        osc = engine.make_oscillator_processor("osc", 440.0)
        
        # Connect oscillator to plugin
        engine.load_graph([
            (osc, []),
            (plugin, ["osc"])
        ])
        
        # Render audio
        engine.render(0.5)  # Render 0.5 seconds
        audio = engine.get_audio()
        
        # Verify audio output
        assert audio is not None
        assert isinstance(audio, np.ndarray)
        assert audio.shape[0] == 2  # Stereo
        assert audio.shape[1] > 0  # Should have samples
        
        # Check audio quality
        assert not np.any(np.isnan(audio)), "Audio should not contain NaN"
        # Note: Some effects might silence the audio, so we don't check for non-zero


class TestPresetFunctionality:
    """Test existing preset functionality."""
    
    @pytest.fixture
    def loaded_plugin(self):
        """Load a plugin that might support presets."""
        engine = daw.RenderEngine(44100, 512)
        
        # Try VST3 plugins that might have preset support
        test_plugins = [
            'plugins/TAL-NoiseMaker.vst3',
            'plugins/ValhallaFreqEcho.vst3'
        ]
        
        for plugin_path in test_plugins:
            if os.path.exists(plugin_path):
                try:
                    return engine.make_plugin_processor('preset_test', plugin_path)
                except Exception:
                    continue
        
        pytest.skip("No suitable plugins available for preset testing")
    
    def test_state_save_load(self, loaded_plugin):
        """Test basic state save/load functionality."""
        # This is a basic test - actual preset files would need to exist
        # for more comprehensive testing
        
        # Get initial patch
        initial_patch = loaded_plugin.get_patch()
        assert isinstance(initial_patch, list)
        
        # The plugin should have parameter state
        params = loaded_plugin.get_parameters_description()
        if len(params) > 0:
            assert len(initial_patch) > 0


def test_suite_summary():
    """Print summary of test requirements."""
    print("\n" + "="*50)
    print("BASELINE FUNCTIONALITY TEST SUITE SUMMARY")
    print("="*50)
    print("Prerequisites:")
    print("- DawDreamer built and importable")
    print("- At least one working VST3 plugin in tests/plugins/")
    print("- RenderEngine can be created")
    print("- Basic audio processing works")
    print("- Parameter extraction works")
    print("\nIf these tests pass, the environment is ready for")
    print("developing new VST parameter extraction features!")
    print("="*50)


if __name__ == "__main__":
    # Run with pytest for proper test execution
    print("Run this test suite with: python -m pytest test_baseline_functionality.py -v")
    test_suite_summary()