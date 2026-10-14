# Reflection — Static Code Analysis

### 1. What did you learn from using static analysis tools?

I learned that static analysis tools can identify code quality, security, and formatting problems before the program is deployed. Pylint checks code quality, Bandit identifies common security risks, and Flake8 checks Python style and formatting.

### 2. Which issues were the most important to fix, and why?

The most important issues were unsafe `eval()`, shell command execution, and MD5 hashing. They can introduce security risks, so I replaced them with an allowlist, removed shell execution, and used SHA-256 hashing. I also replaced the insecure random PIN generator with Python's `secrets` module.

### 3. How did the tools help improve the code?

The tools helped me find problems such as mutable default arguments, broad exception handling, unused variables, missing documentation, and long lines. Fixing these issues made the code easier to read, maintain, and review.

### 4. What challenges did you face, and how did you overcome them?

I faced issues with Python syntax, trailing blank lines, and Flake8 line-length errors. I corrected the code, reran all three tools, and checked the reports until Pylint reached 10.00/10, Bandit reported no issues, and Flake8 produced no output.
