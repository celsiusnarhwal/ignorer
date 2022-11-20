from pathlib import Path

import invoke
from invoke import task


@task(aliases=["hbf"], optional=["--verbose"])
def build_formula(ctx, package, verbose=False):
    formula_name = "ignorer"
    formula_description = "Generate .gitignore files from your command line"
    formula_homepage = "https://github.com/celsiusnarhwal/ignorer"
    minimum_python_version = "3.10"

    cmds = [
        "python -m venv venv",
        "source venv/bin/activate",
        f"pip install {package} homebrew-pypi-poet --no-cache-dir",
        f"poet -f {package} > homebrew-formulae/Formula/{formula_name}.rb",
        "rm -rf venv",
    ]

    invoke.run(" && ".join(cmds), hide=not verbose)

    with (Path(__file__).parent / "homebrew-formulae" / "Formula" / f"{formula_name}.rb").open("a+") as formula:
        formula.seek(0)
        text = f"# Homebrew formula for {package}. {formula_homepage}\n\n"
        text += formula.read()
        text = (text.replace('desc "Shiny new formula"', f'desc "{formula_description}"', 1)
                .replace('homepage ""', f'homepage "{formula_homepage}"', 1)
                .replace('depends_on "python3"', f'depends_on "python@{minimum_python_version}"', 1))
        formula.truncate(0)
        formula.write(text)
