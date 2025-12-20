# Contributing to Maze Generator & Solver

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/Marcuii/maze-generator-and-solver.git
   cd maze-generator-and-solver
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow the existing code style and conventions
   - Add type hints to all new functions
   - Include docstrings for classes and methods
   - Add error handling where appropriate

3. **Test your changes**:
   ```bash
   python main.py
   ```
   - Test all affected features thoroughly
   - Ensure maze generation works correctly
   - Verify all pathfinding algorithms function properly
   - Check that save/load and export features work

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```
   - Use clear, descriptive commit messages
   - Reference issue numbers if applicable

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**:
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your feature branch
   - Provide a clear description of your changes

## Code Style Guidelines

### Python Style
- Follow PEP 8 style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Type Hints
All functions should include type hints:
```python
def my_function(param1: int, param2: str) -> bool:
    """Function description."""
    return True
```

### Docstrings
Use Google-style docstrings:
```python
def example_function(param1: int, param2: str) -> List[int]:
    """
    Brief description of the function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When invalid input is provided
    """
    pass
```

### Comments
- Add comments for complex logic
- Explain the "why" not the "what"
- Keep comments up-to-date with code changes

## What to Contribute

### Bug Fixes
- Check existing issues first
- Create an issue if one doesn't exist
- Reference the issue in your PR

### New Features
Potential areas for contribution:
- Additional pathfinding algorithms (Greedy Best-First, Bidirectional Search)
- New maze generation algorithms (Recursive Backtracking, Kruskal's)
- Custom start/end point selection
- Maze editing capabilities
- Performance optimizations
- UI improvements
- Additional export formats
- Unit tests

### Documentation
- Fix typos or clarify existing docs
- Add code examples
- Improve installation instructions
- Create tutorials or guides

## Reporting Issues

When reporting bugs, please include:
1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Detailed steps to recreate the bug
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: OS, Python version, etc.
6. **Screenshots**: If applicable

## Code Review Process

1. All contributions require review before merging
2. Address reviewer feedback promptly
3. Keep PRs focused on a single feature/fix
4. Update your branch if main has changed

## Questions?

Feel free to:
- Open an issue for discussion
- Ask questions in your PR
- Reach out to the maintainer

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to make this project better! 🎉
