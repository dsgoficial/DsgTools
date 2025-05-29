#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to update translation.pro file for QGIS plugins.
This script scans your plugin directory for Python and UI files
and updates the SOURCES and FORMS sections of translation.pro.
"""

import os
import re
import argparse


def collect_files(base_dir, extensions):
    """
    Scan directory recursively for files with specific extensions

    Args:
        base_dir (str): Base directory to start scanning
        extensions (list): List of file extensions to collect (e.g., ['.py', '.ui'])

    Returns:
        list: Sorted list of collected file paths relative to base_dir
    """
    collected_files = []

    for root, dirs, files in os.walk(base_dir):
        # Skip __pycache__ directories and .git directories
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")
        if ".git" in dirs:
            dirs.remove(".git")

        for file in files:
            # Check if file has one of the target extensions
            if any(file.endswith(ext) for ext in extensions):
                # Get path relative to base_dir
                rel_path = os.path.relpath(os.path.join(root, file), base_dir)
                # Normalize path separators to Unix style
                rel_path = rel_path.replace("\\", "/")
                collected_files.append(rel_path)

    return sorted(collected_files)


def update_translation_pro(pro_file, py_files, ui_files):
    """
    Update translation.pro file with new Python and UI files

    Args:
        pro_file (str): Path to translation.pro file
        py_files (list): List of Python files to include in SOURCES
        ui_files (list): List of UI files to include in FORMS

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read existing content
        with open(pro_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract the TRANSLATIONS line
        translations_match = re.search(r"TRANSLATIONS\s*=\s*([^\n]+)", content)
        translations_line = (
            translations_match.group(0)
            if translations_match
            else "TRANSLATIONS = i18n/DsgTools_pt.ts"
        )

        # Extract any other content after TRANSLATIONS (e.g., RESOURCES)
        resources_match = re.search(r"(RESOURCES\s*[^\n]+).*$", content, re.DOTALL)
        resources_line = (
            resources_match.group(1)
            if resources_match
            else "RESOURCES += resources.qrc"
        )

        # Format Python files list for SOURCES
        sources = " SOURCES\t\t =\t"
        for i, py_file in enumerate(py_files):
            if i > 0:
                sources += " " * 21
            sources += py_file + " \\\n"
        # Remove the final backslash and newline
        sources = sources[:-2]

        # Format UI files list for FORMS
        forms = " FORMS\t\t =\t"
        for i, ui_file in enumerate(ui_files):
            if i > 0:
                forms += " " * 21
            forms += ui_file + " \\\n"
        # Remove the final backslash and newline
        forms = forms[:-2]

        # Build the new content
        new_content = (
            f"{sources}\n\n{forms}\n\n {translations_line}\n\n{resources_line}\n"
        )

        # Write the updated content
        with open(pro_file, "w", encoding="utf-8") as f:
            f.write(new_content)

        return True

    except Exception as e:
        print(f"Error updating translation.pro: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Update translation.pro file for QGIS plugin"
    )
    parser.add_argument(
        "--dir", default=".", help="Plugin directory (default: current directory)"
    )
    parser.add_argument(
        "--output",
        default="translation.pro",
        help="Output pro file path (default: translation.pro)",
    )

    args = parser.parse_args()

    base_dir = args.dir
    pro_file = args.output

    print(f"Scanning plugin directory: {base_dir}")

    # Collect Python files
    py_files = collect_files(base_dir, [".py"])
    print(f"Found {len(py_files)} Python files")

    # Collect UI files
    ui_files = collect_files(base_dir, [".ui"])
    print(f"Found {len(ui_files)} UI files")

    # Update translation.pro
    if update_translation_pro(pro_file, py_files, ui_files):
        print(f"Successfully updated {pro_file}")
    else:
        print(f"Failed to update {pro_file}")


if __name__ == "__main__":
    main()
