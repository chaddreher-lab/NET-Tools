import sys

sys.stdout.reconfigure(encoding="utf-8")


def load_env_file(env_path=".env"):
    """Loads key-value pairs from a .env file into a dictionary."""
    env_vars = {}
    try:
        with open(env_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"❌ Error: {env_path} file not found.")
    return env_vars


def check_all_secrets(env_vars):
    """Checks all secrets loaded from the .env file."""
    if not env_vars:
        print("❌ No secrets found in the .env file.")
        return

    print("Checking all secrets in .env file...\n")
    for secret_name, secret_value in env_vars.items():
        print(
            f"{secret_name}: ✅ Loaded successfully (Length: {len(secret_value)} characters)"
        )

    print("\nSecret validation complete!")


def main():
    env_vars = load_env_file()
    check_all_secrets(env_vars)


if __name__ == "__main__":
    main()