import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
def test_main():
    main()
def check_secret(secret_name):
    secret_value = os.getenv(secret_name)
    if secret_value:
        print(f"{secret_name}: ✅ Loaded successfully (Length: {len(secret_value)} characters)")
    else:
        print(f"{secret_name}: ❌ Not found")

def main():
    print("Checking GitHub Secrets availability...\n")
    
    # List of secrets to check
    secrets_to_check = [
        "PASTEBIN_API",  # Add more secrets as needed
        "TEST",
    ]
    
    for secret in secrets_to_check:
        check_secret(secret)
    
    print("\nSecret validation complete!")

if __name__ == "__main__":
    main()