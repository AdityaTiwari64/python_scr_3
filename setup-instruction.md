# Python Competence Analyzer - Setup Instructions

## What This Project Does

This project analyzes Python code written by student and provides educational feedback. It can detect syntax errors, assess skill levels, and generate helpful questions for learning.

## Requirements

- Python 3.7 or higher
- No external packages required (uses only standard library)

## Quick Setup

1. Download or clone this project to your computer
2. Open a terminal/command prompt in the project folder
3. Run the tests to make sure everything works:

```
python run_test.py
```

You should see "All tests passed!" at the end.

## How to Run

### Basic Demo

Run the main analyzer to see it in action:

```
python src/competence_analyse.py
```

This will analyze 3 sample code submissions and show the results.

### Run Tests

To run all tests:

```
python test/test_analyzer.py
```

### Analyze Your Own Code

Create a file called `my_code.py` with your Python code, then run:

```
python -c "import sys; sys.path.append('src'); from competence_analyse import StudentCodeAnalyzer; analyzer = StudentCodeAnalyzer(); code = open('my_code.py').read(); metrics, feedback = analyzer.assess_code(code); print('Scores:'); print(f'Syntax: {metrics.syntax_score:.2f}'); print(f'Overall: {metrics.total_score:.2f}'); print('Feedback:'); [print(f'  {i+1}. {f}') for i, f in enumerate(feedback)]"
```

### Jupyter Notebook (Optional)

If you want to use the interactive notebook:

1. Install Jupyter:
```
pip install jupyter matplotlib pandas
```

2. Start the notebook:
```
jupyter notebook notebooks/analysis_demo.ipynb
```

## Understanding the Results

- **Syntax Score**: 0.00 = syntax error, 1.00 = no syntax errors
- **Structure Score**: Based on code complexity (functions, classes, loops)
- **Concept Score**: Skill level (0.25=beginner, 0.50=intermediate, 0.75=advanced, 1.00=expert)
- **Overall Score**: Combined assessment

## Sample Code Files

The `data/sample_codes/` folder contains example Python files:
- `beginner_syntax_error.py` - Has a syntax error (missing colon)
- `beginner_basic_function.py` - Simple function example
- `intermediate_class_loops.py` - Class with loops
- `advanced_decorators_exceptions.py` - Advanced Python features

## Troubleshooting

If you get import errors, make sure you're running commands from the project root folder (where you see the `src` and `test` folders).

If tests fail, check that you're using Python 3.7 or higher:

```
python --version
```

## Project Structure

```
sse_intern/
├── src/
│   └── competence_analyse.py    # Main analyzer code
├── test/
│   └── test_analyzer.py         # Unit tests
├── data/
│   └── sample_codes/            # Example Python files
├── notebooks/
│   └── analysis_demo.ipynb      # Jupyter notebook
├── run_test.py                  # Test runner
└── requirements.txt             # Dependencies (optional)
└── research.md                  # Reseach Plan (optional)
```

That's it. The project should work out of the box with just Python installed.
