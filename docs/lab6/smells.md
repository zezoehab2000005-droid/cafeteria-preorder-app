# Task C1 — Code smells in `legacy_invoice.py`

**Team 22 · Cafeteria Pre-Order App · SET 312 Lab 6**

| # | Smell (lecture name) | Where in `legacy_invoice.py` | Refactoring | Done in |
|---|---|---|---|---|
| 1 | Switch statement / type code | `if kind == "regular" … elif kind == "international"` | Replace conditional with polymorphism: one policy class per kind (`RegularPolicy`, `ScholarshipPolicy`, `InternationalPolicy`) in a `POLICIES` table | `invoice.py` |
| 2 | Magic numbers | `1200`, `0.5`, `2000`, `5000` | Named constants: `FEE_PER_HOUR`, `InternationalPolicy.RATE`, `SERVICE_FEE` | `invoice.py` |
| 3 | Duplicated / scattered logic | `kind == "international"` is checked twice (in the loop and after it) | All international rules live in one class, `InternationalPolicy.fee` | `invoice.py` |
| 4 | Feature envy | The loop sums `student.courses` by hand instead of using `student.total_hours` | Use `student.total_hours` | `invoice.py` |
| 5 | Mixed responsibilities (long method) | One function calculates, builds text, writes a file **and** prints | Split: policy calculates, `make_invoice` builds text, a writer saves it; `print` removed | `invoice.py` |
| 6 | Hidden dependency (hard to test) | `open("invoice_…txt", "w")` is hard-coded, so every test writes a real file | Dependency injection: `make_invoice(…, writer=None)` with `FileWriter` as the default and a `FakeWriter` in tests | `invoice.py` |
| 7 | Unsafe resource handling | `f = open(…)` … `f.close()` is skipped if `write` fails | `with open(…) as f:` | `FileWriter.write` |
| 8 | Shotgun surgery / closed to extension | A new student kind means editing the `if` chain in two places | New kind = new class + one line in `POLICIES` (see `SiblingPolicy`, Task C2) | `invoice.py` |
| 9 | Primitive string building | `"Invoice for " + … + str(int(total)) + " EGP"` | f-string | `invoice.py` |

## Task C2 — `SiblingPolicy`

`SiblingPolicy` was added by TDD (red commit, then green commit) **without changing `make_invoice`**, which shows the open/closed principle:

```python
class SiblingPolicy:
    DISCOUNT = 0.25

    def fee(self, hours):
        return hours * FEE_PER_HOUR * (1 - self.DISCOUNT)
```

Test: 6 hours × 1200 = 7200, minus 25 % = **5400 EGP** (`test_sibling_invoice_gets_discount`).
