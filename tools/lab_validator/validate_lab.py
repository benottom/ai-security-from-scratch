#!/usr/bin/env python3
"""
Lab Validator for AI Security from Scratch curriculum.

Validates that a lab directory follows the required structure, contains
all necessary files, apps run correctly, tests exist, and safety markers
are in place.

Usage:
    python validate_lab.py <lab_path> [options]

Options:
    --verbose       Show detailed output for each check
    --no-run        Skip app startup checks (structural checks only)
    --format FMT    Output format: text (default) or json
    --recursive     Validate all lab directories under the given path
    --timeout SECS  Timeout for app startup checks (default: 30)
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import urlopen, Request
from urllib.error import URLError


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class CheckResult:
    """Result of a single validation check."""
    name: str
    status: str  # "pass", "fail", "skip", "warn"
    details: str = ""
    items: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "details": self.details,
            "items": self.items,
        }


@dataclass
class ValidationResult:
    """Aggregated result for an entire lab."""
    lab_path: str
    timestamp: str
    overall_result: str  # "pass", "fail"
    checks: list[CheckResult] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "lab_path": self.lab_path,
            "timestamp": self.timestamp,
            "overall_result": self.overall_result,
            "checks": [c.to_dict() for c in self.checks],
        }


# ---------------------------------------------------------------------------
# Required file definitions
# ---------------------------------------------------------------------------

REQUIRED_FILES = [
    "README.md",
    "vulnerable/app.py",
    "vulnerable/requirements.txt",
    "patched/app.py",
    "patched/requirements.txt",
    "attacks/attack.py",
    "tests/test_vulnerable.py",
    "tests/test_patched.py",
]

RECOMMENDED_FILES = [
    "attacks/README.md",
    "tests/conftest.py",
    "assurance/control-ledger.yaml",
    "defense.py",
]


# ---------------------------------------------------------------------------
# Check functions
# ---------------------------------------------------------------------------

def check_required_files(lab_path: Path) -> CheckResult:
    """Verify all required files are present."""
    missing = []
    found = []
    for req_file in REQUIRED_FILES:
        full_path = lab_path / req_file
        if full_path.exists():
            found.append(req_file)
        else:
            missing.append(req_file)

    if missing:
        return CheckResult(
            name="required_files",
            status="fail",
            details=f"Missing {len(missing)} required file(s): {', '.join(missing)}",
            items=missing,
        )
    return CheckResult(
        name="required_files",
        status="pass",
        details=f"All {len(REQUIRED_FILES)} required files present",
        items=found,
    )


def check_recommended_files(lab_path: Path) -> CheckResult:
    """Verify recommended files are present (warn, not fail)."""
    missing = []
    for rec_file in RECOMMENDED_FILES:
        if not (lab_path / rec_file).exists():
            missing.append(rec_file)

    if missing:
        return CheckResult(
            name="recommended_files",
            status="warn",
            details=f"Missing {len(missing)} recommended file(s): {', '.join(missing)}",
            items=missing,
        )
    return CheckResult(
        name="recommended_files",
        status="pass",
        details="All recommended files present",
    )


def check_safety_markers(lab_path: Path) -> CheckResult:
    """Verify attack files contain SAFETY markers."""
    attack_files = list(lab_path.glob("attacks/*.py")) + list(lab_path.glob("attacks/*.md"))
    if not attack_files:
        return CheckResult(
            name="safety_markers",
            status="fail",
            details="No attack files found in attacks/ directory",
        )

    results = []
    missing_markers = []
    safety_pattern = re.compile(r"<!--\s*SAFETY:.*?-->", re.IGNORECASE)
    # Also check for Python safety comments
    python_safety_pattern = re.compile(r"#\s*SAFETY:.*", re.IGNORECASE)

    for attack_file in attack_files:
        content = attack_file.read_text(errors="replace")
        has_html_safety = bool(safety_pattern.search(content))
        has_py_safety = bool(python_safety_pattern.search(content))
        if has_html_safety or has_py_safety:
            count = len(safety_pattern.findall(content)) + len(python_safety_pattern.findall(content))
            results.append(f"{attack_file.relative_to(lab_path)} ({count} markers)")
        else:
            missing_markers.append(str(attack_file.relative_to(lab_path)))

    if missing_markers:
        return CheckResult(
            name="safety_markers",
            status="fail",
            details=f"Missing safety markers in: {', '.join(missing_markers)}",
            items=missing_markers,
        )
    return CheckResult(
        name="safety_markers",
        status="pass",
        details=f"Safety markers found in all {len(attack_files)} attack file(s)",
        items=results,
    )


def check_inline_annotations(lab_path: Path) -> CheckResult:
    """Verify vulnerable code has # VULNERABLE: and patched code has # PATCH: markers."""
    results = []
    failures = []

    # Check vulnerable/app.py for # VULNERABLE: annotations
    vuln_app = lab_path / "vulnerable" / "app.py"
    if vuln_app.exists():
        content = vuln_app.read_text(errors="replace")
        vuln_markers = re.findall(r"#\s*VULNERABLE:\s*.+", content)
        if vuln_markers:
            results.append(f"vulnerable/app.py ({len(vuln_markers)} VULNERABLE markers)")
        else:
            failures.append("vulnerable/app.py missing # VULNERABLE: annotations")
    else:
        failures.append("vulnerable/app.py not found")

    # Check patched/app.py for # PATCH: annotations
    patched_app = lab_path / "patched" / "app.py"
    if patched_app.exists():
        content = patched_app.read_text(errors="replace")
        patch_markers = re.findall(r"#\s*PATCH:\s*.+", content)
        if patch_markers:
            results.append(f"patched/app.py ({len(patch_markers)} PATCH markers)")
        else:
            failures.append("patched/app.py missing # PATCH: annotations")
    else:
        failures.append("patched/app.py not found")

    if failures:
        return CheckResult(
            name="inline_annotations",
            status="fail",
            details="; ".join(failures),
            items=failures,
        )
    return CheckResult(
        name="inline_annotations",
        status="pass",
        details="Inline annotations found in both app versions",
        items=results,
    )


