import importlib
import traceback
import yaml

def run_plan(plan_path, llm, strict=False):
    with open(plan_path, 'r') as f:
        plan = yaml.safe_load(f)

    results = []
    step_status = {}  # Track pass/fail for each step by name

    for step in plan.get("steps", []):
        step_name = step.get("step")
        module_path = step.get("module")
        expected_leakage = step.get("expected_leakage", False)
        mitre_tactic = step.get("mitre_tactic", None)
        depends_on = step.get("depends_on")

        # Skip this step if dependency failed
        if depends_on and not step_status.get(depends_on, False):
            result = {
                "step": step_name,
                "module": module_path,
                "skipped": True,
                "reason": f"Dependency '{depends_on}' failed or was skipped.",
                "expected_leakage": expected_leakage,
                "actual_leakage": None,
                "passed": False,
                "mitre_tactic": mitre_tactic,
            }
            results.append(result)
            step_status[step_name] = False
            continue

        try:
            module = importlib.import_module(module_path)
            result = module.run_test(llm)
        except Exception as e:
            result = {
                "step": step_name,
                "module": module_path,
                "error": str(e),
                "traceback": traceback.format_exc(),
                "expected_leakage": expected_leakage,
                "actual_leakage": False,
                "passed": False,
                "mitre_tactic": mitre_tactic,
                "skipped": False,
            }
            results.append(result)
            step_status[step_name] = False
            if strict:
                break
            continue

        actual_leakage = result.get("success", False)
        passed = actual_leakage == expected_leakage

        result.update({
            "step": step_name,
            "expected_leakage": expected_leakage,
            "actual_leakage": actual_leakage,
            "passed": passed,
            "mitre_tactic": mitre_tactic,
            "skipped": False,
        })

        results.append(result)
        step_status[step_name] = passed

        if strict and not passed:
            break

    return results
