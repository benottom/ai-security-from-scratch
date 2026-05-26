# Report Generator

A tool that produces **evidence reports** for each class in the AI Security from Scratch curriculum. It collects test results, control ledger events, and assurance files from a class directory and generates a comprehensive markdown evidence report.

## What It Does

The report generator:

1. **Collects test results** — Runs `pytest` and captures JUnit XML output
2. **Parses the control ledger** — Reads `assurance/control-ledger.yaml` for control-to-test mappings
3. **Gathers assurance files** — Collects any existing evidence artifacts
4. **Generates a markdown report** — Produces a structured evidence report linking controls → tests → evidence

## Usage

```bash
# Generate report for a specific class
python tools/report_generator/generate_evidence.py labs/phase-2/class-07/

# Generate report without running tests (use existing JUnit XML)
python tools/report_generator/generate_evidence.py labs/phase-2/class-07/ --no-test

# Specify output file
python tools/report_generator/generate_evidence.py labs/phase-2/class-07/ -o evidence-report.md

# Specify JUnit XML input file
python tools/report_generator/generate_evidence.py labs/phase-2/class-07/ --junit results.xml

# Include verbose test output in the report
python tools/report_generator/generate_evidence.py labs/phase-2/class-07/ --verbose
```

## Output

The tool generates a markdown file (default: `assurance/evidence-report.md` in the class directory) containing:

- Executive summary
- Test results organized by control ID
- Control-to-test mapping table
- Pass/fail status for each control
- Overall assurance assessment
- Raw test output appendix

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Report generated successfully, all tests pass |
| 1 | Report generated, but some tests failed |
| 2 | Error (invalid path, missing files, etc.) |

## Dependencies

- Python 3.11+
- PyYAML (for parsing control-ledger.yaml)
- pytest (for running tests, unless `--no-test` is used)
