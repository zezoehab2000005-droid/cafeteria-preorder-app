# Findings — Static Analysis of `legacy_fees.py`

**Team 22 · Cafeteria Pre-Order App · SET 312 Lab 5**
Tools: Ruff 0.17.6 (config from the handout) · Pylint 4.1.4. Full output is in `before.txt`.

## 1. Summary

| Tool | Result |
|---|---|
| Ruff | **17 problems** in 11 rule codes |
| Pylint | **4.86 / 10** (15 messages) |
| Highest cyclomatic complexity | **9** (`calc`, limit 5) |

> **Note on the count:** the handout lists 16 Ruff problems. Our Ruff version (0.17.6) reports one extra rule, **PLR0917 too-many-positional-arguments**, on the same line as PLR0913. Without it the count is exactly the handout's 16.

## 2. Findings table

| Rule | Count | Smell (lecture name) | Refactoring |
|---|---|---|---|
| F401 | 2 | Dead code (unused imports `os`, `math`) | Delete the imports |
| PLR2004 | 6 | Magic numbers (`2`, `3`, `6000` used as raw values) | Replace with named constants / an enum |
| C901 | 1 | Long method / complex conditional (`calc` complexity 9 > 5) | Replace conditional with a lookup (rate) table; extract the type logic |
| PLR0913 (+ PLR0917) | 1 (+1) | Long parameter list (6 arguments) | Remove unused parameters; group related data into an object (`Course`, `StudentType`) |
| ARG001 | 1 | Dead code (unused parameter `y`, the year) | Remove the parameter |
| B006 | 1 | Mutable default argument (`extra=[]` shared between calls) | Use an immutable default `extras=()` (or `None`) |
| E711 / E712 | 1 / 1 | Unclear conditionals (`disc != None`, `s == True`) | Use `if summer:` and a default discount of `0` (or `is not None`) |
| F841 | 1 | Dead code (unused variable `tmp`) | Delete the variable |
| N802 | 1 | Inconsistent naming (`ProcessAll` is not snake_case) | Rename to `process_all` |

**Pylint adds:** missing module and function docstrings (C0114, C0116) and **E0606 possibly-used-before-assignment** on `fee` in `ProcessAll`, which points straight at the hidden bug below.

## 3. Smells the tools did not report

1. **Mysterious names**: `d`, `t`, `y`, `s`, `disc`, `c`, `e`, `x`, `st` say nothing about what they hold. A comment (`# t: 1=student…`) is needed to explain `t`, which is itself a smell.
2. **Type code instead of a type**: students are identified by the numbers 1, 2 and 3 instead of a named type (enum).
3. **Duplicated code**: `ProcessAll` has two almost identical `calc(...)` calls that differ only in the type number, and the price `350` is repeated in two branches.
4. **Mixed responsibilities**: `report` both calculates and prints, and `ProcessAll` prints instead of returning results, so neither can be tested or reused.
5. **Primitive obsession**: a course is a bare dictionary `{"h": 3}` with a cryptic key instead of a small `Course` object.
6. **Hard-coded year**: `2026` is passed in three places and never used.

## 4. The hidden bug in `ProcessAll`

```
Sara 1050
Omar 1050
```

`ProcessAll` only has branches for type 1 and type 2, so for Omar (type 3, scholarship) **no `if` runs and `fee` is never assigned**. Python then prints the old value of `fee` left over from the previous student, so Omar is wrongly shown Sara's fee of 1050 instead of 0. If Omar is the **first** student in the list, `fee` does not exist yet and the program crashes with `UnboundLocalError: cannot access local variable 'fee'`. We confirmed both cases by running the code.

**Fix (refactoring step 7):** `process_all` calls `tuition_fee` for every student with their own type and returns a `{name: fee}` dictionary, so a scholarship student always gets their own fee (0).
