"""
Test Suite for Phase 11: Advanced Debugging & Hardware Integration

Tests cover:
1. Time-Travel Debugging
2. Performance Profiling
3. Hardware Integration
4. IoT Device Management
5. FPGA Synthesis
6. Hardware Debugging
"""

import unittest
from datetime import datetime
import time
from src.hb_lcs.advanced_debugging_hardware import (
    TimeTravelDebugger,
    DebugAction,
    ExecutionSnapshot,
    PerformanceProfiler,
    ProfileMetric,
    HardwareIntegrationManager,
    HardwareTarget,
    IoTProtocol,
    FPGASynthesizer,
    HDLLanguage,
    HardwareDebugger
)


class TestTimeTravelDebugger(unittest.TestCase):
    """Test time-travel debugging functionality."""
    
    def setUp(self):
        self.debugger = TimeTravelDebugger(max_snapshots=100)
        
    def test_start_stop_recording(self):
        """Test starting and stopping recording."""
        self.debugger.start_recording()
        self.assertTrue(self.debugger.recording)
        
        self.debugger.stop_recording()
        self.assertFalse(self.debugger.recording)
        
    def test_record_snapshot(self):
        """Test recording execution snapshots."""
        self.debugger.start_recording()
        
        self.debugger.record_snapshot(
            action=DebugAction.FUNCTION_CALL,
            location="test.py:10:5",
            variables={'x': 42, 'y': "hello"},
            call_stack=['main', 'foo'],
            memory_usage=1024
        )
        
        self.assertEqual(len(self.debugger.snapshots), 1)
        snapshot = self.debugger.snapshots[0]
        self.assertEqual(snapshot.action, DebugAction.FUNCTION_CALL)
        self.assertEqual(snapshot.variables['x'], 42)
        self.assertEqual(len(snapshot.call_stack), 2)
        
    def test_step_forward_backward(self):
        """Test stepping through execution history."""
        self.debugger.start_recording()
        
        # Record multiple snapshots
        for i in range(5):
            self.debugger.record_snapshot(
                action=DebugAction.VARIABLE_ASSIGN,
                location=f"test.py:{i}:0",
                variables={'i': i},
                call_stack=['main'],
                memory_usage=1000
            )
            
        # Step forward
        self.debugger.current_step = 0
        snapshot = self.debugger.step_forward()
        self.assertIsNotNone(snapshot)
        self.assertEqual(self.debugger.current_step, 1)
        
        # Step backward
        snapshot = self.debugger.step_backward()
        self.assertEqual(self.debugger.current_step, 0)
        
    def test_jump_to_step(self):
        """Test jumping to specific step."""
        self.debugger.start_recording()
        
        for i in range(10):
            self.debugger.record_snapshot(
                action=DebugAction.LOOP_ITERATION,
                location="test.py:5:0",
                variables={'i': i},
                call_stack=['main'],
                memory_usage=1000
            )
            
        snapshot = self.debugger.jump_to_step(5)
        self.assertIsNotNone(snapshot)
        self.assertEqual(snapshot.variables['i'], 5)
        self.assertEqual(self.debugger.current_step, 5)
        
    def test_breakpoints(self):
        """Test breakpoint management."""
        self.debugger.add_breakpoint("test.py:10", "x > 5")
        self.assertIn("test.py:10", self.debugger.breakpoints)
        
        bp = self.debugger.breakpoints["test.py:10"]
        self.assertEqual(bp.condition, "x > 5")
        self.assertTrue(bp.enabled)
        
        self.debugger.remove_breakpoint("test.py:10")
        self.assertNotIn("test.py:10", self.debugger.breakpoints)
        
    def test_watch_expressions(self):
        """Test watch expression functionality."""
        self.debugger.add_watch("x")
        self.debugger.add_watch("y")
        
        self.assertEqual(len(self.debugger.watch_expressions), 2)
        
        snapshot = ExecutionSnapshot(
            timestamp=datetime.now(),
            step_number=0,
            action=DebugAction.VARIABLE_ASSIGN,
            location="test.py:1:0",
            variables={'x': 10, 'y': 20, 'z': 30},
            call_stack=['main'],
            memory_usage=1000,
            execution_time=0.1
        )
        
        values = self.debugger.get_watch_values(snapshot)
        self.assertEqual(values['x'], 10)
        self.assertEqual(values['y'], 20)
        self.assertNotIn('z', values)
        
    def test_find_snapshots_by_action(self):
        """Test finding snapshots by action type."""
        self.debugger.start_recording()
        
        self.debugger.record_snapshot(
            DebugAction.FUNCTION_CALL, "test.py:1:0", {}, [], 1000
        )
        self.debugger.record_snapshot(
            DebugAction.VARIABLE_ASSIGN, "test.py:2:0", {}, [], 1000
        )
        self.debugger.record_snapshot(
            DebugAction.FUNCTION_CALL, "test.py:3:0", {}, [], 1000
        )
        
        calls = self.debugger.find_snapshots_by_action(DebugAction.FUNCTION_CALL)
        self.assertEqual(len(calls), 2)
        
    def test_execution_timeline(self):
        """Test execution timeline generation."""
        self.debugger.start_recording()
        
        for i in range(3):
            self.debugger.record_snapshot(
                DebugAction.VARIABLE_ASSIGN,
                f"test.py:{i}:0",
                {'i': i},
                ['main'],
                1000
            )
            
        timeline = self.debugger.get_execution_timeline()
        self.assertEqual(len(timeline), 3)
        self.assertEqual(timeline[0]['step'], 0)
        self.assertEqual(timeline[1]['step'], 1)


