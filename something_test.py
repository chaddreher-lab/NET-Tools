import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Define directories to scan
GITHUB_DIR = os.path.abspath(os.path.expanduser("~/NET-Tools"))  # Adjust if needed
TEST_DIR = os.path.join(GITHUB_DIR, "test")  # Add test directory explicitly
RUNNER_DIR = "/home/runner/work/NET-Tools/NET-Tools"  # Explicitly include this directory

# Scripts to exclude
EXCLUDED_SCRIPTS = {"sheetstopastebin.py", "infocollect.py", "something_test.py", "thebasics.py"}

def test_find_python_scripts(*directories):
    """Recursively finds all Python scripts in the given directories."""
    python_files = []
    
    for directory in directories:
        abs_directory = os.path.abspath(directory)
        print(f"🔍 Searching in: {abs_directory}")  # Debugging output
        
        if not os.path.isdir(abs_directory):
            print(f"⚠️ Skipping non-existent directory: {abs_directory}")
            continue
        
        for root, _, files in os.walk(abs_directory):
            for file in files:
                if file.endswith(".py") and file not in EXCLUDED_SCRIPTS:
                    script_path = os.path.join(root, file)
                    python_files.append(script_path)
    
    print(f"📂 Found {len(python_files)} Python scripts.")
    return python_files

def test_check_script_execution(script_path):
    """Attempts to execute a Python script and reports success or failure."""
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
        print(f"No Python scripts found in {GITHUB_DIR}, {TEST_DIR}, or {RUNNER_DIR}.")
        return

    print(f"🚀 Running checks on {len(scripts)} scripts...\n")
    for script in scripts:
        test_check_script_execution(script)

if __name__ == "__main__":
    main()