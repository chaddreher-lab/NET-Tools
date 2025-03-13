import os
import subprocess

# Set this to your main GitHub directory
GITHUB_DIR = os.path.expanduser("~/gh/net-tools")  

def find_python_scripts(directory):
    """Recursively finds all Python scripts in the given directory."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files

def check_script_execution(script_path):
    """Attempts to execute a Python script and reports success or failure."""
    try:
        result = subprocess.run(
            ["python", script_path], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            print(f"✅ SUCCESS: {script_path}")
        else:
            print(f"❌ ERROR: {script_path}\nOutput:\n{result.stderr}")
    except Exception as e:
        print(f"⚠️ EXCEPTION: {script_path} - {e}")

def main():
    scripts = find_python_scripts(GITHUB_DIR)

    if not scripts:
        print(f"No Python scripts found in {GITHUB_DIR}.")
        return

    print(f"Found {len(scripts)} Python scripts in {GITHUB_DIR}. Running checks...\n")
    for script in scripts:
        check_script_execution(script)

if __name__ == "__main__":
    main()