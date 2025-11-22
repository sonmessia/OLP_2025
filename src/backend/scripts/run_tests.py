#!/usr/bin/env python3
"""
Test runner script for OLP 2025 backend tests.
Provides comprehensive test execution with coverage reporting.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode, result.stdout, result.stderr


def main():
    """Main test runner function."""
    # Get the backend directory
    backend_dir = Path(__file__).parent

    # Ensure we're in the backend directory for tests
    os.chdir(backend_dir)

    print("=" * 60)
    print("OLP 2025 Backend Test Suite")
    print("=" * 60)

    # Install dependencies if needed
    print("\n1. Checking/Installing test dependencies...")
    returncode, _, _ = run_command(
        [sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"]
    )
    if returncode != 0:
        print("Failed to install dependencies")
        return 1

    # Run linting first
    print("\n2. Running linting checks...")
    returncode, _, _ = run_command([sys.executable, "-m", "ruff", "check", "."])
    if returncode != 0:
        print("Linting checks failed")
        return 1

    # Run type checking
    print("\n3. Running type checking...")
    returncode, _, _ = run_command([sys.executable, "-m", "mypy", "app"])
    if returncode != 0:
        print("Type checking failed")
        return 1

    # Run tests with coverage
    print("\n4. Running tests with coverage...")
    test_cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--cov=app",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-report=xml",
        "--cov-fail-under=80",
    ]

    returncode, stdout, stderr = run_command(test_cmd)
    if returncode != 0:
        print("Tests failed or coverage below threshold")
        return 1

    # Generate test report
    print("\n5. Test Summary:")
    lines = stdout.split("\n") if stdout else []
    for line in lines:
        if "passed" in line and "failed" in line:
            print(f"  {line}")
        if "%" in line and "coverage" in line.lower():
            print(f"  {line}")

    # Run integration tests specifically
    print("\n6. Running integration tests...")
    integration_cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/test_*_integration.py",
        "-v",
        "--tb=short",
    ]

    returncode, _, _ = run_command(integration_cmd)
    if returncode != 0:
        print("Integration tests failed")
        return 1

    print("\n" + "=" * 60)
    print("All tests passed successfully!")
    print(f"Coverage report generated: {backend_dir}/htmlcov/index.html")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
