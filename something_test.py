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
EXCLUDED_SCRIPTS = {"sheetstopastebin.py", "infocollect.py", "something_test.py", "thebasics.py"}

@pytest.fixture
def directory():
    """Fixture to return the directory to scan."""
    return os.getcwd()  # Adjust if you want a different base directory for scanning

@pytest.fixture
def script_path():
    """Fixture to return the script path for testing execution."""
    return os.path.join(os.getcwd(), "something_test.py")  # Adjust as needed to point to your script

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
    try:
        result = subprocess.run(
            ["python", script_path], capture_output=True, text=True, timeout=30, encoding="utf-8"
        )
        if result.returncode == 0:
            print(f"✅ SUCCESS: {script_path}")
        else:
            print(f"❌ ERROR: {script_path}\nOutput:\n{result.stderr}")
    except Exception as e:
        print(f"⚠️ EXCEPTION: {script_path} - {e}")

def main():
    # Ensure all relevant directories are included
    scripts = test_find_python_scripts(GITHUB_DIR, TEST_DIR, RUNNER_DIR)

    if not scripts:
        print(f"❌ No Python scripts found in {GITHUB_DIR}, {TEST_DIR}, or {RUNNER_DIR}.")
        return

    print(f"🚀 Running checks on {len(scripts)} scripts...\n")
    for script in scripts:
        test_check_script_execution(script)

if __name__ == "__main__":
    main()
