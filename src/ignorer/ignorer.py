import itertools
import string
from io import StringIO
from pathlib import Path
from typing import List

import click
import inflect as ifl
import pyperclip
from InquirerPy.base import Choice

from ignorer import prompts

inflect = ifl.engine()

multiselect_controls = ("↑/↓: Move up and down\n"
                        "Control + Z: Toggle selection\n"
                        "Control + A: Toggle all on/off\n"
                        "Enter: Confirm\n")


class Underline:
    end = '\033[0m'
    underline = '\033[4m'


def generate_gitignore(templates: List[Path], remove_duplicates: bool, remove_comments: bool) -> str:
    gitignore = StringIO()

    for template in templates:
        for line in template.open().readlines():
            if remove_duplicates and line in gitignore.getvalue() and line not in string.whitespace:
                continue

            if remove_comments and (line.startswith("#") or line in string.whitespace):
                continue

            gitignore.write(line)

        if template != templates[-1] and not remove_comments:
            gitignore.write("\n")

    gitignore.seek(0)

    return gitignore.read()


def save_gitignore(gitignore: str, use_cwd: bool = False) -> None:
    while True:
        if use_cwd:
            save_path = Path.cwd() / ".gitignore"
        else:
            def path_postprocessor(path: str) -> str:
                path = Path(path).joinpath(".gitignore")

                path.parent.mkdir(parents=True, exist_ok=True)
                return path.expanduser().resolve()

            save_path = prompts.filepath(
                message="Where should your .gitignore be saved?",
                instruction="Enter a path.",
                long_instruction="Both absolute and relative paths are supported.\n"
                                 "Nonexistent directories will be created as necessary.",
                multicolumn_complete=True,
                only_directories=True,
                validate=lambda path: bool(path),
                invalid_message="You must enter a path.",
                filter=path_postprocessor,
                transformer=path_postprocessor).execute()

        if save_path.exists():
            overwrite_choices = [
                Choice(name="Overwrite it", value=True),
                Choice(name="Choose another place", value=False),
            ]

            overwrite = prompts.select(
                message="A .gitignore file already exists there. What do you wanna do?",
                choices=overwrite_choices).execute()

            if overwrite:
                save_path.write_text(gitignore)
                break
            else:
                use_cwd = False
                continue

        else:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_text(gitignore)
            break

    print(f"\n.gitignore saved to {save_path}.")


def get_templates() -> List[Path]:
    categories = [
        Choice(name="Languages and frameworks", value=["*.gitignore", "community/**/*.gitignore"]),
        Choice(name="Editors and operating systems", value=["Global/*.gitignore"]),
        Choice(name="Just show me everything", value=[]),
    ]

    category = (prompts.select(message="Choose a category.", choices=categories).execute() or
                itertools.chain.from_iterable([choices.value for choices in categories]))

    repo_path = Path(__file__).parent / "gitignore"
    templates: List[Path] = []

    for template in itertools.chain(*[repo_path.glob(pattern) for pattern in category]):
        name = template.stem

        if template.parent.name == "Global" and any(t.name == template.stem for t in templates):
            name += " (Global)"

        templates.append(Choice(name=name, value=template))

    templates.sort(key=lambda t: t.name.lower())

    return prompts.fuzzy(
        message="Choose some templates.",
        instruction="You can type to search for specific ones.",
        long_instruction=multiselect_controls,
        choices=templates,
        multiselect=True,
        transformer=lambda result: f"Generating from {inflect.no('template', len(result))}."
    ).execute()


def get_modifiers() -> List[str]:
    modifier_choices = [
        Choice(name="Generate without duplicates", value="no_duplicates"),
        Choice(name="Generate without comments and empty lines", value="no_comments"),
    ]

    def modifier_transformer(result: List[str]) -> str:
        modifier_transformations = {
            "Generate without duplicates": ["duplicates"],
            "Generate without comments and empty lines": ["comments", "empty lines"],
        }

        words = [x for sublist in [modifier_transformations[r] for r in result] for x in sublist]
        return f"Generating without {inflect.join(words, conj='or')}."

    modifiers = prompts.select(message="Choose some options.",
                               instruction="Or skip this question with Control + D.",
                               long_instruction=multiselect_controls,
                               choices=modifier_choices,
                               multiselect=True,
                               mandatory=False,
                               transformer=lambda result: modifier_transformer(result)).execute() or []

    return modifiers


def get_output() -> str:
    output_choices = [
        Choice(name="Save to current directory", value="cwd"),
        Choice(name="Save to another directory", value="elsewhere"),
        Choice(name="Print to stdout", value="stdout"),
        Choice(name="Copy to clipboard", value="clipboard"),
    ]

    output = prompts.select(message="Choose how to save your .gitignore.",
                            choices=output_choices).execute()

    return output


def main():
    print("ignorer © 2022-present celsius narhwal. Licensed under MIT (see --license).\n")
    templates = get_templates()
    modifiers = get_modifiers()
    output = get_output()

    remove_duplicates, remove_comments = "no_duplicates" in modifiers, "no_comments" in modifiers

    gitignore = generate_gitignore(templates, remove_duplicates, remove_comments)

    if output == "cwd":
        save_gitignore(gitignore, use_cwd=True)
    elif output == "elsewhere":
        save_gitignore(gitignore)
    elif output == "stdout":
        print(f"\n{Underline.underline}Generated .gitignore{Underline.end}\n{gitignore}")
    elif output == "clipboard":
        pyperclip.copy(gitignore)
        print("\n.gitignore copied to clipboard.")


@click.command()
@click.option("--license", "show_license", is_flag=True, help="See ignorer's license.")
def cli(show_license: bool):
    if show_license:
        print((Path(__file__).parent / "LICENSE").read_text())
    else:
        while True:
            try:
                main()
                break
            except (KeyboardInterrupt, EOFError):
                print("\nExiting.")
                break


if __name__ == '__main__':
    cli()
