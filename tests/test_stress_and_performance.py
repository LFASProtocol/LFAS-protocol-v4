"""
LFAS Protocol v4 - Performance and Stress Tests

Tests for protocol performance under high load and extreme conditions.
"""

import unittest
import sys
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lfas import VulnerabilityDetector, CrisisDetector, ProtectionLevel


class TestPerformanceAndStress(unittest.TestCase):
    """Test protocol performance under stress conditions"""
    
    def setUp(self):
        self.detector = VulnerabilityDetector()
        self.crisis_detector = CrisisDetector()
    
    def test_concurrent_detections(self):
        """Test concurrent vulnerability detection requests"""
        test_inputs = [
            "I need help with my business",
            "This is my last hope",
            "I'm desperate for money",
            "Can't take it anymore",
            "Lost my job",
        ] * 20  # 100 total requests
        
        results = []
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.detector.detect, inp) for inp in test_inputs]
            for future in as_completed(futures):
                results.append(future.result())
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 100 detections in reasonable time
        self.assertEqual(len(results), 100)
        self.assertLess(duration, 5.0, f"Took {duration:.2f}s, should be under 5s")
        
        # Verify results are correct
        crisis_count = sum(1 for r in results if r.protection_level == ProtectionLevel.CRISIS)
        self.assertGreater(crisis_count, 0, "Should detect some crisis situations")
    
    def test_large_batch_processing(self):
        """Test processing large batch of inputs"""
        test_inputs = [
            f"Test message number {i} with some crisis language like desperate and last hope"
            for i in range(1000)
        ]
        
        start_time = time.time()
        results = [self.detector.detect(inp) for inp in test_inputs]
        end_time = time.time()
        
        duration = end_time - start_time
        avg_time = duration / len(test_inputs)
        
        self.assertEqual(len(results), 1000)
        self.assertLess(avg_time, 0.01, f"Average {avg_time:.4f}s per detection, should be under 0.01s")
    
    def test_memory_efficiency_repeated_detections(self):
        """Test memory efficiency with repeated detections"""
        # Create a large input that might stress memory
        large_input = "I need help. " * 1000 + " This is my last hope. " * 100
        
        # Run detection multiple times
        for i in range(100):
            result = self.detector.detect(large_input)
            self.assertIsNotNone(result)
            self.assertGreaterEqual(result.triggers_count, 1)
        
        # If we get here without MemoryError, test passes
        self.assertTrue(True)
    
    def test_extreme_input_length(self):
        """Test handling of extremely long inputs"""
        # Create extremely long input (100KB+)
        extreme_input = "Some normal text. " * 5000 + " I'm desperate and this is my last hope. " + "More text. " * 5000
        
        start_time = time.time()
        result = self.detector.detect(extreme_input)
        end_time = time.time()
        
        duration = end_time - start_time
        
        # Should still detect crisis
        self.assertGreaterEqual(result.triggers_count, 2)
        # Should complete in reasonable time
        self.assertLess(duration, 1.0, f"Took {duration:.2f}s for extreme input")
    
    def test_rapid_sequential_detections(self):
        """Test rapid sequential vulnerability checks"""
        test_input = "I'm so desperate, this is my last chance, can't take it anymore"
        
        start_time = time.time()
        for i in range(1000):
            result = self.detector.detect(test_input)
            self.assertEqual(result.protection_level, ProtectionLevel.CRISIS)
        end_time = time.time()
        
        duration = end_time - start_time
        self.assertLess(duration, 2.0, f"1000 detections took {duration:.2f}s, should be under 2s")
    
    def test_crisis_response_generation_performance(self):
        """Test crisis response generation speed"""
        input_text = "I can't take this anymore, thinking about ending it all"
        detection = self.detector.detect(input_text)
        
        start_time = time.time()
        for i in range(100):
            response = self.crisis_detector.assess_crisis(detection)
            self.assertIsNotNone(response)
            self.assertTrue(response.requires_human_escalation)
        end_time = time.time()
        
        duration = end_time - start_time
        avg_time = duration / 100
        self.assertLess(avg_time, 0.001, f"Average {avg_time:.4f}s per response")


