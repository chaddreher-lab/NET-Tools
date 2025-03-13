import os
import subprocess
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Set this to your main GitHub working branch directory
GITHUB_DIR = os.path.expanduser("~/NET-tools")  

# Scripts to exclude
EXCLUDED_SCRIPTS = {"sheetstopastebin.py", "infocollect.py", "something_test.py", "thebasics.py"}

def test_find_python_scripts(directory):
    """Recursively finds all Python scripts in the given directory."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and file not in EXCLUDED_SCRIPTS:
                python_files.append(os.path.join(root, file))
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
    scripts = test_find_python_scripts(GITHUB_DIR)

    if not scripts:
        print(f"No Python scripts found in {GITHUB_DIR}.")
        return

    print(f"Found {len(scripts)} Python scripts in {GITHUB_DIR}. Running checks...\n")
    for script in scripts:
        test_check_script_execution(script)

if __name__ == "__main__":
    main()