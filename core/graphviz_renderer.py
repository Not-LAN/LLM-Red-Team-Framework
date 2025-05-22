# core/graphviz_renderer.py

from graphviz import Digraph
import os

def render_chain_graph(results, plan_name):
    dot = Digraph(comment="LLM Emulation Chain", format='svg')
    dot.attr(rankdir="LR", size="8,5")

    step_nodes = {}
    for idx, r in enumerate(results):
        step_id = f"step{idx}"
        label = r.get("step", f"Step {idx + 1}")
        status = "✅" if r.get("passed") else ("⚠️" if r.get("skipped") else "❌")
        tactic = r.get("mitre_tactic", "N/A")
        label += f"\n{status} {tactic}"

        # Color styling
        if r.get("skipped"):
            color = "gray"
        elif r.get("passed"):
            color = "green"
        else:
            color = "red"

        dot.node(step_id, label=label, style="filled", fillcolor=color, fontname="Helvetica")
        step_nodes[label] = step_id

    # Add edges for dependent steps
    for idx, r in enumerate(results):
        if "depends_on" in r:
            source_label = r["depends_on"]
            target_id = f"step{idx}"
            for lbl, node_id in step_nodes.items():
                if lbl.startswith(source_label):
                    dot.edge(node_id, target_id)

    # Prepare file name
    safe_name = plan_name.lower().replace(" ", "_")
    output_base = os.path.join("reports", f"{safe_name}_chain")

    os.makedirs("reports", exist_ok=True)

    # Render both SVG and PNG
    svg_path = dot.render(filename=output_base, format="svg", cleanup=True)
    png_path = dot.render(filename=output_base, format="png", cleanup=True)

    return svg_path, png_path
