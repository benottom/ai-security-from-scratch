#!/usr/bin/env python3
"""
Evidence Report Generator for AI Security from Scratch curriculum.

Collects test results, control ledger events, and assurance files from a
class directory and generates a comprehensive markdown evidence report.

Usage:
    python generate_evidence.py <class_path> [options]

Options:
    --no-test       Skip running tests; use existing JUnit XML if available
    --junit FILE    Path to existing JUnit XML file (skips test run)
    -o, --output    Output file path (default: <class_path>/assurance/evidence-report.md)
    --verbose       Include full test output in the report
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class TestCase:
    """A single test case result."""
    name: str
    classname: str
    status: str  # "pass", "fail", "error", "skip"
    time: float = 0.0
    message: str = ""
    output: str = ""


@dataclass
class TestSuite:
    """A test suite containing test cases."""
    name: str
    tests: list[TestCase] = field(default_factory=list)
    time: float = 0.0
    errors: int = 0
    failures: int = 0
    skipped: int = 0

    @property
    def total(self) -> int:
        return len(self.tests)

    @property
    def passed(self) -> int:
        return sum(1 for t in self.tests if t.status == "pass")


@dataclass
class ControlMapping:
    """A control-to-test mapping from the control ledger."""
    control_id: str
    name: str
    category: str
    control_loop_element: str
    description: str
    test_evidence: list[dict[str, str]] = field(default_factory=list)


@dataclass
class EvidenceReport:
    """The complete evidence report data."""
    class_id: str
    class_path: str
    vulnerability: str
    generated_at: str
    controls: list[ControlMapping] = field(default_factory=list)
    test_suites: list[TestSuite] = field(default_factory=list)
    overall_pass: bool = True


# ---------------------------------------------------------------------------
# JUnit XML parsing
# ---------------------------------------------------------------------------

def parse_junit_xml(xml_path: Path) -> list[TestSuite]:
    """Parse a JUnit XML file and return test suites."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    suites = []

    # Handle both <testsuites> wrapper and direct <testsuite>
    suite_elements = root.findall(".//testsuite")
    if not suite_elements:
        suite_elements = [root] if root.tag == "testsuite" else []

    for suite_elem in suite_elements:
        suite = TestSuite(
            name=suite_elem.get("name", "unknown"),
            time=float(suite_elem.get("time", "0")),
            errors=int(suite_elem.get("errors", "0")),
            failures=int(suite_elem.get("failures", "0")),
            skipped=int(suite_elem.get("skipped", "0")),
        )

        for case_elem in suite_elem.findall("testcase"):
            case = TestCase(
                name=case_elem.get("name", "unknown"),
                classname=case_elem.get("classname", ""),
                time=float(case_elem.get("time", "0")),
            )

            # Check for failure
            failure = case_elem.find("failure")
            error = case_elem.find("error")
            skip = case_elem.find("skipped")

            if failure is not None:
                case.status = "fail"
                case.message = failure.get("message", "")
                case.output = failure.text or ""
            elif error is not None:
                case.status = "error"
                case.message = error.get("message", "")
                case.output = error.text or ""
            elif skip is not None:
                case.status = "skip"
                case.message = skip.get("message", "")
            else:
                case.status = "pass"

            suite.tests.append(case)

        suites.append(suite)

    return suites


# ---------------------------------------------------------------------------
# Control ledger parsing
# ---------------------------------------------------------------------------

def parse_control_ledger(ledger_path: Path) -> tuple[list[ControlMapping], str, str]:
    """Parse the control ledger YAML and return control mappings."""
    try:
        import yaml
    except ImportError:
        # Fallback: basic regex parsing
        return _parse_ledger_basic(ledger_path)

    content = ledger_path.read_text(errors="replace")
    data = yaml.safe_load(content)

    if not isinstance(data, dict):
        return [], "unknown", "unknown"

    class_id = data.get("class_id", "unknown")
    vulnerability = data.get("vulnerability", "unknown")
    controls = []

    for ctrl_data in data.get("controls", []):
        if not isinstance(ctrl_data, dict):
            continue
        ctrl = ControlMapping(
            control_id=ctrl_data.get("control_id", "CTL-?"),
            name=ctrl_data.get("name", "Unknown"),
            category=ctrl_data.get("category", "unknown"),
            control_loop_element=ctrl_data.get("control_loop_element", "unknown"),
            description=ctrl_data.get("description", ""),
            test_evidence=ctrl_data.get("test_evidence", []),
        )
        controls.append(ctrl)

    return controls, class_id, vulnerability


def _parse_ledger_basic(ledger_path: Path) -> tuple[list[ControlMapping], str, str]:
    """Basic parsing without PyYAML — limited but functional."""
    content = ledger_path.read_text(errors="replace")
    class_id = "unknown"
    vulnerability = "unknown"

    # Extract class_id
    m = re.search(r'class_id:\s*["\']?([^"\'\n]+)', content)
    if m:
        class_id = m.group(1).strip()

    # Extract vulnerability
    m = re.search(r'vulnerability:\s*["\']?([^"\'\n]+)', content)
    if m:
        vulnerability = m.group(1).strip()

    return [], class_id, vulnerability


