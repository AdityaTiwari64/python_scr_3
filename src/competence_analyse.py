"""
Python Student Code Competence Analyzer
Evaluates student programming skills and generates educational feedback
"""

import ast
import sys
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class CodeMetrics:
    """Student code assessment metrics"""
    syntax_score: float
    structure_score: float
    concept_score: float
    quality_score: float
    total_score: float

class StudentCodeAnalyzer:
    """Analyzes Python code to assess student programming competence"""
    
    def __init__(self):
        # Define skill level indicators
        self.skill_levels = {
            'novice': ['variables', 'print', 'input', 'basic_operators'],
            'developing': ['functions', 'conditionals', 'loops', 'lists'],
            'proficient': ['classes', 'exceptions', 'file_ops', 'dictionaries'],
            'advanced': ['decorators', 'generators', 'context_mgrs', 'metaclasses']
        }
    
    def parse_code_structure(self, code: str) -> Dict:
        """Parse code and extract structural elements"""
        try:
            tree = ast.parse(code.strip())
        except SyntaxError as err:
            return {'has_syntax_error': True, 'error_details': str(err)}
        
        # Count different code constructs
        elements = {
            'functions': 0, 'classes': 0, 'loops': 0, 'conditionals': 0,
            'try_blocks': 0, 'comprehensions': 0, 'imports': 0
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                elements['functions'] += 1
            elif isinstance(node, ast.ClassDef):
                elements['classes'] += 1
            elif isinstance(node, (ast.For, ast.While)):
                elements['loops'] += 1
            elif isinstance(node, ast.If):
                elements['conditionals'] += 1
            elif isinstance(node, (ast.Try, ast.ExceptHandler)):
                elements['try_blocks'] += 1
            elif isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)):
                elements['comprehensions'] += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                elements['imports'] += 1
        
        return elements
    
    def determine_skill_level(self, code_elements: Dict) -> str:
        """Assess student skill level based on code complexity"""
        if code_elements.get('has_syntax_error'):
            return 'novice'
        
        # Calculate complexity indicators
        advanced_count = code_elements.get('classes', 0) + code_elements.get('try_blocks', 0)
        intermediate_count = code_elements.get('functions', 0) + code_elements.get('comprehensions', 0)
        basic_count = code_elements.get('loops', 0) + code_elements.get('conditionals', 0)
        
        # Determine level based on feature usage
        if advanced_count >= 2 or code_elements.get('comprehensions', 0) >= 2:
            return 'advanced'
        elif intermediate_count >= 2 or (intermediate_count >= 1 and basic_count >= 3):
            return 'proficient'
        elif basic_count >= 1 or intermediate_count >= 1:
            return 'developing'
        else:
            return 'novice'
    
    def create_feedback_prompts(self, code: str, skill_level: str, code_elements: Dict) -> List[str]:
        """Generate educational prompts tailored to student level"""
        feedback = []
        
        if skill_level == 'novice':
            if code_elements.get('has_syntax_error'):
                feedback.extend([
                    "Check your code line by line - which line looks different from Python examples?",
                    "Are all your parentheses, brackets, and colons in the right places?",
                    "Look for syntax errors - missing colons, incorrect indentation, or typos in keywords."
                ])
            else:
                feedback.extend([
                    "Try using more descriptive names for your variables.",
                    "Walk through your code with a sample input - does it do what you expect?"
                ])
        
        elif skill_level == 'developing':
            feedback.extend([
                "Would breaking this into smaller functions make it easier to understand?",
                "What happens if someone gives your program unexpected input?",
                "How would you explain what this code does to another student?"
            ])
        
        elif skill_level == 'proficient':
            feedback.extend([
                "Are there any programming patterns that could make this code cleaner?",
                "How would this code perform with much larger inputs?",
                "What parts of this code might be hard for someone else to modify?"
            ])
        
        else:  # advanced
            feedback.extend([
                "Could you restructure this to follow any well-known design patterns?",
                "How does your solution handle edge cases and potential failures?",
                "What would you change if this code needed to handle 1000x more data?"
            ])
        
        return feedback
    
    def assess_code(self, code: str) -> Tuple[CodeMetrics, List[str]]:
        """Main method to evaluate student code and generate feedback"""
        code_elements = self.parse_code_structure(code)
        skill_level = self.determine_skill_level(code_elements)
        feedback = self.create_feedback_prompts(code, skill_level, code_elements)
        
        # Calculate scores
        if code_elements.get('has_syntax_error'):
            syntax_score = 0.0
            structure_score = 0.0
        else:
            syntax_score = 1.0
            # Sum only numeric values for structure scoring
            valid_counts = [v for k, v in code_elements.items() 
                          if isinstance(v, int) and k != 'has_syntax_error']
            structure_score = min(1.0, sum(valid_counts) / 8.0)
        
        # Map skill levels to scores
        level_scores = {'novice': 0.25, 'developing': 0.5, 'proficient': 0.75, 'advanced': 1.0}
        concept_score = level_scores[skill_level]
        quality_score = structure_score * concept_score
        total_score = (syntax_score + structure_score + concept_score + quality_score) / 4
        
        metrics = CodeMetrics(
            syntax_score=syntax_score,
            structure_score=structure_score,
            concept_score=concept_score,
            quality_score=quality_score,
            total_score=total_score
        )
        
        return metrics, feedback

def run_demo():
    """Test the analyzer with sample student submissions"""
    analyzer = StudentCodeAnalyzer()
    
    # Sample code submissions
    test_submissions = [
        # Novice level - missing colon
        """
def area_circle(r)
    return 3.14159 * r * r
print(area_circle(5))
        """,
        
        # Developing level
        """
class SimpleCalc:
    def __init__(self):
        self.memory = []
    
    def add_nums(self, x, y):
        result = x + y
        self.memory.append(f"{x} + {y} = {result}")
        return result
    
    def show_history(self):
        return self.memory

my_calc = SimpleCalc()
answer = my_calc.add_nums(10, 15)
print(f"Result: {answer}")
        """,
        
        # Advanced level
        """
from functools import wraps
import time

def timing_decorator(max_retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    elapsed = time.time() - start_time
                    print(f"Function completed in {elapsed:.3f}s")
                    return result
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(0.5)
        return wrapper
    return decorator

@timing_decorator(max_retries=2)
def process_data(data):
    if not data:
        raise ValueError("No data provided")
    return [x**2 for x in data if x > 0]
        """
    ]
    
    for idx, submission in enumerate(test_submissions, 1):
        print(f"\n--- Student Submission {idx} Analysis ---")
        
        try:
            metrics, prompts = analyzer.assess_code(submission)
            
            print("Assessment Results:")
            print(f"  Syntax: {metrics.syntax_score:.2f}")
            print(f"  Structure: {metrics.structure_score:.2f}")
            print(f"  Concepts: {metrics.concept_score:.2f}")
            print(f"  Quality: {metrics.quality_score:.2f}")
            print(f"  Overall: {metrics.total_score:.2f}")
            
            print("\nFeedback Questions:")
            for i, prompt in enumerate(prompts, 1):
                print(f"  {i}. {prompt}")
                
        except Exception as e:
            print(f"Analysis failed: {e}")

if __name__ == "__main__":
    run_demo()