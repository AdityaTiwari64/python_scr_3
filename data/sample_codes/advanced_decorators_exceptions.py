# Advanced level - decorators, exceptions, file handling
import functools
import json
from typing import List, Dict

def validate_input(func):
    """Decorator to validate function inputs"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except (ValueError, TypeError) as e:
            print(f"Input validation error in {func.__name__}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in {func.__name__}: {e}")
            raise
    return wrapper

class DataProcessor:
    """Advanced data processing with error handling"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.data: List[Dict] = []
    
    @validate_input
    def load_data(self) -> bool:
        """Load data from JSON file with error handling"""
        try:
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
            return True
        except FileNotFoundError:
            print(f"File {self.filename} not found")
            return False
        except json.JSONDecodeError as e:
            print(f"Invalid JSON format: {e}")
            return False
    
    @validate_input
    def process_records(self, min_value: float = 0) -> List[Dict]:
        """Process records with list comprehension and filtering"""
        if not self.data:
            raise ValueError("No data loaded")
        
        # Advanced list comprehension with conditional logic
        processed = [
            {
                'id': record.get('id'),
                'value': record.get('value', 0) * 1.1,  # Apply 10% increase
                'category': record.get('category', 'unknown').upper(),
                'processed': True
            }
            for record in self.data
            if isinstance(record.get('value'), (int, float)) and record.get('value', 0) >= min_value
        ]
        
        return processed
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup"""
        if exc_type:
            print(f"Exception occurred: {exc_type.__name__}: {exc_val}")
        self.data.clear()
        return False

# Usage with context manager and advanced features
def main():
    try:
        with DataProcessor("sample_data.json") as processor:
            if processor.load_data():
                results = processor.process_records(min_value=10)
                
                # Generator expression for memory efficiency
                high_value_items = (
                    item for item in results 
                    if item['value'] > 50
                )
                
                print("High value processed items:")
                for item in high_value_items:
                    print(f"  ID: {item['id']}, Value: {item['value']:.2f}")
            
    except Exception as e:
        print(f"Application error: {e}")

if __name__ == "__main__":
    main()