class TestPerformanceProfiler(unittest.TestCase):
    """Test performance profiling functionality."""
    
    def setUp(self):
        self.profiler = PerformanceProfiler()
        
    def test_start_stop_profiling(self):
        """Test profiling a code section."""
        self.profiler.start_profiling("test_function", "test.py:10")
        time.sleep(0.01)  # Simulate work
        self.profiler.stop_profiling("test_function")
        
        self.assertEqual(len(self.profiler.profiles), 1)
        profile = self.profiler.profiles[0]
        self.assertEqual(profile.name, "test_function")
        self.assertGreater(profile.value, 0)
        
    def test_function_stats(self):
        """Test function statistics tracking."""
        # Profile function multiple times
        for _ in range(3):
            self.profiler.start_profiling("foo", "test.py:5")
            time.sleep(0.005)
            self.profiler.stop_profiling("foo")
            
        stats = self.profiler.function_stats['foo']
        self.assertEqual(stats['call_count'], 3)
        self.assertGreater(stats['total_time'], 0)
        
    def test_get_hotspots(self):
        """Test hotspot detection."""
        # Create some profiling data
        self.profiler.start_profiling("slow_function", "test.py:10")
        time.sleep(0.02)
        self.profiler.stop_profiling("slow_function")
        
        self.profiler.start_profiling("fast_function", "test.py:20")
        time.sleep(0.001)
        self.profiler.stop_profiling("fast_function")
        
        hotspots = self.profiler.get_hotspots(top_n=2)
        self.assertEqual(len(hotspots), 2)
        
        # Slowest should be first
        self.assertEqual(hotspots[0].function_name, "slow_function")
        self.assertGreater(hotspots[0].cpu_time, hotspots[1].cpu_time)
        
    def test_hotspot_recommendations(self):
        """Test performance recommendations."""
        # Create function with many calls
        for _ in range(1001):
            self.profiler.start_profiling("busy_function", "test.py:30")
            self.profiler.stop_profiling("busy_function")
            
        hotspots = self.profiler.get_hotspots()
        self.assertGreater(len(hotspots[0].recommendations), 0)
        
    def test_get_summary(self):
        """Test profiling summary."""
        self.profiler.start_profiling("func1", "test.py:10")
        time.sleep(0.01)
        self.profiler.stop_profiling("func1")
        
        self.profiler.start_profiling("func2", "test.py:20")
        time.sleep(0.01)
        self.profiler.stop_profiling("func2")
        
        summary = self.profiler.get_summary()
        self.assertGreater(summary['total_cpu_time'], 0)
        self.assertEqual(summary['total_profiles'], 2)
        self.assertEqual(summary['unique_functions'], 2)
        
    def test_flamegraph_data(self):
        """Test flamegraph data generation."""
        self.profiler.start_profiling("main", "test.py:1")
        time.sleep(0.01)
        self.profiler.stop_profiling("main")
        
        data = self.profiler.generate_flamegraph_data()
        self.assertGreater(len(data), 0)
        self.assertIn('name', data[0])
        self.assertIn('value', data[0])


