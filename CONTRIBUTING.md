# Contributing to CelebrateAI

Thank you for your interest in contributing to CelebrateAI!

## Development Guidelines

1. **Code Standards**:
   - Follow PEP 8 guidelines for Python code.
   - Use type hints across all models, routers, and utility functions.
   - Run `pytest` before submitting changes.

2. **Branching Strategy**:
   - `main`: Production-ready branch.
   - `feature/<name>`: Dedicated feature development branches.

3. **Running Tests**:
   ```powershell
   python -m pytest tests -v
   ```

4. **Security & Vulnerabilities**:
   - Ensure all user inputs are sanitized against XSS.
   - Never commit sensitive API keys or credentials.
