import platform
import psutil

def system_info():
    """Print system information."""
    print("System:", platform.system())
    print("Version:", platform.version())
    print("Processor:", platform.processor())
    print("RAM:", psutil.virtual_memory().total / (1024**3), "GB")