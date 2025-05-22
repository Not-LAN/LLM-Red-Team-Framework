import importlib
import os
import pkgutil
from typing import List, Dict

def discover_modules(base_package: str = "modules") -> List[str]:
    """
    Recursively discover all test modules inside the given base package.
    Returns a list of module import paths to be loaded and run.
    """
    modules = []
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Convert dot path (e.g. modules.injection) to file path
    folder_path = base_package.replace(".", "/")
    package_path = os.path.abspath(os.path.join(base_dir, "..", folder_path))

    print(f"[DEBUG] Scanning modules recursively from: {package_path}")
    # Walk through packages/modules in the target directory
    for importer, modname, ispkg in pkgutil.walk_packages(path=[package_path], prefix=f"{base_package}."):
        print(f"[DEBUG] Found: {modname} (pkg: {ispkg})")
        if not ispkg and ".test_" in modname:
            modules.append(modname)

    print(f"[DEBUG] Final module list: {modules}")
    return modules

def run_module(module_path: str, model) -> Dict:
    """
    Dynamically import a module and run its run_test function.
    """
    try:
        module = importlib.import_module(module_path)
        if hasattr(module, "run_test"):
            return module.run_test(model)
        return {"module": module_path, "error": "No run_test() in module."}
    except Exception as e:
        return {"module": module_path, "error": str(e)}

def run_all_modules(model, base_package: str = "modules") -> List[Dict]:
    """
    Discover and run all test modules.
    """
    module_paths = discover_modules(base_package)
    print(f"[DEBUG] Modules to run: {module_paths}")

    results = []
    for mod_path in module_paths:
        result = run_module(mod_path, model)
        print(f"[DEBUG] Ran: {mod_path} → result: {result}")
        results.append(result)
    return results