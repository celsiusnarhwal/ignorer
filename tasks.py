from pathlib import Path

import invoke
from invoke import task


@task(aliases=["hbf"], optional=["--verbose"])
def build_formula(ctx, package, verbose=False):
    formula_name = "ignorer"
    formula_description = "Generate .gitignore files from your command line"
    formula_homepage = "https://github.com/celsiusnarhwal/ignorer"
    formula_python_version = 3
    formula_path = Path(f"houkago-tea-tap/Formula/{formula_name}.rb")

    cmds = [
        "python -m venv venv",
        "source venv/bin/activate",
        f"pip install {package} homebrew-pypi-poet --no-cache-dir",
        f"poet -f {package} > {formula_path}",
        "rm -rf venv",
    ]

    invoke.run(" && ".join(cmds), hide=not verbose)

    with formula_path.open("a+") as formula:
        formula.seek(0)
        text = f"# Homebrew formula for {package}. {formula_homepage}\n\n"
        text += formula.read()
        text = (text.replace('desc "Shiny new formula"', f'desc "{formula_description}"', 1)
                .replace('homepage ""', f'homepage "{formula_homepage}"', 1))

        if type(formula_python_version) == int:
            text = text.replace('depends_on "python3"', f'depends_on "python{formula_python_version}"', 1)
        else:
            text = text.replace('depends_on "python3"', f'depends_on "python@{formula_python_version}"', 1)

        formula.truncate(0)
        formula.write(text)
