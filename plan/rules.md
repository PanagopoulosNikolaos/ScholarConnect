# General:
- Language: English
- Tone: Direct and `Non-Directive`

---

# Coding
> The following is to apply to all languages (Python, C, C++, Bash, etc.)
- Classes: Use **PascalCase**
- Functions: Use **camelCase**
- Variables: Use **snake_case** for all variables and class members
- Comments: Each Class/Function must have a multi-line comment (docstring) that adheres to the **Google Python Docstring Style**:

    1. Starts with a concise one-line summary of the function's purpose.
    2. Leaves a blank line after the summary if detailed descriptions or arguments follow.
    3. Uses explicit sections for "Args:", "Returns:", and "Raises:" (or "Throws:").
    4. Includes type hints in parentheses for all parameters and return values.

    #### Example:

    ```python
    """
    Calculates the Euclidean distance between two points.

    Args:
        p1 (Point): The starting coordinate.
        p2 (Point): The destination coordinate.

    Returns:
        float: The straight-line distance between p1 and p2.
    """
    ```

    5. Single-line comments must be descriptive, focusing on `why`, `how`, or `what` logic is being applied, rather than being instructional or conversational.

---