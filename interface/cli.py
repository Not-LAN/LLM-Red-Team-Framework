# interface/cli.py

import typer
import yaml
from core import engine, plan_runner, reporter
from runners.openai_runner import OpenAIInterface
from runners.gemini_runner import GeminiInterface
from runners.mistral_runner import MistralInterface  # ✅ New

app = typer.Typer()
cli = typer.Typer()
app.add_typer(cli, name="tests")

@app.command()
def hello():
    """Sanity test command."""
    typer.echo("LLM Red Team CLI is alive.")

def load_model(model: str):
    if model == "openai":
        return OpenAIInterface()
    elif model == "gemini":
        return GeminiInterface()
    elif model == "mistral":
        return MistralInterface()
    elif model == "custom":
        from runners.custom_runner import CustomLLMInterface
        return CustomLLMInterface()
    else:
        typer.echo("Unsupported model. Choose from: openai, gemini, mistral, custom")
        raise typer.Exit(code=1)

@cli.command("run-all")
def run_all(model: str = typer.Option("openai", help="Model backend: openai, gemini, mistral, custom")):
    llm = load_model(model)
    typer.echo("[DEBUG] CLI has called engine.run_all_modules()")
    results = engine.run_all_modules(llm)

    if not results:
        typer.echo("[!] No test modules were found or executed.")

    for result in results:
        typer.echo("\n--- Result ---")
        typer.echo(f"Module: {result.get('module', 'N/A')}")
        typer.echo(f"Success: {result.get('success', False)}")
        typer.echo(f"Severity: {result.get('severity', 'unknown')}")
        typer.echo(f"Tags: {result.get('tags', [])}")
        typer.echo(f"Prompt: {result.get('prompt', '')}")
        typer.echo(f"Response: {result.get('response', '')[:300]}...")

@cli.command("run-module")
def run_module_command(
    module: str = typer.Argument(..., help="Full dotted path to module"),
    model: str = typer.Option("openai", help="Model backend: openai, gemini, mistral, custom")
):
    llm = load_model(model)
    typer.echo(f"[DEBUG] Running module: {module}")
    result = engine.run_module(module, llm)

    typer.echo("--- Result ---")
    typer.echo(f"Module: {result.get('module', 'N/A')}")
    if 'error' in result:
        typer.echo(f"[ERROR] {result['error']}")
        raise typer.Exit(code=1)

    typer.echo(f"Success: {result.get('success', False)}")
    typer.echo(f"Severity: {result.get('severity', 'unknown')}")
    typer.echo(f"Tags: {result.get('tags', [])}")
    typer.echo(f"Prompt: {result.get('prompt', '')}")
    typer.echo(f"Response: {result.get('response', '')[:300]}...")

@cli.command("run-category")
def run_category(
    category: str = typer.Argument(..., help="Subfolder in modules/, e.g., injection, evasion"),
    model: str = typer.Option("openai", help="Model backend: openai, gemini, mistral, custom")
):
    llm = load_model(model)
    base_package = f"modules.{category}"
    results = engine.run_all_modules(llm, base_package=base_package)

    if not results:
        typer.echo("[!] No test modules were found in this category.")

    for result in results:
        typer.echo("\n--- Result ---")
        typer.echo(f"Module: {result.get('module', 'N/A')}")
        if 'error' in result:
            typer.echo(f"[ERROR] {result['error']}")
            continue
        typer.echo(f"Success: {result.get('success', False)}")
        typer.echo(f"Severity: {result.get('severity', 'unknown')}")
        typer.echo(f"Tags: {result.get('tags', [])}")
        typer.echo(f"Prompt: {result.get('prompt', '')}")
        typer.echo(f"Response: {result.get('response', '')[:300]}...")

@app.command("run-plan")
def run_plan(
    plan_path: str = typer.Argument(..., help="Path to emulation YAML file."),
    model: str = typer.Option("openai", help="Model backend: openai, gemini, mistral, custom"),
    strict: bool = typer.Option(False, help="Fail immediately on first failed step")
):
    llm = load_model(model)
    results = plan_runner.run_plan(plan_path, llm, strict=strict)

    with open(plan_path, 'r') as f:
        plan_yaml = yaml.safe_load(f)

    mode = plan_yaml.get("mode", "")
    report_path = reporter.generate_markdown_report(
        plan_name=plan_yaml.get("name", "Unnamed Plan"),
        plan_description=plan_yaml.get("description", ""),
        results=results,
        mode=mode
    )

    typer.echo(f"\n📄 Markdown report saved to: {report_path}")

    for result in results:
        typer.echo("\n--- Step Result ---")
        typer.echo(f"Step: {result.get('step', 'N/A')}")
        typer.echo(f"Module: {result.get('module', 'N/A')}")
        typer.echo(f"Expected Leakage: {result.get('expected_leakage')}")
        typer.echo(f"Actual Leakage: {result.get('actual_leakage')}")
        typer.echo(f"Severity: {result.get('severity', 'N/A')}")
        typer.echo(f"Tags: {', '.join(result.get('tags', []))}")
        typer.echo(f"Prompt: {result.get('prompt', '')[:150]}")
        typer.echo(f"Response: {result.get('response', '')[:300]}...")

    failed = [r for r in results if r.get("actual_leakage") != r.get("expected_leakage") and not r.get("skipped")]
    if failed:
        typer.echo(f"\n❌ {len(failed)} steps failed.")
    else:
        typer.echo("\n✅ All steps passed.")

if __name__ == "__main__":
    app()