class TestRobustnessAndResilience(unittest.TestCase):
    """Test protocol robustness and error handling"""
    
    def setUp(self):
        self.detector = VulnerabilityDetector()
        self.crisis_detector = CrisisDetector()
    
    def test_null_and_none_input(self):
        """Test handling of null/None inputs"""
        # Empty string should work
        result = self.detector.detect("")
        self.assertEqual(result.protection_level, ProtectionLevel.STANDARD)
        self.assertEqual(result.triggers_count, 0)
    
    def test_whitespace_only_input(self):
        """Test handling of whitespace-only input"""
        whitespace_inputs = [
            "   ",
            "\n\n\n",
            "\t\t\t",
            "   \n  \t  ",
        ]
        
        for inp in whitespace_inputs:
            result = self.detector.detect(inp)
            self.assertEqual(result.protection_level, ProtectionLevel.STANDARD)
    
    def test_special_characters_only(self):
        """Test handling of special characters"""
        special_inputs = [
            "!@#$%^&*()",
            "????!!!",
            "----------",
            "==========",
        ]
        
        for inp in special_inputs:
            result = self.detector.detect(inp)
            # Should not crash
            self.assertIsNotNone(result)
    
    def test_binary_and_control_characters(self):
        """Test handling of binary/control characters"""
        binary_input = "Test \x00\x01\x02 message with crisis language: desperate and last hope"
        
        result = self.detector.detect(binary_input)
        # Should still detect crisis despite binary characters
        self.assertIsNotNone(result)
    
    def test_repeated_detector_instantiation(self):
        """Test creating multiple detector instances"""
        detectors = [VulnerabilityDetector() for _ in range(50)]
        
        test_input = "This is my last hope"
        
        for detector in detectors:
            result = detector.detect(test_input)
            self.assertGreaterEqual(result.triggers_count, 1)
    
    def test_detector_reuse_different_inputs(self):
        """Test reusing same detector instance for different input types"""
        inputs = [
            "Normal business question",
            "I lost my job and desperate for money",
            "What's a good investment?",
            "I can't take this anymore",
            "How do I start a blog?",
        ]
        
        for inp in inputs:
            result = self.detector.detect(inp)
            self.assertIsNotNone(result)
            # Verify detector state isn't corrupted between calls
            self.assertIsInstance(result.protection_level, ProtectionLevel)


class TestEdgeCaseInputFormats(unittest.TestCase):
    """Test unusual input formats and encodings"""
    
    def setUp(self):
        self.detector = VulnerabilityDetector()
    
    def test_only_numbers(self):
        """Test numeric-only input"""
        result = self.detector.detect("123456789")
        self.assertEqual(result.protection_level, ProtectionLevel.STANDARD)
    
    def test_urls_and_links(self):
        """Test input with URLs"""
        input_text = "Check out https://example.com I'm desperate and this is my last hope"
        result = self.detector.detect(input_text)
        # Should still detect crisis despite URL
        self.assertGreaterEqual(result.triggers_count, 2)
    
    def test_markdown_formatting(self):
        """Test input with markdown formatting"""
        input_text = "**I'm desperate** and this is my _last hope_. `Can't take it anymore`"
        result = self.detector.detect(input_text)
        self.assertGreaterEqual(result.triggers_count, 3)
    
    def test_html_tags(self):
        """Test input with HTML tags"""
        input_text = "<p>I'm <strong>desperate</strong> and this is my last hope</p>"
        result = self.detector.detect(input_text)
        # Should detect crisis despite HTML tags
        self.assertGreaterEqual(result.triggers_count, 2)
    
    def test_json_formatted_input(self):
        """Test JSON-like formatted input"""
        input_text = '{"message": "I am desperate", "status": "last hope", "feeling": "cant take it anymore"}'
        result = self.detector.detect(input_text)
        self.assertGreaterEqual(result.triggers_count, 3)
    
    def test_code_blocks(self):
        """Test input containing code blocks"""
        input_text = """
        Here's my code:
        ```python
        print("desperate")
        ```
        But actually I'm desperate and this is my last hope
        """
        result = self.detector.detect(input_text)
        self.assertGreaterEqual(result.triggers_count, 2)


def run_stress_test_suite():
    """Run the stress test suite with detailed reporting"""
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    test_classes = [
        TestPerformanceAndStress,
        TestRobustnessAndResilience,
        TestEdgeCaseInputFormats,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*70)
    print("STRESS TEST SUITE SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*70)
    
    return result


if __name__ == "__main__":
    run_stress_test_suite()
