# Lab Validator

A validation tool that checks whether a lab directory follows the required structure and quality standards for the **AI Security from Scratch** curriculum.

## What It Does

The lab validator performs a comprehensive check on a single lab directory to ensure:

1. **Required files are present** — `README.md`, `vulnerable/app.py`, `vulnerable/requirements.txt`, `patched/app.py`, `patched/requirements.txt`
2. **Vulnerable app runs** — The vulnerable application starts and responds to health checks
3. **Patched app runs** — The patched application starts and responds to health checks
4. **Tests exist** — Both `test_vulnerable.py` and `test_patched.py` are present
5. **Safety markers** — Attack files contain required `<!-- SAFETY: ... -->` markers
6. **Inline annotations** — Vulnerable code has `# VULNERABLE:` comments; patched code has `# PATCH:` comments
7. **Dependencies are pinned** — `requirements.txt` files use `==` version pins
8. **Control ledger exists** — `assurance/control-ledger.yaml` is present and valid YAML

## Usage

```bash
# Validate a specific lab
python tools/lab_validator/validate_lab.py labs/phase-2/class-07/

# Validate with verbose output
python tools/lab_validator/validate_lab.py labs/phase-2/class-07/ --verbose

# Validate without starting apps (structural checks only)
python tools/lab_validator/validate_lab.py labs/phase-2/class-07/ --no-run

# Validate and output results as JSON
python tools/lab_validator/validate_lab.py labs/phase-2/class-07/ --format json

# Validate all labs
python tools/lab_validator/validate_lab.py labs/ --recursive
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks passed |
| 1 | One or more checks failed |
| 2 | Invalid arguments or lab path not found |

## Output

The validator produces a human-readable report by default:

```
═══════════════════════════════════════════════════════════
  Lab Validation Report: phase-2/class-07
═══════════════════════════════════════════════════════════

  ✅ PASS  Required files present (8/8)
  ✅ PASS  Vulnerable app starts and responds to /health
  ✅ PASS  Patched app starts and responds to /health
  ✅ PASS  Test files present (2/2)
  ✅ PASS  Safety markers in attack files (3/3)
  ✅ PASS  Inline annotations in vulnerable/app.py (2 found)
  ✅ PASS  Inline annotations in patched/app.py (2 found)
  ✅ PASS  Dependencies pinned in vulnerable/requirements.txt
  ✅ PASS  Dependencies pinned in patched/requirements.txt
  ✅ PASS  Control ledger present and valid YAML

═══════════════════════════════════════════════════════════
  Result: ALL CHECKS PASSED ✅
═══════════════════════════════════════════════════════════
```

With `--format json`, the output is a JSON object suitable for CI integration:

```json
{
  "lab_path": "labs/phase-2/class-07",
  "timestamp": "2024-01-15T10:30:00Z",
  "overall_result": "pass",
  "checks": [
    {
      "name": "required_files",
      "status": "pass",
      "details": "8/8 files present"
    },
    ...
  ]
}
```

## Integration with CI

This tool is designed to run in GitHub Actions. See `.github/workflows/validate-lessons.yml` for the CI configuration.

## Extending

To add a new validation check:

1. Create a new function in `validate_lab.py` with the signature `check_*(lab_path: Path) -> CheckResult`
2. Register it in the `ALL_CHECKS` list
3. The check will automatically be included in validation runs
