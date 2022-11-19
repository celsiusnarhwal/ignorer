import invoke
from invoke import task


@task
def build_formula(ctx, package, formula_name=None):
    formula_name = formula_name or package

    cmds = [
        "python -m venv venv",
        "source venv/bin/activate",
        f"pip install {package} homebrew-pypi-poet",
        f"poet -f {package} > homebrew/{formula_name}.rb",
        "rm -rf venv",
    ]

    invoke.run(" && ".join(cmds))
