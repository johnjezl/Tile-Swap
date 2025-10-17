#!/usr/bin/env python3
"""
Test script to verify web interface setup.

Run this before starting the web server to check that everything is configured correctly.
"""

import sys
import os


def test_flask_import():
    """Test if Flask is installed."""
    try:
        import flask
        print(f"[OK] Flask {flask.__version__} is installed")
        return True
    except ImportError:
        print("[FAIL] Flask is not installed")
        print("  Run: pip install -r requirements.txt")
        return False


def test_core_modules():
    """Test if core game modules can be imported."""
    modules = [
        'graph',
        'graph_builder',
        'tile_manager',
        'score_calculator',
        'web_game_state'
    ]

    success = True
    for module in modules:
        try:
            __import__(module)
            print(f"[OK] Module '{module}' imports successfully")
        except Exception as e:
            print(f"[FAIL] Module '{module}' failed to import: {e}")
            success = False

    return success


def test_file_structure():
    """Test if required files and directories exist."""
    required_items = [
        ('templates', True),
        ('static', True),
        ('templates/index.html', False),
        ('static/game.js', False),
        ('static/style.css', False),
        ('web_app.py', False),
        ('web_game_state.py', False),
    ]

    success = True
    for item, is_dir in required_items:
        if is_dir:
            if os.path.isdir(item):
                print(f"[OK] Directory '{item}' exists")
            else:
                print(f"[FAIL] Directory '{item}' not found")
                success = False
        else:
            if os.path.isfile(item):
                print(f"[OK] File '{item}' exists")
            else:
                print(f"[FAIL] File '{item}' not found")
                success = False

    return success


def main():
    """Run all tests."""
    print("=" * 60)
    print("WEB INTERFACE SETUP TEST")
    print("=" * 60)
    print()

    print("Testing Flask installation...")
    flask_ok = test_flask_import()
    print()

    print("Testing core modules...")
    modules_ok = test_core_modules()
    print()

    print("Testing file structure...")
    files_ok = test_file_structure()
    print()

    print("=" * 60)
    if flask_ok and modules_ok and files_ok:
        print("[SUCCESS] ALL TESTS PASSED")
        print()
        print("You can now start the web server with:")
        print("  python web_app.py")
    else:
        print("[ERROR] SOME TESTS FAILED")
        print()
        if not flask_ok:
            print("Please install Flask: pip install -r requirements.txt")
        if not modules_ok:
            print("Some core modules failed to import. Check for errors above.")
        if not files_ok:
            print("Some required files are missing. Check the file structure.")

    print("=" * 60)

    return flask_ok and modules_ok and files_ok


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
