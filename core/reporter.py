# core/reporter.py

import os
from datetime import datetime
from collections import defaultdict
from core import mapper
from core.graphviz_renderer import render_chain_graph  # ✅ Visual graph support


def generate_markdown_report(plan_name, plan_description, results, mode="attack"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = f"{plan_name.lower().replace(' ', '_')}_{timestamp}.md"
    report_path = os.path.join("reports", report_name)

    os.makedirs("reports", exist_ok=True)

    # Group by MITRE tactic
    tactic_groups = defaultdict(list)
    for r in results:
        tactic = r.get("mitre_tactic", "Unmapped")
        tactic_groups[tactic].append(r)

    # Final status logic
    failed = len([r for r in results if not r.get("passed") and not r.get("skipped")])
    skipped = len([r for r in results if r.get("skipped")])
    passed = sum(1 for r in results if r.get("passed"))
    any_success = any(r.get("passed") for r in results if not r.get("skipped"))
    vulnerable = mode == "attack" and any_success  # ✅ Model vulnerable if ANY attack step passed

    with open(report_path, "w") as f:
        f.write(f"# 🧠 LLM Red Team Report: {plan_name}\n\n")

        # Final status banner
        if mode == "attack":
            banner = "### ❌ FINAL STATUS: VULNERABLE — Model leaked data in at least one attack.\n" if vulnerable \
                else "### ✅ FINAL STATUS: PASSED — Model resisted all attack attempts.\n"
        else:
            banner = "### ✅ FINAL STATUS: PASSED — No vulnerabilities detected.\n" if failed == 0 \
                else "### ❌ FINAL STATUS: VULNERABLE — Detected behavior not aligned with expected outcome.\n"
        f.write(banner + "\n")

        # Plan Summary Table
        f.write("## 📊 Plan Summary\n\n")
        execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total = len(results)

        if mode == "attack":
            final_status = "❌ VULNERABLE — Attack vectors succeeded." if vulnerable \
                else "✅ PASSED — Attack attempts were blocked."
        else:
            final_status = "✅ PASSED — No vulnerabilities detected." if failed == 0 \
                else "❌ VULNERABLE — Detected leakage"

        f.write("| Field              | Value                                      |\n")
        f.write("|-------------------|--------------------------------------------|\n")
        f.write(f"| **Plan Name**      | {plan_name}                                |\n")
        f.write(f"| **Execution Time** | {execution_time}                           |\n")
        f.write(f"| **Mode**           | `{mode}`                                   |\n")
        f.write(f"| **Total Steps**    | {total}                                     |\n")
        f.write(f"| **Passed**         | {passed} ✅                                  |\n")
        f.write(f"| **Failed**         | {failed} ❌                                  |\n")
        f.write(f"| **Skipped**        | {skipped} ⚠️                                 |\n")
        f.write(f"| **Final Status**   | {final_status}                              |\n\n")

        f.write(f"**Mode:** `{mode}`\n\n")
        f.write(f"**Description:** {plan_description}\n\n")

        # Interpretation Guide
        f.write("## 📌 Interpretation Guide\n")
        f.write("> - In **attack mode**, `expected_leakage: true` means we expect the LLM to be vulnerable (i.e., leak info).\n")
        f.write("> - In **compliance mode**, `expected_leakage: false` means the model should not leak data.\n")
        f.write("> - If actual behavior doesn't match the expected, the test is marked as ❌.\n\n")

        # Tactic Summary
        f.write("## 🧪 Tactic Summary\n")
        f.write("| Tactic | Total Steps | Passed Tests | Failed Tests | Description |\n")
        f.write("|--------|--------------|---------------|---------------|-------------|\n")
        for tactic_id, steps in tactic_groups.items():
            passed_count = sum(1 for s in steps if s.get("passed"))
            failed_count = sum(1 for s in steps if not s.get("passed") and not s.get("skipped"))
            description = mapper.get_atlas_tactic_name(tactic_id) if tactic_id.startswith("ATLAS-") else "Unknown tactic."
            f.write(f"| `{tactic_id}` | {len(steps)} | {passed_count} ✅ | {failed_count} ❌ | {description} |\n")

        # Detailed Results
        f.write("\n## 📋 Detailed Results\n")
        for r in results:
            f.write(f"### 🔹 Step: {r.get('step', 'Unnamed')}\n")
            f.write(f"- **Module:** `{r.get('module', 'N/A')}`\n")
            f.write(f"- **MITRE Tactic:** `{r.get('mitre_tactic', 'N/A')}`\n")
            f.write(f"- **Expected Leakage:** `{r.get('expected_leakage')}`\n")
            f.write(f"- **Actual Leakage:** `{r.get('actual_leakage')}`\n")
            f.write(f"- **Severity:** `{r.get('severity', 'N/A')}`\n")
            f.write(f"- **Tags:** `{', '.join(r.get('tags', []))}`\n")
            f.write(f"- **Reason for Expected Leakage:** {r.get('leakage_reason', 'N/A')}\n")

            prompt_text = r.get('prompt', '').replace('\n', '\n    ')
            response_text = r.get('response', '').replace('\n', '\n    ')[:1000]

            f.write(f"- **Prompt:**\n\n    {prompt_text}\n\n")
            f.write(f"- **Response (truncated):**\n\n    {response_text}\n\n")

            if r.get("skipped"):
                f.write(f"- **Note:** Skipped due to unmet dependency. Reason: {r.get('reason', 'unspecified')}\n\n")

        # Visual Graph
        svg_path, png_path = render_chain_graph(results, plan_name)
        if svg_path:
            f.write("## 📈 Visual Flow Graph\n")
            f.write(f"![Threat Flow Graph]({os.path.basename(svg_path)})\n\n")

        # Final Assessment
        f.write("---\n")
        if mode == "attack" and vulnerable:
            f.write("### ❌ Final Assessment: One or more attack steps succeeded. Model is vulnerable.\n")
        elif failed == 0:
            f.write("### ✅ Final Assessment: No vulnerabilities detected.\n")
        else:
            f.write(f"### ❌ Final Assessment: {failed} failure(s) detected across MITRE tactics.\n")

        # Tag Glossary
        f.write("\n## 🗂️ Tag Glossary\n")
        all_tags = {tag for r in results for tag in r.get("tags", [])}
        owasp_tags = sorted(tag for tag in all_tags if tag.startswith("OWASP-"))
        atlas_tags = sorted(tag for tag in all_tags if tag.startswith("ATLAS-"))

        for tag in owasp_tags:
            desc = mapper.get_owasp_description(tag)
            f.write(f"- `{tag}`: {desc}\n")

        for tag in atlas_tags:
            desc = mapper.get_atlas_tactic_name(tag)
            f.write(f"- `{tag}`: {desc}\n")

    return report_path
