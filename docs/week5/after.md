# Before / After Comparison & Pairing Reflection

**Team 22 · Cafeteria Pre-Order App · SET 312 Lab 5**
Full "after" output is in `after-output.txt`.

## 1. Before / after table

| Measure | Before (`legacy_fees.py`) | After (`fees.py`) |
|---|---|---|
| Ruff issues (total) | 17 (16 in the handout's Ruff version) | **0**: All checks passed! |
| Highest cyclomatic complexity | 9 (`calc`) | **3** (`tuition_fee`) |
| Arguments of the main function | 6 | **5** (`courses, kind, summer, discount, extras`); only 2 are required |
| Pylint score (/10) | 4.86 | **10.00** |
| Tests passing | 0 (no tests) | **16** (6 in `test_fees.py`, 10 in `test_grades.py`) |

> `legacy_fees.py` is kept unchanged so the characterization tests can compare old and new behaviour. It is excluded from `ruff check .` in `pyproject.toml`; its problems are recorded in `before.txt`.

## 2. What changed (one commit per step)

| # | Step | Removes | Example |
|---|---|---|---|
| 1 | Deleted unused imports, `tmp` and the unused year `y` | F401, F841, ARG001 | `calc(d, t, y, s, disc, extra)` → no `y` |
| 2 | Renamed everything | N802, mysterious names | `calc` → `tuition_fee`, `d` → `courses`, `ProcessAll` → `process_all` |
| 3 | Named constants + `StudentType` enum | PLR2004, type-code comment | `350` → `PRICE_PER_CREDIT_HOUR`, `t == 2` → `StudentType.STAFF_CHILD` |
| 4 | Rate table instead of `if/elif`; `if summer:`; discount defaults to 0 | C901, E711, E712 | `PRICE_SHARE[kind]` |
| 5 | `extras=()` and a frozen `Course` data class | B006, primitive obsession | `{"h": 3}` → `Course(3)` |
| 6 | `fee_report` returns text instead of printing | Mixed responsibilities | `print(...)` → `return "\n".join(lines)` |
| 7 | `process_all` gives every student a fee | The hidden bug | `{"Sara": 1050, "Omar": 0}` |

**Before**
```python
def calc(d, t, y, s, disc, extra=[]):
    # t: 1=student, 2=staff child, 3=scholarship
    total = 0
    for c in d:
        if t == 1:
            total = total + c["h"] * 350
        elif t == 2:
            total = total + c["h"] * 350 * 0.5
        elif t == 3:
            total = total + 0
    ...
```

**After**
```python
def tuition_fee(courses, kind, summer=False, discount=0, extras=()):
    """Return the total tuition fee for one student."""
    total = (
        sum(course.hours for course in courses)
        * PRICE_PER_CREDIT_HOUR
        * PRICE_SHARE[kind]
    )
    if total > LARGE_FEE_THRESHOLD:
        total -= LARGE_FEE_REDUCTION
    if summer:
        total += SUMMER_SUPPLEMENT
    return total - discount + sum(extras)
```

## 3. Pairing reflection

<!-- Write this yourselves (3–4 sentences): it must describe how YOUR pair actually worked.
     Prompts: Who drove and who navigated in each round? Did the 12-minute switch work?
     What did the navigator catch that the driver missed (e.g. a boundary test, a name)?
     What was hard (staying quiet as navigator, thinking aloud as driver)?
     Would you pair again for your project, and on what kind of task? -->

**Pair:** ____________ (driver/navigator) and ____________

_Reflection:_

**One line each (kata, Checkpoint B):**
- ____________: 
- ____________: 
