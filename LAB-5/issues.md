# Static Code Analysis — Issues and Fixes

| Issue | Type | Line(s) Before Fix | Description | Fix Approach |
|---|---|---|---|---|
| MD5 hashing | Security — High | Check original report | MD5 is not suitable for security-sensitive hashing. | Replaced MD5 with SHA-256. |
| Shell command execution | Security — High | Check original report | `os.system()` executes a shell command and can introduce command-injection risks. | Removed shell execution and used a normal Python print statement. |
| Unsafe `eval()` | Security — Medium | Check original report | Evaluating an arbitrary expression can execute unintended code. | Replaced `eval()` with an allowlist of approved discount multipliers. |
| Hardcoded secret | Security — Low | Check original report | A hardcoded secret can be exposed in source code. | Read the secret from the `GYM_API_SECRET` environment variable. |
| Insecure random PIN | Security — Low | Check original report | `random.randint()` is not intended for security-sensitive values. | Used `secrets.randbelow()` to generate the PIN. |
| Mutable default argument | Code quality | Check original report | A default list can be shared across function calls. | Used `None` and initialized a new list inside the function. |
| Broad exception handling | Code quality | Check original report | A bare `except` can hide unexpected errors. | Caught `KeyError` specifically when cancelling a membership. |
| Missing file handling improvements | Code quality | Check original report | Opening files without a context manager can leave them unclosed. | Used `with open()` and specified UTF-8 encoding. |
| Long lines | Style | Lines 9–10 in the intermediate version | Lines exceeded Flake8's configured length limit. | Split the member records across multiple lines. |

**Final verification:** Pylint scored 10.00/10, Bandit reported no issues, and Flake8 produced no output.
