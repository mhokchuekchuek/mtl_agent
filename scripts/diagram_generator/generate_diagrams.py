#!/usr/bin/env python3
"""Generate PNG images from Mermaid diagram files."""

import subprocess
import sys
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
DIAGRAMS_DIR = PROJECT_ROOT / "docs" / "assets" / "diagrams"
IMAGES_DIR = PROJECT_ROOT / "docs" / "assets" / "diagrams"  # Same location as source
MERMAID_CONFIG = Path(__file__).parent / "mermaid-config.json"


def generate_diagram(mmd_file: Path) -> Path | None:
    """Generate PNG from .mmd file."""
    # Output PNG alongside the source .mmd file
    output_path = mmd_file.with_suffix(".png")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "npx",
        "mmdc",
        "-i",
        str(mmd_file),
        "-o",
        str(output_path),
        "-c",
        str(MERMAID_CONFIG),
        "-b",
        "white",
        "-s",
        "2",  # Scale factor for higher resolution
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Generated: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error generating {mmd_file}: {e.stderr}")
        return None


def main() -> int:
    """Generate all diagrams."""
    if not DIAGRAMS_DIR.exists():
        print(f"Diagrams directory not found: {DIAGRAMS_DIR}")
        return 1

    mmd_files = list(DIAGRAMS_DIR.rglob("*.mmd"))

    if not mmd_files:
        print("No .mmd files found")
        return 0

    print(f"Found {len(mmd_files)} diagram file(s)")

    success_count = 0
    for mmd_file in mmd_files:
        if generate_diagram(mmd_file):
            success_count += 1

    print(f"\nGenerated {success_count}/{len(mmd_files)} diagrams")
    return 0 if success_count == len(mmd_files) else 1


if __name__ == "__main__":
    sys.exit(main())
