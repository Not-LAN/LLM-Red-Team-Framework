# core/graphviz_renderer.py

from graphviz import Digraph
import os

def render_chain_graph(results, plan_name, mode="attack"):  # Accept mode
    dot = Digraph(comment="LLM Emulation Chain", format='svg')
    dot.attr(rankdir="LR", size="8,5")

    step_nodes = {}
    for idx, r in enumerate(results):
        step_id = f"step{idx}"
        label = r.get("step", f"Step {idx + 1}")
        tactic = r.get("mitre_tactic", "N/A")

        # Decide color + status icon
        if r.get("skipped"):
            status_icon = "⚠️"
            color = "gray"
        elif mode == "attack":
            if r.get("passed"):
                status_icon = "❌"  # Attack succeeded → bad
                color = "red"
            else:
                status_icon = "✅"  # Attack blocked → good
                color = "green"
        else:  # compliance
            if r.get("passed"):
                status_icon = "✅"  # Compliance success
                color = "green"
            else:
                status_icon = "❌"
                color = "red"

        label += f"\n{status_icon} {tactic}"
        dot.node(step_id, label=label, style="filled", fillcolor=color, fontname="Helvetica")
        step_nodes[label] = step_id

    # Add dependency edges
    for idx, r in enumerate(results):
        if "depends_on" in r:
            source_label = r["depends_on"]
            target_id = f"step{idx}"
            for lbl, node_id in step_nodes.items():
                if lbl.startswith(source_label):
                    dot.edge(node_id, target_id)

    # Output paths
    safe_name = plan_name.lower().replace(" ", "_")
    output_base = os.path.join("reports", f"{safe_name}_chain")
    os.makedirs("reports", exist_ok=True)

    svg_path = dot.render(filename=output_base, format="svg", cleanup=True)
    png_path = dot.render(filename=output_base, format="png", cleanup=True)

    return svg_path, png_path