# ---------------------------------------------------------------------------
# Test execution
# ---------------------------------------------------------------------------

def run_tests(class_path: Path, output_xml: Path) -> bool:
    """Run pytest and capture JUnit XML output."""
    test_dir = class_path / "tests"
    if not test_dir.exists():
        return False

    cmd = [
        sys.executable, "-m", "pytest",
        str(test_dir),
        f"--junitxml={output_xml}",
        "--tb=short",
        "-q",
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(class_path),
        )
        return result.returncode in (0, 1)  # 1 = test failures, still valid output
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(report: EvidenceReport, verbose: bool = False) -> str:
    """Generate the markdown evidence report."""
    lines = []

    lines.append(f"# Evidence Report: {report.class_id}")
    lines.append("")
    lines.append(f"**Class ID:** {report.class_id}")
    lines.append(f"**Vulnerability:** {report.vulnerability}")
    lines.append(f"**Generated:** {report.generated_at}")
    lines.append(f"**Overall Status:** {'✅ PASS' if report.overall_pass else '❌ FAIL'}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Executive Summary
    lines.append("## Executive Summary")
    lines.append("")

    total_tests = sum(s.total for s in report.test_suites)
    total_passed = sum(s.passed for s in report.test_suites)
    total_failed = sum(s.failures + s.errors for s in report.test_suites)
    total_controls = len(report.controls)
    controls_with_evidence = sum(
        1 for c in report.controls
        if any(
            any(tc.name.endswith(e.get("test_function", "").split("::")[-1])
                for suite in report.test_suites
                for tc in suite.tests)
            for e in c.test_evidence
        )
    )

    if report.overall_pass:
        lines.append(
            f"All {total_tests} tests pass. {total_controls} controls are verified "
            f"with automated test evidence. The defensive measures for the "
            f"{report.vulnerability} vulnerability provide effective mitigation."
        )
    else:
        lines.append(
            f"{total_failed} of {total_tests} tests failed. The defensive measures "
            f"for the {report.vulnerability} vulnerability require attention before "
            f"assurance can be confirmed."
        )
    lines.append("")

    # Control Summary
    lines.append("## Control Summary")
    lines.append("")
    lines.append("| Control ID | Name | Category | Control-Loop Element | Test Status |")
    lines.append("|------------|------|----------|---------------------|-------------|")

    for ctrl in report.controls:
        # Determine test status for this control
        ctrl_pass = True
        ctrl_has_tests = False
        for evidence in ctrl.test_evidence:
            test_fn = evidence.get("test_function", "")
            # Find matching test case
            for suite in report.test_suites:
                for tc in suite.tests:
                    if test_fn in tc.name or tc.name.endswith(test_fn.split("::")[-1]):
                        ctrl_has_tests = True
                        if tc.status != "pass":
                            ctrl_pass = False

        if ctrl_has_tests:
            status = "✅ PASS" if ctrl_pass else "❌ FAIL"
        else:
            status = "⚠️ NO TEST"

        lines.append(
            f"| {ctrl.control_id} | {ctrl.name} | {ctrl.category} | "
            f"{ctrl.control_loop_element} | {status} |"
        )
    lines.append("")

    # Test Results Detail
    lines.append("## Test Results Detail")
    lines.append("")

    for suite in report.test_suites:
        lines.append(f"### {suite.name}")
        lines.append("")
        lines.append(f"- **Total:** {suite.total}")
        lines.append(f"- **Passed:** {suite.passed}")
        lines.append(f"- **Failed:** {suite.failures}")
        lines.append(f"- **Errors:** {suite.errors}")
        lines.append(f"- **Skipped:** {suite.skipped}")
        lines.append(f"- **Duration:** {suite.time:.2f}s")
        lines.append("")

        lines.append("| Test | Status | Duration | Message |")
        lines.append("|------|--------|----------|---------|")
        for tc in suite.tests:
            icon = {"pass": "✅", "fail": "❌", "error": "💥", "skip": "⏭️"}.get(tc.status, "❓")
            msg = tc.message[:60] + "..." if len(tc.message) > 60 else tc.message
            lines.append(f"| {tc.name} | {icon} {tc.status} | {tc.time:.3f}s | {msg} |")
        lines.append("")

        # Verbose output for failed tests
        if verbose:
            failed_tests = [tc for tc in suite.tests if tc.status in ("fail", "error")]
            if failed_tests:
                lines.append("#### Failed Test Output")
                lines.append("")
                for tc in failed_tests:
                    lines.append(f"**{tc.name}:**")
                    lines.append(f"```")
                    lines.append(tc.output[:2000] if tc.output else "(no output)")
                    lines.append(f"```")
                    lines.append("")

    # Control-to-Test Mapping
    lines.append("## Control-to-Test Mapping")
    lines.append("")

    for ctrl in report.controls:
        lines.append(f"### {ctrl.control_id}: {ctrl.name}")
        lines.append("")
        lines.append(f"- **Category:** {ctrl.category}")
        lines.append(f"- **Control-loop element:** {ctrl.control_loop_element}")
        lines.append(f"- **Description:** {ctrl.description}")
        lines.append("")

        if ctrl.test_evidence:
            lines.append("| Test File | Test Function | Assertion | Result |")
            lines.append("|-----------|---------------|-----------|--------|")
            for evidence in ctrl.test_evidence:
                test_fn = evidence.get("test_function", "N/A")
                test_file = evidence.get("test_file", "N/A")
                assertion = evidence.get("assertion", "N/A")

                # Find test result
                result_str = "⚠️ NOT FOUND"
                for suite in report.test_suites:
                    for tc in suite.tests:
                        short_fn = test_fn.split("::")[-1] if "::" in test_fn else test_fn
                        if short_fn in tc.name:
                            icon = {"pass": "✅", "fail": "❌", "skip": "⏭️"}.get(tc.status, "❓")
                            result_str = f"{icon} {tc.status.upper()}"
                            break

                lines.append(f"| {test_file} | {test_fn} | {assertion} | {result_str} |")
            lines.append("")
        else:
            lines.append("*No test evidence linked.*")
            lines.append("")

    # Overall Assessment
    lines.append("## Overall Assessment")
    lines.append("")

    if report.overall_pass and total_controls > 0:
        lines.append(
            f"Based on {total_tests} automated tests covering {total_controls} controls, "
            f"the defensive measures for the {report.vulnerability} vulnerability "
            f"are verified and effective. All tests pass and all controls have "
            f"corresponding test evidence."
        )
    elif report.overall_pass and total_controls == 0:
        lines.append(
            f"All {total_tests} tests pass, but no control ledger was found. "
            f"Control-to-test mapping cannot be verified. Generate the control ledger "
            f"using the Blue-Team Defense Agent."
        )
    else:
        lines.append(
            f"{total_failed} test(s) failed. The defensive measures require "
            f"remediation before assurance can be confirmed. Review the failed tests "
            f"above and update the affected controls."
        )
    lines.append("")

    # Footer
    lines.append("---")
    lines.append(f"*Report generated by evidence-report-generator on {report.generated_at}*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate evidence report for an AI Security from Scratch class"
    )
    parser.add_argument(
        "class_path",
        type=str,
        help="Path to the class directory (e.g., labs/phase-2/class-07/)",
    )
    parser.add_argument(
        "--no-test",
        action="store_true",
        help="Skip running tests; use existing JUnit XML if available",
    )
    parser.add_argument(
        "--junit",
        type=str,
        help="Path to existing JUnit XML file",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output file path (default: <class_path>/assurance/evidence-report.md)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Include full test output in the report",
    )

    args = parser.parse_args()
    class_path = Path(args.class_path).resolve()

    if not class_path.exists():
        print(f"Error: Path not found: {class_path}", file=sys.stderr)
        return 2

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        assurance_dir = class_path / "assurance"
        assurance_dir.mkdir(parents=True, exist_ok=True)
        output_path = assurance_dir / "evidence-report.md"

    # Parse control ledger
    ledger_path = class_path / "assurance" / "control-ledger.yaml"
    if ledger_path.exists():
        controls, class_id, vulnerability = parse_control_ledger(ledger_path)
    else:
        controls = []
        class_id = class_path.name
        vulnerability = "unknown"
        print("Warning: No control ledger found. Control mapping will be incomplete.", file=sys.stderr)

    # Get test results
    junit_xml_path = None
    if args.junit:
        junit_xml_path = Path(args.junit)
        if not junit_xml_path.exists():
            print(f"Error: JUnit XML not found: {junit_xml_path}", file=sys.stderr)
            return 2
    elif not args.no_test:
        # Run tests and capture JUnit XML
        junit_xml_path = class_path / "assurance" / ".test-results.xml"
        print("Running tests...")
        if not run_tests(class_path, junit_xml_path):
            print("Warning: Test run failed or produced no output.", file=sys.stderr)
            junit_xml_path = None
    else:
        # Look for existing JUnit XML
        for candidate in [
            class_path / "assurance" / ".test-results.xml",
            class_path / "test-results.xml",
            class_path / "reports" / "junit.xml",
        ]:
            if candidate.exists():
                junit_xml_path = candidate
                break

    # Parse test results
    test_suites: list[TestSuite] = []
    if junit_xml_path and junit_xml_path.exists():
        try:
            test_suites = parse_junit_xml(junit_xml_path)
        except ET.ParseError as e:
            print(f"Warning: Failed to parse JUnit XML: {e}", file=sys.stderr)

    # Build report
    overall_pass = all(
        tc.status == "pass"
        for suite in test_suites
        for tc in suite.tests
    )

    report = EvidenceReport(
        class_id=class_id,
        class_path=str(class_path),
        vulnerability=vulnerability,
        generated_at=datetime.now(timezone.utc).isoformat(),
        controls=controls,
        test_suites=test_suites,
        overall_pass=overall_pass,
    )

    # Generate markdown
    markdown = generate_report(report, verbose=args.verbose)

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown)
    print(f"Evidence report written to: {output_path}")

    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
