"""
TwinFlow AI Backend Test Runner
Executes backend unit and integration test suite using pytest.
"""
import sys
import subprocess
from pathlib import Path

def main():
    backend_dir = Path(__file__).resolve().parent
    print("=" * 60)
    print(" 🧪 Running TwinFlow AI Backend Test Suite")
    print(f" Directory: {backend_dir}")
    print("=" * 60)

    try:
        import pytest
        import httpx
    except ImportError as e:
        print(f"\n⚠️ Missing test dependency: {e.name}")
        print("Please install test requirements by running:")
        print("  pip install pytest httpx")
        print("\nAttempting automatic installation...\n")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pytest>=8.0.0", "httpx>=0.27.0"], check=True)
            import pytest
        except Exception as install_err:
            print(f"Failed to auto-install: {install_err}")
            sys.exit(1)

    # Run pytest with verbose and summary flags
    args = [
        str(backend_dir / "tests"),
        "-v",
        "--tb=short",
        "-ra"
    ]
    sys.exit(pytest.main(args))

if __name__ == "__main__":
    main()