class TestHardwareIntegration(unittest.TestCase):
    """Test hardware integration functionality."""
    
    def setUp(self):
        self.manager = HardwareIntegrationManager()
        
    def test_register_device(self):
        """Test IoT device registration."""
        device = self.manager.register_device(
            device_id="esp32-001",
            name="Temperature Sensor",
            hardware=HardwareTarget.ESP32,
            protocol=IoTProtocol.MQTT,
            ip_address="192.168.1.100"
        )
        
        self.assertEqual(device.device_id, "esp32-001")
        self.assertEqual(device.hardware, HardwareTarget.ESP32)
        self.assertEqual(device.status, "registered")
        self.assertIn("esp32-001", self.manager.devices)
        
    def test_update_device_status(self):
        """Test device status updates."""
        self.manager.register_device(
            "device-1", "Test", HardwareTarget.ARDUINO, IoTProtocol.HTTP
        )
        
        self.manager.update_device_status("device-1", "online")
        device = self.manager.devices["device-1"]
        self.assertEqual(device.status, "online")
        self.assertIsNotNone(device.last_seen)
        
    def test_get_online_devices(self):
        """Test getting online devices."""
        self.manager.register_device(
            "device-1", "D1", HardwareTarget.ESP32, IoTProtocol.MQTT
        )
        self.manager.register_device(
            "device-2", "D2", HardwareTarget.ARDUINO, IoTProtocol.HTTP
        )
        
        self.manager.update_device_status("device-1", "online")
        
        online = self.manager.get_online_devices()
        self.assertEqual(len(online), 1)
        self.assertEqual(online[0].device_id, "device-1")
        
    def test_hardware_configs(self):
        """Test hardware configurations."""
        esp32_config = self.manager.hardware_configs[HardwareTarget.ESP32]
        self.assertEqual(esp32_config.cpu_frequency, 240)
        self.assertGreater(esp32_config.memory_size, 0)
        self.assertIn(IoTProtocol.MQTT, esp32_config.protocols)
        
        arduino_config = self.manager.hardware_configs[HardwareTarget.ARDUINO]
        self.assertEqual(arduino_config.cpu_frequency, 16)
        
    def test_deploy_to_device(self):
        """Test code deployment to device."""
        self.manager.register_device(
            "esp32-test", "Test ESP32", HardwareTarget.ESP32, IoTProtocol.MQTT
        )
        
        result = self.manager.deploy_to_device(
            "esp32-test",
            "digitalWrite(LED_PIN, HIGH);"
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['device_id'], "esp32-test")
        self.assertGreater(result['code_size'], 0)
        
    def test_deploy_to_nonexistent_device(self):
        """Test deployment to non-existent device."""
        result = self.manager.deploy_to_device("fake-device", "code")
        self.assertFalse(result['success'])
        self.assertIn('error', result)
        
    def test_generate_embedded_code(self):
        """Test embedded code generation."""
        config = self.manager.hardware_configs[HardwareTarget.ESP32]
        code = self.manager._generate_embedded_code("// user code", config)
        
        self.assertIn("esp32", code.lower())
        self.assertIn("#include", code)
        self.assertIn("int main(void)", code)
        self.assertIn("// user code", code)


class TestFPGASynthesizer(unittest.TestCase):
    """Test FPGA synthesis functionality."""
    
    def setUp(self):
        self.synthesizer = FPGASynthesizer(HDLLanguage.VERILOG)
        
    def test_create_module(self):
        """Test FPGA module creation."""
        module = self.synthesizer.create_module(
            name="adder",
            inputs=[("a", 8), ("b", 8)],
            outputs=[("sum", 8), ("carry", 1)],
            logic="assign {carry, sum} = a + b;",
            clock_freq=100
        )
        
        self.assertEqual(module.name, "adder")
        self.assertEqual(len(module.inputs), 2)
        self.assertEqual(len(module.outputs), 2)
        self.assertEqual(module.clock_frequency, 100)
        
    def test_generate_verilog(self):
        """Test Verilog code generation."""
        module = self.synthesizer.create_module(
            name="counter",
            inputs=[("clk", 1), ("reset", 1)],
            outputs=[("count", 8)],
            logic="always @(posedge clk) count <= count + 1;",
            clock_freq=50
        )
        
        verilog = self.synthesizer.generate_verilog(module)
        
        self.assertIn("module counter", verilog)
        self.assertIn("input [0:0] clk", verilog)
        self.assertIn("output [7:0] count", verilog)
        self.assertIn("endmodule", verilog)
        self.assertIn("always @(posedge clk)", verilog)
        
    def test_estimate_resources(self):
        """Test FPGA resource estimation."""
        module = self.synthesizer.create_module(
            name="multiplier",
            inputs=[("a", 16), ("b", 16)],
            outputs=[("product", 32)],
            logic="assign product = a * b;",
            clock_freq=100
        )
        
        resources = self.synthesizer.estimate_resources(module)
        
        self.assertIn('luts', resources)
        self.assertIn('flip_flops', resources)
        self.assertIn('io_pins', resources)
        self.assertGreater(resources['luts'], 0)
        self.assertEqual(resources['io_pins'], 3)  # 2 inputs + 1 output
        
    def test_multiple_modules(self):
        """Test managing multiple FPGA modules."""
        self.synthesizer.create_module(
            "mod1", [("in", 8)], [("out", 8)], "assign out = in;", 100
        )
        self.synthesizer.create_module(
            "mod2", [("in", 4)], [("out", 4)], "assign out = ~in;", 100
        )
        
        self.assertEqual(len(self.synthesizer.modules), 2)


