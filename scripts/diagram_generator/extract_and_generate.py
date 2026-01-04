#!/usr/bin/env python3
"""Extract Mermaid diagrams from markdown files and generate PNG images."""

import re
import subprocess
import sys
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
ASSETS_DIR = DOCS_DIR / "assets" / "diagrams"
MERMAID_CONFIG = Path(__file__).parent / "mermaid-config.json"

# Regex to match mermaid code blocks
MERMAID_PATTERN = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)
# Regex to find headings
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


def get_nearest_heading(content: str, mermaid_start_pos: int) -> str:
    """Find the nearest markdown heading above the mermaid block."""
    # Get content before the mermaid block
    content_before = content[:mermaid_start_pos]

    # Find all headings in the content before
    headings = list(HEADING_PATTERN.finditer(content_before))

    if headings:
        # Return the last (nearest) heading text
        return headings[-1].group(2).strip()

    return "Diagram"


def get_category_from_path(md_path: Path) -> str:
    """Determine diagram category from markdown file path."""
    relative = md_path.relative_to(DOCS_DIR)
    parts = relative.parts

    # Map common directory patterns to categories
    category_mappings = {
        "architecture": "architecture",
        "agents": "agents",
        "decisions": "decisions",
        "evaluation": "evaluation",
        "repositories": "repositories",
        "tools": "tools",
        "workflows": "workflows",
        "prompts": "prompts",
        "modules": "modules",
        "api": "api",
        "dependencies": "dependencies",
        "usecases": "usecases",
        "ingestor": "ingestor",
        "guides": "guides",
        "infrastructure": "infrastructure",
        "ui": "ui",
        "cli": "cli",
        "configs": "configs",
    }

    # Look for category in path parts
    for part in parts:
        if part in category_mappings:
            return category_mappings[part]

    # Default to first directory or 'misc'
    if len(parts) > 1:
        return parts[0]
    return "misc"


def generate_filename(md_path: Path, index: int) -> str:
    """Generate unique filename for diagram based on markdown path and index."""
    # Get the stem (filename without extension)
    stem = md_path.stem

    # If there are parent directories, include them for uniqueness
    relative = md_path.relative_to(DOCS_DIR)
    parent_parts = relative.parts[:-1]

    # Create filename with parent context if needed
    if parent_parts:
        # Use last parent directory for context
        parent = parent_parts[-1]
        if parent != stem:
            base = f"{parent}_{stem}"
        else:
            base = stem
    else:
        base = stem

    return f"{base}_{index}"


def calculate_relative_path(md_path: Path, png_path: Path) -> str:
    """Calculate relative path from markdown file to PNG."""
    md_dir = md_path.parent
    try:
        relative = png_path.relative_to(md_dir)
        return str(relative)
    except ValueError:
        # Not a subpath, need to go up directories
        # Find common ancestor
        md_parts = md_dir.parts
        png_parts = png_path.parts

        # Find common prefix length
        common_len = 0
        for i, (m, p) in enumerate(zip(md_parts, png_parts)):
            if m != p:
                break
            common_len = i + 1

        # Calculate ups needed
        ups_needed = len(md_parts) - common_len

        # Build relative path
        rel_parts = [".."] * ups_needed + list(png_parts[common_len:])
        return "/".join(rel_parts)


def generate_png(mmd_path: Path) -> bool:
    """Generate PNG from .mmd file."""
    png_path = mmd_path.with_suffix(".png")

    cmd = [
        "npx",
        "mmdc",
        "-i",
        str(mmd_path),
        "-o",
        str(png_path),
        "-c",
        str(MERMAID_CONFIG),
        "-b",
        "white",
        "-s",
        "2",  # Scale factor for higher resolution
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"  Generated: {png_path.name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Error generating {mmd_path.name}: {e.stderr}")
        return False


def process_markdown_file(md_path: Path, dry_run: bool = False) -> tuple[int, int]:
    """Process a markdown file, extracting mermaid diagrams and replacing with image refs.

    Returns (diagrams_found, diagrams_processed) tuple.
    """
    content = md_path.read_text()

    # Find all mermaid blocks
    matches = list(MERMAID_PATTERN.finditer(content))

    if not matches:
        return 0, 0

    print(f"\nProcessing: {md_path.relative_to(PROJECT_ROOT)}")
    print(f"  Found {len(matches)} mermaid diagram(s)")

    category = get_category_from_path(md_path)
    category_dir = ASSETS_DIR / category

    if not dry_run:
        category_dir.mkdir(parents=True, exist_ok=True)

    # Process in reverse order to maintain positions
    new_content = content
    processed = 0

    for i, match in enumerate(reversed(matches), 1):
        index = len(matches) - i + 1
        mermaid_content = match.group(1).strip()
        heading = get_nearest_heading(content, match.start())

        filename = generate_filename(md_path, index)
        mmd_path = category_dir / f"{filename}.mmd"
        png_path = category_dir / f"{filename}.png"

        print(f"  [{index}] '{heading}' -> {category}/{filename}.png")

        if not dry_run:
            # Save .mmd file
            mmd_path.write_text(mermaid_content + "\n")

            # Generate PNG
            if generate_png(mmd_path):
                # Calculate relative path from md file to png
                rel_path = calculate_relative_path(md_path, png_path)

                # Replace mermaid block with image reference
                image_ref = f"![{heading}]({rel_path})"
                new_content = (
                    new_content[: match.start()] + image_ref + new_content[match.end() :]
                )
                processed += 1
            else:
                print(f"  Skipping replacement for {filename} due to generation error")
        else:
            processed += 1

    if not dry_run and processed > 0:
        md_path.write_text(new_content)
        print(f"  Updated markdown file")

    return len(matches), processed


def main() -> int:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract Mermaid diagrams from markdown and generate PNGs"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="Process only a specific markdown file",
    )
    args = parser.parse_args()

    if args.dry_run:
        print("DRY RUN - No files will be modified\n")

    # Check for mermaid-cli
    if not args.dry_run:
        try:
            subprocess.run(
                ["npx", "mmdc", "--version"],
                check=True,
                capture_output=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: mermaid-cli not found. Run 'npm install' first.")
            return 1

    # Find markdown files
    if args.file:
        if not args.file.exists():
            print(f"Error: File not found: {args.file}")
            return 1
        md_files = [args.file]
    else:
        md_files = list(DOCS_DIR.rglob("*.md"))

    print(f"Scanning {len(md_files)} markdown file(s)...")

    total_found = 0
    total_processed = 0
    files_with_diagrams = 0

    for md_file in sorted(md_files):
        found, processed = process_markdown_file(md_file, args.dry_run)
        if found > 0:
            files_with_diagrams += 1
            total_found += found
            total_processed += processed

    print(f"\n{'=' * 50}")
    print(f"Summary:")
    print(f"  Files with diagrams: {files_with_diagrams}")
    print(f"  Total diagrams found: {total_found}")
    print(f"  Diagrams processed: {total_processed}")

    if args.dry_run:
        print("\nRun without --dry-run to apply changes")

    return 0 if total_processed == total_found else 1


if __name__ == "__main__":
    sys.exit(main())