def check_dependencies_pinned(lab_path: Path) -> CheckResult:
    """Verify requirements.txt files use == version pins."""
    results = []
    failures = []

    for req_file_rel in ["vulnerable/requirements.txt", "patched/requirements.txt"]:
        req_file = lab_path / req_file_rel
        if not req_file.exists():
            failures.append(f"{req_file_rel} not found")
            continue

        content = req_file.read_text(errors="replace")
        unpinned = []
        for line_num, line in enumerate(content.splitlines(), 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Check for == pin
            if "==" not in line:
                unpinned.append(f"  Line {line_num}: {line}")

        if unpinned:
            failures.append(f"{req_file_rel} has unpinned dependencies:\n" + "\n".join(unpinned))
        else:
            results.append(f"{req_file_rel} all dependencies pinned")

    if failures:
        return CheckResult(
            name="dependencies_pinned",
            status="fail",
            details="Unpinned dependencies found",
            items=failures,
        )
    return CheckResult(
        name="dependencies_pinned",
        status="pass",
        details="All dependencies use == version pins",
        items=results,
    )


def check_control_ledger(lab_path: Path) -> CheckResult:
    """Verify assurance/control-ledger.yaml exists and is valid YAML."""
    ledger_path = lab_path / "assurance" / "control-ledger.yaml"
    if not ledger_path.exists():
        return CheckResult(
            name="control_ledger",
            status="fail",
            details="assurance/control-ledger.yaml not found",
        )

    try:
        import yaml  # noqa: F811
        content = ledger_path.read_text(errors="replace")
        data = yaml.safe_load(content)
    except ImportError:
        # If PyYAML not available, do basic syntax check
        content = ledger_path.read_text(errors="replace")
        if content.strip():
            return CheckResult(
                name="control_ledger",
                status="warn",
                details="control-ledger.yaml exists but PyYAML not installed for validation",
            )
        return CheckResult(
            name="control_ledger",
            status="fail",
            details="control-ledger.yaml is empty",
        )
    except Exception as e:
        return CheckResult(
            name="control_ledger",
            status="fail",
            details=f"Invalid YAML in control-ledger.yaml: {e}",
        )

    # Check required fields
    if not isinstance(data, dict):
        return CheckResult(
            name="control_ledger",
            status="fail",
            details="control-ledger.yaml does not contain a YAML mapping",
        )

    required_fields = ["class_id", "vulnerability", "controls"]
    missing_fields = [f for f in required_fields if f not in data]
    if missing_fields:
        return CheckResult(
            name="control_ledger",
            status="fail",
            details=f"Missing required fields: {', '.join(missing_fields)}",
            items=missing_fields,
        )

    # Check controls have required sub-fields
    controls = data.get("controls", [])
    control_issues = []
    for i, ctrl in enumerate(controls):
        if not isinstance(ctrl, dict):
            control_issues.append(f"Control {i} is not a mapping")
            continue
        for req_field in ["control_id", "name", "category", "control_loop_element"]:
            if req_field not in ctrl:
                control_issues.append(f"Control {i} missing field: {req_field}")

    if control_issues:
        return CheckResult(
            name="control_ledger",
            status="warn",
            details=f"Control ledger valid YAML but has issues: {'; '.join(control_issues)}",
            items=control_issues,
        )

    return CheckResult(
        name="control_ledger",
        status="pass",
        details=f"Control ledger valid with {len(controls)} control(s)",
    )


def check_app_runs(lab_path: Path, subdir: str, timeout: int = 30) -> CheckResult:
    """Verify that an app starts and responds to /health endpoint."""
    app_path = lab_path / subdir / "app.py"
    if not app_path.exists():
        return CheckResult(
            name=f"{subdir}_app_runs",
            status="fail",
            details=f"{subdir}/app.py not found",
        )

    port = 5000 if subdir == "vulnerable" else 5001
    env_overrides = {"PORT": str(port), "PYTHONUNBUFFERED": "1"}

    try:
        import os
        env = {**os.environ, **env_overrides}
        proc = subprocess.Popen(
            [sys.executable, str(app_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            cwd=str(lab_path / subdir),
        )

        # Wait for /health to respond
        start_time = time.time()
        healthy = False
        while time.time() - start_time < timeout:
            try:
                req = Request(f"http://localhost:{port}/health")
                resp = urlopen(req, timeout=2)
                if resp.status == 200:
                    healthy = True
                    break
            except (URLError, OSError):
                pass
            time.sleep(0.5)

        if healthy:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)
            return CheckResult(
                name=f"{subdir}_app_runs",
                status="pass",
                details=f"{subdir}/app.py starts and responds to /health on port {port}",
            )
        else:
            proc.terminate()
            _, stderr = proc.communicate(timeout=5)
            stderr_text = stderr.decode(errors="replace")[:500] if stderr else ""
            return CheckResult(
                name=f"{subdir}_app_runs",
                status="fail",
                details=f"{subdir}/app.py did not respond to /health within {timeout}s. Stderr: {stderr_text}",
            )

    except Exception as e:
        return CheckResult(
            name=f"{subdir}_app_runs",
            status="fail",
            details=f"Failed to start {subdir}/app.py: {e}",
        )


def check_test_files(lab_path: Path) -> CheckResult:
    """Verify test files exist and have test functions."""
    test_files = {
        "tests/test_vulnerable.py": "TestVulnerability",
        "tests/test_patched.py": "TestPatch",
    }

    results = []
    missing = []

    for test_file_rel, expected_class in test_files.items():
        test_file = lab_path / test_file_rel
        if not test_file.exists():
            missing.append(test_file_rel)
            continue

        content = test_file.read_text(errors="replace")
        test_functions = re.findall(r"def\s+(test_\w+)", content)
        if test_functions:
            results.append(f"{test_file_rel} ({len(test_functions)} test(s))")
        else:
            missing.append(f"{test_file_rel} (no test functions found)")

    if missing:
        return CheckResult(
            name="test_files",
            status="fail",
            details=f"Test file issues: {', '.join(missing)}",
            items=missing,
        )
    return CheckResult(
        name="test_files",
        status="pass",
        details="All test files present with test functions",
        items=results,
    )


def check_readme_sections(lab_path: Path) -> CheckResult:
    """Verify lab README.md has all required sections."""
    readme_path = lab_path / "README.md"
    if not readme_path.exists():
        return CheckResult(
            name="readme_sections",
            status="fail",
            details="README.md not found",
        )

    content = readme_path.read_text(errors="replace")
    required_sections = [
        "Objective",
        "Setup",
        "Tasks",
        "Cleanup",
        "Safety Notice",
    ]

    found = []
    missing = []
    for section in required_sections:
        if re.search(rf"##\s+.*{section}", content, re.IGNORECASE):
            found.append(section)
        else:
            missing.append(section)

    if missing:
        return CheckResult(
            name="readme_sections",
            status="fail",
            details=f"README.md missing sections: {', '.join(missing)}",
            items=missing,
        )
    return CheckResult(
        name="readme_sections",
        status="pass",
        details=f"README.md has all {len(required_sections)} required sections",
        items=found,
    )


# ---------------------------------------------------------------------------
# All checks in execution order
# ---------------------------------------------------------------------------

STRUCTURAL_CHECKS = [
    check_required_files,
    check_recommended_files,
    check_safety_markers,
    check_inline_annotations,
    check_dependencies_pinned,
    check_control_ledger,
    check_test_files,
    check_readme_sections,
]

RUNTIME_CHECKS = [
    lambda lab_path: check_app_runs(lab_path, "vulnerable"),
    lambda lab_path: check_app_runs(lab_path, "patched"),
]

ALL_CHECKS = STRUCTURAL_CHECKS + RUNTIME_CHECKS


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def format_text_report(result: ValidationResult) -> str:
    """Format validation result as human-readable text."""
    lines = []
    lines.append("═" * 60)
    lines.append(f"  Lab Validation Report: {Path(result.lab_path).name}")
    lines.append("═" * 60)
    lines.append("")

    for check in result.checks:
        icon = {
            "pass": "✅ PASS",
            "fail": "❌ FAIL",
            "warn": "⚠️  WARN",
            "skip": "⏭️  SKIP",
        }.get(check.status, "❓ UNK")

        lines.append(f"  {icon}  {check.name}")
        if check.details:
            lines.append(f"        {check.details}")
        for item in check.items[:5]:  # Show up to 5 items
            lines.append(f"        - {item}")
        if len(check.items) > 5:
            lines.append(f"        ... and {len(check.items) - 5} more")

    lines.append("")
    lines.append("═" * 60)

    if result.overall_result == "pass":
        lines.append("  Result: ALL CHECKS PASSED ✅")
    else:
        lines.append("  Result: SOME CHECKS FAILED ❌")

    lines.append("═" * 60)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def validate_lab(lab_path: Path, no_run: bool = False, timeout: int = 30) -> ValidationResult:
    """Run all validation checks on a lab directory."""
    result = ValidationResult(
        lab_path=str(lab_path),
        timestamp=datetime.now(timezone.utc).isoformat(),
        overall_result="pass",
    )

    # Structural checks
    for check_fn in STRUCTURAL_CHECKS:
        check_result = check_fn(lab_path)
        result.checks.append(check_result)

    # Runtime checks
    if no_run:
        for check_fn in RUNTIME_CHECKS:
            result.checks.append(CheckResult(
                name=check_fn.__name__ if hasattr(check_fn, '__name__') else "runtime_check",
                status="skip",
                details="Skipped (--no-run flag)",
            ))
    else:
        for check_fn in RUNTIME_CHECKS:
            check_result = check_fn(lab_path)
            # Inject timeout for app check functions
            if "app_runs" in check_result.name:
                pass  # Already handled with default timeout
            result.checks.append(check_result)

    # Determine overall result
    for check in result.checks:
        if check.status == "fail":
            result.overall_result = "fail"
            break

    return result


def find_lab_dirs(base_path: Path) -> list[Path]:
    """Find all lab directories under a base path."""
    lab_dirs = []
    for candidate in sorted(base_path.rglob("*")):
        if candidate.is_dir() and (candidate / "README.md").exists() and (
            (candidate / "vulnerable").exists() or (candidate / "patched").exists()
        ):
            lab_dirs.append(candidate)
    return lab_dirs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate AI Security from Scratch lab directories"
    )
    parser.add_argument(
        "lab_path",
        type=str,
        help="Path to a lab directory or base directory (with --recursive)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output for each check",
    )
    parser.add_argument(
        "--no-run",
        action="store_true",
        help="Skip app startup checks (structural checks only)",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Validate all lab directories under the given path",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout in seconds for app startup checks (default: 30)",
    )

    args = parser.parse_args()
    lab_path = Path(args.lab_path)

    if not lab_path.exists():
        print(f"Error: Path not found: {lab_path}", file=sys.stderr)
        return 2

    if args.recursive:
        lab_dirs = find_lab_dirs(lab_path)
        if not lab_dirs:
            print(f"No lab directories found under: {lab_path}", file=sys.stderr)
            return 2
    else:
        lab_dirs = [lab_path]

    all_results = []
    overall_pass = True

    for lab_dir in lab_dirs:
        result = validate_lab(lab_dir, no_run=args.no_run, timeout=args.timeout)
        all_results.append(result)
        if result.overall_result != "pass":
            overall_pass = False

    # Output results
    if args.format == "json":
        if len(all_results) == 1:
            print(json.dumps(all_results[0].to_dict(), indent=2))
        else:
            print(json.dumps({
                "results": [r.to_dict() for r in all_results],
                "overall": "pass" if overall_pass else "fail",
            }, indent=2))
    else:
        for result in all_results:
            print(format_text_report(result))
            print()

    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