class TestHardwareDebugger(unittest.TestCase):
    """Test hardware debugging functionality."""
    
    def setUp(self):
        self.debugger = HardwareDebugger("esp32-001")
        
    def test_connect_disconnect(self):
        """Test debugger connection."""
        self.assertFalse(self.debugger.connected)
        
        result = self.debugger.connect()
        self.assertTrue(result)
        self.assertTrue(self.debugger.connected)
        
        self.debugger.disconnect()
        self.assertFalse(self.debugger.connected)
        
    def test_set_breakpoint(self):
        """Test setting breakpoints."""
        self.debugger.connect()
        self.debugger.set_breakpoint(0x08000100)
        
        self.assertIn(0x08000100, self.debugger.breakpoints)
        
    def test_read_memory(self):
        """Test reading device memory."""
        self.debugger.connect()
        data = self.debugger.read_memory(0x20000000, 16)
        
        self.assertEqual(len(data), 16)
        self.assertIsInstance(data, bytes)
        
    def test_read_memory_disconnected(self):
        """Test reading memory when disconnected."""
        data = self.debugger.read_memory(0x20000000, 16)
        self.assertEqual(len(data), 0)
        
    def test_get_registers(self):
        """Test getting CPU registers."""
        self.debugger.connect()
        registers = self.debugger.get_registers()
        
        self.assertIn('R0', registers)
        self.assertIn('PC', registers)
        self.assertIn('SP', registers)
        
    def test_get_stack_trace(self):
        """Test getting call stack."""
        self.debugger.connect()
        stack = self.debugger.get_stack_trace()
        
        self.assertGreater(len(stack), 0)
        self.assertIn('function', stack[0])
        self.assertIn('address', stack[0])
        self.assertIn('file', stack[0])


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple components."""
    
    def test_profile_and_debug(self):
        """Test combining profiling with debugging."""
        profiler = PerformanceProfiler()
        debugger = TimeTravelDebugger()
        
        # Start both systems
        profiler.start_profiling("test_function", "test.py:10")
        debugger.start_recording()
        
        # Simulate some work
        for i in range(5):
            debugger.record_snapshot(
                DebugAction.LOOP_ITERATION,
                f"test.py:10:{i}",
                {'i': i},
                ['main', 'test_function'],
                1024
            )
            
        profiler.stop_profiling("test_function")
        debugger.stop_recording()
        
        # Verify both systems captured data
        self.assertGreater(len(profiler.profiles), 0)
        self.assertEqual(len(debugger.snapshots), 5)
        
    def test_hardware_deployment_with_profiling(self):
        """Test hardware deployment with performance profiling."""
        manager = HardwareIntegrationManager()
        profiler = PerformanceProfiler()
        
        # Register device
        manager.register_device(
            "test-device", "Test", HardwareTarget.ESP32, IoTProtocol.MQTT
        )
        
        # Profile deployment
        profiler.start_profiling("deploy", "deploy.py:1")
        result = manager.deploy_to_device("test-device", "test_code();")
        profiler.stop_profiling("deploy")
        
        self.assertTrue(result['success'])
        self.assertGreater(len(profiler.profiles), 0)


if __name__ == '__main__':
    unittest.main()
