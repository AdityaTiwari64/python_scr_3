"""
Unit tests for the Python Student Competence Analyzer
"""

import unittest
import sys
import os

# Add src directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_dir)

try:
    from competence_analyse import StudentCodeAnalyzer, CodeMetrics
except ImportError:
    # Alternative import method if above fails
    import importlib.util
    spec = importlib.util.spec_from_file_location("competence_analyse", 
                                                 os.path.join(src_dir, "competence_analyse.py"))
    competence_analyse = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(competence_analyse)
    StudentCodeAnalyzer = competence_analyse.StudentCodeAnalyzer
    CodeMetrics = competence_analyse.CodeMetrics

class TestStudentCodeAnalyzer(unittest.TestCase):
    """Test cases for the competence analyzer"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.analyzer = StudentCodeAnalyzer()
    
    def test_analyzer_initialization(self):
        """Test that analyzer initializes correctly"""
        self.assertIsInstance(self.analyzer, StudentCodeAnalyzer)
        self.assertIn('novice', self.analyzer.skill_levels)
        self.assertIn('advanced', self.analyzer.skill_levels)
    
    def test_syntax_error_handling(self):
        """Test handling of code with syntax errors"""
        code_with_error = """
def broken_function()
    return "missing colon"
        """
        
        metrics, feedback = self.analyzer.assess_code(code_with_error)
        
        # Should detect syntax error
        self.assertEqual(metrics.syntax_score, 0.0)
        self.assertEqual(metrics.structure_score, 0.0)
        
        # Should provide appropriate feedback
        self.assertGreater(len(feedback), 0)
        self.assertTrue(any('syntax' in prompt.lower() for prompt in feedback))
    
    def test_valid_simple_code(self):
        """Test analysis of simple valid code"""
        simple_code = """
def add(a, b):
    return a + b

result = add(5, 3)
print(result)
        """
        
        metrics, feedback = self.analyzer.assess_code(simple_code)
        
        # Should have perfect syntax
        self.assertEqual(metrics.syntax_score, 1.0)
        
        # Should have some structure
        self.assertGreater(metrics.structure_score, 0.0)
        
        # Should provide feedback
        self.assertGreater(len(feedback), 0)
    
    def test_skill_level_progression(self):
        """Test that skill levels progress correctly"""
        codes = {
            'simple': "x = 5\nprint(x)",
            'with_function': """
def greet(name):
    return f"Hello {name}"
print(greet("Alice"))
            """,
            'with_class': """
class Person:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return f"I am {self.name}"

p = Person("Bob")
print(p.speak())
            """,
            'advanced': """
from functools import wraps

def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def advanced_func():
    pass
            """
        }
        
        scores = []
        for level, code in codes.items():
            metrics, _ = self.analyzer.assess_code(code)
            scores.append(metrics.total_score)
        
        # Scores should generally increase with complexity
        # (though not strictly monotonic due to different aspects)
        self.assertGreater(scores[-1], scores[0])  # Advanced > Simple
    
    def test_code_structure_parsing(self):
        """Test AST structure parsing"""
        complex_code = """
class Calculator:
    def add(self, a, b):
        return a + b
    
    def process_list(self, numbers):
        result = []
        for num in numbers:
            if num > 0:
                result.append(num * 2)
        return result

calc = Calculator()
try:
    result = calc.process_list([1, -2, 3, 4])
except Exception as e:
    print(f"Error: {e}")
        """
        
        elements = self.analyzer.parse_code_structure(complex_code)
        
        # Should identify various code constructs
        self.assertGreater(elements['classes'], 0)
        self.assertGreater(elements['functions'], 0)
        self.assertGreater(elements['loops'], 0)
        self.assertGreater(elements['conditionals'], 0)
        self.assertGreater(elements['try_blocks'], 0)
    
    def test_skill_level_determination(self):
        """Test skill level classification"""
        test_cases = [
            ({'has_syntax_error': True}, 'novice'),
            ({'functions': 0, 'classes': 0, 'loops': 1}, 'developing'),
            ({'functions': 2, 'classes': 0, 'loops': 1}, 'proficient'),
            ({'functions': 1, 'classes': 2, 'try_blocks': 1}, 'advanced')
        ]
        
        for elements, expected_level in test_cases:
            level = self.analyzer.determine_skill_level(elements)
            self.assertEqual(level, expected_level, 
                           f"Expected {expected_level} for {elements}, got {level}")
    
    def test_feedback_generation(self):
        """Test that appropriate feedback is generated for different levels"""
        test_codes = [
            ("def broken()", 'novice'),  # Syntax error
            ("def simple(): pass", 'developing'),  # Simple function
            ("""
