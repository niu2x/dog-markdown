# AGENTS.md

This document provides guidelines for agentic coding tools working in the dog-markdown repository.

## 1. Build/Lint/Test Commands

### Setup
Install dependencies and prepare the environment:
```bash
uv sync
```

### Build
Package the project:
```bash
uv build
```

### Linting
Run static code analysis with Ruff:
```bash
ruff check .
```
Autofix linting issues:
```bash
ruff check . --fix
```

### Formatting
Format code to follow PEP 8 standards:
```bash
ruff format .
```
Check formatting without modifying files:
```bash
ruff format . --check
```

### Type Checking
Validate type hints with mypy:
```bash
mypy src/
```

### Testing
Run all tests:
```bash
pytest
```
Run a single test file:
```bash
pytest tests/test_markdown_parser.py
```
Run a specific test function:
```bash
pytest tests/test_markdown_parser.py::test_parse_heading
```

## 2. Code Style Guidelines

### Imports
- Use absolute imports for all modules within the project
- Group imports in the following order:
  1. Standard library imports (sorted alphabetically)
  2. Third-party dependencies (sorted alphabetically)
  3. Project-specific imports (sorted alphabetically)
- Separate groups with a blank line
- Avoid wildcard imports (`from module import *`)

### Formatting
- Follow PEP 8 conventions for line length (max 88 chars), indentation (4 spaces, no tabs), and whitespace
- Use Ruff as the authoritative formatter (config in `.ruff.toml`)
- Keep lines concise; split long expressions into multiple lines for readability

### Type Hints
- Add type hints for all function parameters, return values, and module-level variables
- Use `from typing import TYPE_CHECKING` and `if TYPE_CHECKING:` blocks for circular imports
- Prefer standard library types (e.g., `list[str]` over `List[str]` in Python 3.9+)
- Mark modules as typed with `py.typed` files (already present in `src/dog_markdown/`)

### Naming Conventions
- **Variables/functions**: `snake_case` (all lowercase, underscores for separators)
- **Classes**: `PascalCase` (capitalized first letter, no underscores)
- **Constants**: `UPPER_SNAKE_CASE` (all uppercase, underscores for separators)
- **Modules**: Short, lowercase names (avoid underscores unless necessary for readability)

### Error Handling
- Catch specific exceptions instead of bare `except:` clauses
- Raise meaningful exceptions with descriptive error messages
- Use context managers (`with` statements) for resource handling
- Avoid suppressing exceptions without explicit reason

### Documentation
- Write docstrings for all public functions, classes, and modules
- Use Google-style docstrings for consistency:
  ```python
  def parse_markdown(content: str) -> list[Node]:
      """Parse Markdown content into an abstract syntax tree.

      Args:
          content: Raw Markdown string to parse.

      Returns:
          List of AST nodes representing the parsed content.
  
      Raises:
          ParseError: If content contains invalid Markdown syntax.
      """
  ```

### Additional Best Practices
- Avoid print statements in production code; use the `logging` module instead
- Keep functions small and focused on a single responsibility
- Write unit tests for all public API functions
- Use `__future__` imports for forward compatibility (if needed)
- Avoid global variables; use dependency injection where appropriate