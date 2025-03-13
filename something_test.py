import os
import subprocess
import sys
import pytest

sys.stdout.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# Define directories to scan
GITHUB_DIR = os.path.realpath(os.path.expanduser("~/NET-Tools"))
TEST_DIR = os.path.join(GITHUB_DIR, "test")
RUNNER_DIR = os.path.realpath("/home/runner/work/NET-Tools/NET-Tools")  # Ensure absolute path

# Scripts to exclude
EXCLUDED_SCRIPTS = {"sheetstopastebin.py", "infocollect.py", "something_test.py", "thebasics.py", "imgurtodiscord.py"}

def test_find_python_scripts(*directories):
    """Recursively finds all Python scripts in the given directories."""
    python_files = []

    for directory in directories:
        abs_directory = os.path.realpath(directory)  # Ensure absolute path
        print(f"🔍 Searching in: {abs_directory}")

        if not os.path.isdir(abs_directory):
            print(f"❌ ERROR: Directory does not exist: {abs_directory}")
            continue

        for root, _, files in os.walk(abs_directory):
            print(f"📂 Inside: {root}")  # Debugging output
            for file in files:
                if file.endswith(".py"):
                    script_path = os.path.join(root, file)
                    print(f"  ➜ Found: {script_path}")  # Debugging output
                    if file not in EXCLUDED_SCRIPTS:
                        python_files.append(script_path)
                    else:
                        print(f"  🚫 Excluded: {script_path}")

    print(f"📂 Total Python scripts found: {len(python_files)}")
    return python_files

def test_check_script_execution(script_path):
    """Attempts to execute a Python script and reports success or failure."""
    print(f"🚀 Running: {script_path}")
    if not os.path.exists(script_path):
        print(f"❌ ERROR: Script does not exist: {script_path}")
        return

    try:
        result = subprocess.run(
            ["python", script_path], capture_output=True, text=True, timeout=30, encoding="utf-8"
        )
        print(f"📜 Output from {script_path}: {result.stdout}")  # Log output for debugging
        if result.returncode == 0:
            print(f"✅ SUCCESS: {script_path}")
        else:
            print(f"❌ ERROR in {script_path}\nOutput:\n{result.stderr}")
    except Exception as e:
        print(f"⚠️ EXCEPTION during execution of {script_path} - {e}")

@pytest.fixture
def directory():
    """Fixture for the current working directory."""
    return os.getcwd()

@pytest.fixture
def script_path(directory):
    """Fixture for the script path to `something_test.py`."""
    return os.path.join(directory, "something_test.py")

def main():
    # Only scan directories that exist
    valid_dirs = [GITHUB_DIR, TEST_DIR, RUNNER_DIR]
    valid_dirs = [d for d in valid_dirs if os.path.isdir(d)]  # Remove any non-existing directories

    if not valid_dirs:
        print("❌ No valid directories to search for Python scripts.")
        return

    # Ensure all relevant directories are included
    scripts = test_find_python_scripts(*valid_dirs)

    if not scripts:
        print(f"❌ No Python scripts found in {', '.join(valid_dirs)}.")
        return

    print(f"🚀 Running checks on {len(scripts)} scripts...\n")
    for script in scripts:
        test_check_script_execution(script)

    # Add debugging for pytest test discovery
    print(f"\n🔍 Discovering pytest tests in the test directory: {TEST_DIR}")
    pytest_args = [TEST_DIR]
    
    # Run pytest discovery with verbose output to show why no tests are found
    result = subprocess.run(["pytest", *pytest_args, "--maxfail=5", "--disable-warnings", "-v"], capture_output=True, text=True)
    print(f"📜 Pytest discovery output:\n{result.stdout}")
    print(f"📜 Pytest discovery errors:\n{result.stderr}")

if __name__ == "__main__":
    main()