class Test:
    def method(self): 
        return "test"
            """, 'proficient'),  # Class usage
            ("""
@property
def advanced_feature(self):
    return self._value
            """, 'advanced')  # Advanced features
        ]
        
        for code, expected_level in test_codes:
            metrics, feedback = self.analyzer.assess_code(code)
            
            # Should generate feedback
            self.assertGreater(len(feedback), 0)
            
            # Feedback should be strings
            for prompt in feedback:
                self.assertIsInstance(prompt, str)
                self.assertGreater(len(prompt), 10)  # Reasonable length
    
    def test_metrics_data_class(self):
        """Test CodeMetrics data class"""
        metrics = CodeMetrics(
            syntax_score=1.0,
            structure_score=0.8,
            concept_score=0.7,
            quality_score=0.6,
            total_score=0.75
        )
        
        self.assertEqual(metrics.syntax_score, 1.0)
        self.assertEqual(metrics.structure_score, 0.8)
        self.assertEqual(metrics.concept_score, 0.7)
        self.assertEqual(metrics.quality_score, 0.6)
        self.assertEqual(metrics.total_score, 0.75)
    
    def test_empty_code_handling(self):
        """Test handling of empty or whitespace-only code"""
        empty_cases = ["", "   ", "\n\n", "# just a comment"]
        
        for empty_code in empty_cases:
            try:
                metrics, feedback = self.analyzer.assess_code(empty_code)
                # Should handle gracefully without crashing
                self.assertIsInstance(metrics, CodeMetrics)
                self.assertIsInstance(feedback, list)
            except Exception as e:
                self.fail(f"Failed to handle empty code '{empty_code}': {e}")
    
    def test_large_code_handling(self):
        """Test handling of larger code samples"""
        large_code = """
# Large code sample to test performance
class DataProcessor:
    def __init__(self):
        self.data = []
    
    def load_data(self, filename):
        try:
            with open(filename, 'r') as f:
                for line in f:
                    self.data.append(line.strip())
        except FileNotFoundError:
            print("File not found")
    
    def process_data(self):
        processed = []
        for item in self.data:
            if len(item) > 5:
                processed.append(item.upper())
        return processed
    
    def save_results(self, results, output_file):
        with open(output_file, 'w') as f:
            for result in results:
                f.write(result + '\\n')

def main():
    processor = DataProcessor()
    processor.load_data('input.txt')
    results = processor.process_data()
    processor.save_results(results, 'output.txt')
    
    # List comprehension example
    filtered = [x for x in results if 'TEST' in x]
    
    # Dictionary comprehension
    counts = {item: len(item) for item in filtered}
    
    return counts

if __name__ == "__main__":
    main()
        """
        
        metrics, feedback = self.analyzer.assess_code(large_code)
        
        # Should handle large code without issues
        self.assertIsInstance(metrics, CodeMetrics)
        self.assertIsInstance(feedback, list)
        self.assertGreater(len(feedback), 0)

class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflow"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = StudentCodeAnalyzer()
    
    def test_full_analysis_workflow(self):
        """Test complete analysis workflow"""
        sample_code = """
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

# Test the function
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    result = factorial(num)
    print(f"factorial({num}) = {result}")
        """
        
        # Should complete without errors
        metrics, feedback = self.analyzer.assess_code(sample_code)
        
        # Verify all components work together
        self.assertIsInstance(metrics, CodeMetrics)
        self.assertIsInstance(feedback, list)
        
        # Verify reasonable scores
        self.assertGreaterEqual(metrics.syntax_score, 0.0)
        self.assertLessEqual(metrics.syntax_score, 1.0)
        self.assertGreaterEqual(metrics.total_score, 0.0)
        self.assertLessEqual(metrics.total_score, 1.0)
        
        # Verify feedback quality
        self.assertGreater(len(feedback), 0)
        for prompt in feedback:
            self.assertIsInstance(prompt, str)
            self.assertGreater(len(prompt.strip()), 0)

def run_tests():
    """Run all tests with detailed output"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestStudentCodeAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"\nSuccess Rate: {success_rate:.1f}%")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    # Run tests when script is executed directly
    success = run_tests()
    sys.exit(0 if success else 1)