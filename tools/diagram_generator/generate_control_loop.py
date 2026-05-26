#!/usr/bin/env python3
"""
Control Loop Diagram Generator for AI Security from Scratch curriculum.

Reads a control-loop-analysis file (markdown or YAML) and generates a Mermaid
diagram string visualizing the control loop with all elements.

Usage:
    python generate_control_loop.py <input_file> [options]

Options:
    -o, --output FILE   Output file path (default: stdout)
    --raw               Output raw Mermaid string (no markdown wrapper)
    --format FMT        Input format: auto (default), md, yaml
    --direction DIR     Diagram direction: LR (default), RL, TB, BT
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class ControlLoopElements:
    """The seven elements of a control-loop model."""
    sensor: str = ""
    estimator: str = ""
    controller: str = ""
    actuator: str = ""
    plant: str = ""
    disturbance: str = ""
    reference: str = ""


# ---------------------------------------------------------------------------
# Parsing: Markdown
# ---------------------------------------------------------------------------

def parse_markdown(md_path: Path) -> ControlLoopElements:
    """Extract control-loop elements from a markdown file."""
    content = md_path.read_text(errors="replace")
    elements = ControlLoopElements()

    # Look for "The Control Loop" section or "control_loop_mapping" section
    # Pattern 1: Bullet list with element: description
    element_patterns = {
        "sensor": r"(?i)(?:sensor|observe|monitor)[:\s]+(.+?)(?:\n|$)",
        "estimator": r"(?i)(?:estimator|infer|analyze)[:\s]+(.+?)(?:\n|$)",
        "controller": r"(?i)(?:controller|decide|policy)[:\s]+(.+?)(?:\n|$)",
        "actuator": r"(?i)(?:actuator|enforce|execute)[:\s]+(.+?)(?:\n|$)",
        "plant": r"(?i)(?:plant|system|protect)[:\s]+(.+?)(?:\n|$)",
        "disturbance": r"(?i)(?:disturbance|threat|attack)[:\s]+(.+?)(?:\n|$)",
        "reference": r"(?i)(?:reference|desired|target)[:\s]+(.+?)(?:\n|$)",
    }

    for element_name, pattern in element_patterns.items():
        match = re.search(pattern, content)
        if match:
            value = match.group(1).strip()
            # Clean up markdown formatting
            value = re.sub(r"[*_`#]", "", value).strip()
            setattr(elements, element_name, value)

    # Pattern 2: YAML-like mapping in markdown (e.g., from class-spec)
    yaml_block = re.search(r"```yaml\s*\n(.*?)```", content, re.DOTALL)
    if yaml_block:
        yaml_content = yaml_block.group(1)
        for element_name in ["sensor", "estimator", "controller", "actuator", "plant", "disturbance", "reference"]:
            match = re.search(rf"{element_name}:\s*[\"']?(.+?)[\"']?\s*$", yaml_content, re.MULTILINE)
            if match and not getattr(elements, element_name):
                setattr(elements, element_name, match.group(1).strip().strip("\"'"))

    # Pattern 3: Table format
    table_match = re.search(r"\|.+\|.+\|[\s\S]*?(?=\n\n|\Z)", content)
    if table_match:
        table_content = table_match.group(0)
        for element_name in ["sensor", "estimator", "controller", "actuator", "plant", "disturbance", "reference"]:
            if not getattr(elements, element_name):
                match = re.search(rf"\|.*{element_name}.*\|(.+?)\|", table_content, re.IGNORECASE)
                if match:
                    setattr(elements, element_name, match.group(1).strip().strip("`"))

    return elements


# ---------------------------------------------------------------------------
# Parsing: YAML
# ---------------------------------------------------------------------------

def parse_yaml(yaml_path: Path) -> ControlLoopElements:
    """Extract control-loop elements from a YAML file."""
    content = yaml_path.read_text(errors="replace")

    # Try to use PyYAML for proper parsing
    try:
        import yaml
        data = yaml.safe_load(content)
        if isinstance(data, dict):
            mapping = data.get("control_loop_mapping", data)
            return ControlLoopElements(
                sensor=str(mapping.get("sensor", "")),
                estimator=str(mapping.get("estimator", "")),
                controller=str(mapping.get("controller", "")),
                actuator=str(mapping.get("actuator", "")),
                plant=str(mapping.get("plant", "")),
                disturbance=str(mapping.get("disturbance", "")),
                reference=str(mapping.get("reference", "")),
            )
    except ImportError:
        pass

    # Fallback: regex parsing
    elements = ControlLoopElements()
    for element_name in ["sensor", "estimator", "controller", "actuator", "plant", "disturbance", "reference"]:
        match = re.search(rf"{element_name}:\s*[\"']?(.+?)[\"']?\s*$", content, re.MULTILINE)
        if match:
            setattr(elements, element_name, match.group(1).strip().strip("\"'"))

    return elements


# ---------------------------------------------------------------------------
# Diagram generation
# ---------------------------------------------------------------------------

# Icons for each element
ELEMENT_ICONS = {
    "sensor": "📡",
    "estimator": "🧠",
    "controller": "⚙️",
    "actuator": "🔒",
    "plant": "🖥️",
    "disturbance": "💥",
    "reference": "🎯",
}

ELEMENT_COLORS = {
    "sensor": "#4A90D9",
    "estimator": "#7B68EE",
    "controller": "#2ECC71",
    "actuator": "#E67E22",
    "plant": "#3498DB",
    "disturbance": "#E74C3C",
    "reference": "#F39C12",
}


def truncate_label(text: str, max_len: int = 40) -> str:
    """Truncate a label to fit in a diagram node."""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


def escape_mermaid(text: str) -> str:
    """Escape special characters for Mermaid syntax."""
    # Replace characters that break Mermaid parsing
    text = text.replace('"', "'")
    text = text.replace("[", "(")
    text = text.replace("]", ")")
    text = text.replace("{", "(")
    text = text.replace("}", ")")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace("#", "")
    text = text.replace("&", "and")
    return text


def generate_mermaid(elements: ControlLoopElements, direction: str = "LR") -> str:
    """Generate a Mermaid flowchart string from control-loop elements."""
    lines = []
    lines.append(f"flowchart {direction}")
    lines.append("")

    # Node definitions
    node_defs = []

    # Plant node
    plant_label = truncate_label(escape_mermaid(elements.plant)) if elements.plant else "System Under Protection"
    node_defs.append(f"    PLANT[\"{ELEMENT_ICONS['plant']} Plant: {plant_label}\"]")

    # Sensor node
    sensor_label = truncate_label(escape_mermaid(elements.sensor)) if elements.sensor else "Observation"
    node_defs.append(f"    SENSOR[\"{ELEMENT_ICONS['sensor']} Sensor: {sensor_label}\"]")

    # Estimator node
    estimator_label = truncate_label(escape_mermaid(elements.estimator)) if elements.estimator else "State Estimation"
    node_defs.append(f"    ESTIMATOR[\"{ELEMENT_ICONS['estimator']} Estimator: {estimator_label}\"]")

    # Controller node
    controller_label = truncate_label(escape_mermaid(elements.controller)) if elements.controller else "Control Policy"
    node_defs.append(f"    CONTROLLER[\"{ELEMENT_ICONS['controller']} Controller: {controller_label}\"]")

    # Actuator node
    actuator_label = truncate_label(escape_mermaid(elements.actuator)) if elements.actuator else "Enforcement"
    node_defs.append(f"    ACTUATOR[\"{ELEMENT_ICONS['actuator']} Actuator: {actuator_label}\"]")

    # Disturbance node (external threat)
    disturbance_label = truncate_label(escape_mermaid(elements.disturbance)) if elements.disturbance else "Adversarial Input"
    node_defs.append(f"    DISTURBANCE[\"{ELEMENT_ICONS['disturbance']} Disturbance: {disturbance_label}\"]")

    # Reference node (desired state)
    reference_label = truncate_label(escape_mermaid(elements.reference)) if elements.reference else "Secure State"
    node_defs.append(f"    REFERENCE[\"{ELEMENT_ICONS['reference']} Reference: {reference_label}\"]")

    lines.extend(node_defs)
    lines.append("")

    # Connections - main feedback loop
    lines.append("    %% Main feedback loop")
    lines.append("    PLANT -->|observes| SENSOR")
    lines.append("    SENSOR -->|raw data| ESTIMATOR")
    lines.append("    ESTIMATOR -->|state estimate| CONTROLLER")
    lines.append("    CONTROLLER -->|control signal| ACTUATOR")
    lines.append("    ACTUATOR -->|enforces| PLANT")
    lines.append("")

    # External inputs - disturbances and reference
    lines.append("    %% External inputs")
    lines.append("    DISTURBANCE -.->|exploits| PLANT")
    lines.append("    REFERENCE -.->|desired state| ESTIMATOR")
    lines.append("")

    # Styling
    lines.append("    %% Styling")
    lines.append(f"    style PLANT fill:{ELEMENT_COLORS['plant']},color:#fff,stroke:#2C3E50")
    lines.append(f"    style SENSOR fill:{ELEMENT_COLORS['sensor']},color:#fff,stroke:#2C3E50")
    lines.append(f"    style ESTIMATOR fill:{ELEMENT_COLORS['estimator']},color:#fff,stroke:#2C3E50")
    lines.append(f"    style CONTROLLER fill:{ELEMENT_COLORS['controller']},color:#fff,stroke:#2C3E50")
    lines.append(f"    style ACTUATOR fill:{ELEMENT_COLORS['actuator']},color:#fff,stroke:#2C3E50")
    lines.append(f"    style DISTURBANCE fill:{ELEMENT_COLORS['disturbance']},color:#fff,stroke:#C0392B")
    lines.append(f"    style REFERENCE fill:{ELEMENT_COLORS['reference']},color:#fff,stroke:#D68910")

    return "\n".join(lines)


def generate_markdown_wrapper(elements: ControlLoopElements, direction: str = "LR") -> str:
    """Generate a full markdown file with embedded Mermaid diagram."""
    mermaid_str = generate_mermaid(elements, direction)

    lines = []
    lines.append("# Control Loop Diagram")
    lines.append("")
    lines.append("## Control-Loop Model")
    lines.append("")
    lines.append("```mermaid")
    lines.append(mermaid_str)
    lines.append("```")
    lines.append("")
    lines.append("## Element Descriptions")
    lines.append("")

    descriptions = {
        "Plant": (elements.plant, "The system under protection"),
        "Sensor": (elements.sensor, "Observes the plant's state"),
        "Estimator": (elements.estimator, "Infers the plant's state from sensor readings"),
        "Controller": (elements.controller, "Decides what action to take based on the estimated state"),
        "Actuator": (elements.actuator, "Enforces the controller's decision on the plant"),
        "Disturbance": (elements.disturbance, "The adversarial input that disrupts the control loop"),
        "Reference": (elements.reference, "The desired secure state the system should maintain"),
    }

    lines.append("| Element | Description |")
    lines.append("|---------|-------------|")
    for name, (value, fallback) in descriptions.items():
        display = value if value else fallback
        lines.append(f"| {name} | {display} |")
    lines.append("")

    lines.append("## Vulnerability as Control-Loop Failure")
    lines.append("")
    lines.append(
        "The vulnerability represents a **disturbance** that exploits a gap in "
        "the control loop. When a sensor fails to observe, an estimator misjudges, "
        "a controller makes a wrong decision, or an actuator fails to enforce, "
        "the disturbance penetrates the system."
    )
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Mermaid control-loop diagram from analysis file"
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to input file (markdown or YAML)",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Output raw Mermaid string (no markdown wrapper)",
    )
    parser.add_argument(
        "--format",
        choices=["auto", "md", "yaml"],
        default="auto",
        help="Input format (default: auto-detect)",
    )
    parser.add_argument(
        "--direction",
        choices=["LR", "RL", "TB", "BT"],
        default="LR",
        help="Diagram direction (default: LR)",
    )

    args = parser.parse_args()
    input_path = Path(args.input_file)

    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        return 2

    # Determine format
    fmt = args.format
    if fmt == "auto":
        if input_path.suffix in (".yaml", ".yml"):
            fmt = "yaml"
        else:
            fmt = "md"

    # Parse input
    if fmt == "yaml":
        elements = parse_yaml(input_path)
    else:
        elements = parse_markdown(input_path)

    # Check that we got at least the core elements
    core_elements = [elements.sensor, elements.estimator, elements.controller,
                     elements.actuator, elements.plant]
    found = sum(1 for e in core_elements if e)

    if found < 2:
        print(
            "Warning: Could not extract enough control-loop elements from the input. "
            f"Found {found}/5 core elements. Diagram may be incomplete.",
            file=sys.stderr,
        )

    # Generate output
    if args.raw:
        output = generate_mermaid(elements, direction=args.direction)
    else:
        output = generate_markdown_wrapper(elements, direction=args.direction)

    # Write output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output)
        print(f"Diagram written to: {output_path}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
