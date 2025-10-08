#!/usr/bin/env python3
"""
Normalize line endings in all text files to LF (Unix style).
This fixes Git issues with CRLF (Windows) line endings.
"""

import os
import glob

def normalize_file(filepath):
    """Convert CRLF to LF in a file."""
    try:
        with open(filepath, 'rb') as file:
            content = file.read()

        # Check if file has CRLF
        if b'\r\n' in content:
            # Convert CRLF to LF
            content = content.replace(b'\r\n', b'\n')

            with open(filepath, 'wb') as file:
                file.write(content)

            return True, "Normalized"
        else:
            return False, "Already LF"
    except Exception as e:
        return False, f"Error: {e}"

def main():
    """Normalize all text files."""
    base_dir = r'h:\My Drive\CS 415 - Algorithm Analysis\Extra Credit App'

    # File patterns to normalize
    patterns = ['*.py', '*.md', '*.txt']

    print("Normalizing Line Endings (CRLF -> LF)")
    print("=" * 60)

    normalized_count = 0
    already_lf_count = 0

    for pattern in patterns:
        files = glob.glob(os.path.join(base_dir, pattern))

        for filepath in files:
            filename = os.path.basename(filepath)
            changed, status = normalize_file(filepath)

            if changed:
                print(f"  [NORMALIZED] {filename}")
                normalized_count += 1
            else:
                print(f"  [OK] {filename} - {status}")
                already_lf_count += 1

    print("=" * 60)
    print(f"Summary:")
    print(f"  Normalized: {normalized_count} files")
    print(f"  Already LF: {already_lf_count} files")
    print(f"  Total: {normalized_count + already_lf_count} files")
    print("\nAll text files now have Unix (LF) line endings.")
    print("This should fix Git markdown rendering issues.")

if __name__ == "__main__":
    main()
