import os
import ctypes

def add_env_var():
    var_name = input("🔹 Enter the variable name: ")
    var_value = input("🔹 Enter the variable value: ")
    
    os.system(f'setx {var_name} "{var_value}"')
    os.environ[var_name] = var_value
    print(f"✅ {var_name} set to {var_value}")

def remove_env_var():
    var_name = input("🔸 Enter the variable name to remove: ")
    
    os.system(f'reg delete HKCU\\Environment /F /V {var_name}')
    os.environ.pop(var_name, None)
    print(f"❌ {var_name} has been removed")

def list_env_vars():
    print("\n📜 Listing all environment variables:\n")
    for key, value in os.environ.items():
        print(f"{key} = {value}")

def main():
    while True:
        print("\n🌍 Environment Variable Manager (Windows) 🌍")
        print("1️⃣  Add Environment Variable")
        print("2️⃣  Remove Environment Variable")
        print("3️⃣  List All Environment Variables")
        print("4️⃣  🚪 Exit")
        
        choice = input("➡️  Enter your choice: ")
        
        if choice == "1":
            add_env_var()
        elif choice == "2":
            remove_env_var()
        elif choice == "3":
            list_env_vars()
        elif choice == "4":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("⚠️ Invalid choice, please try again.")

if __name__ == "__main__":
    main()