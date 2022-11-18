import os
import string
from io import StringIO
from pathlib import Path
from typing import List

import inflect as ifl
import pyperclip
from InquirerPy.base import Choice

import prompts

inflect = ifl.engine()


class Underline:
    end = '\033[0m'
    underline = '\033[4m'


class SelectKeybindings:
    _universal = {
        "skip": [{"key": "c-d"}],
    }

    def mono(self):
        keybindings = {
            "answer": [
                {"key": "enter"},
                {"key": "c-z"}
            ],
        }

        return keybindings | self._universal

    def multi(self):
        keybindings = {
            "toggle": [
                {"key": "c-z"}
            ],
            "toggle-all-true": [
                {"key": "c-a"}
            ],
            "toggle-all-false": [
                {"key": "c-a"}
            ],
        }

        return keybindings | self._universal


def generate_gitignore(templates: List[str], remove_duplicates: bool, remove_comments: bool) -> str:
    gitignore = StringIO()

    for template in templates:
        for line in Path(f"templates/{template}.gitignore").open().readlines():
            if remove_duplicates and line in gitignore.getvalue() and line not in string.whitespace:
                continue

            if remove_comments and (line.startswith("#") or line in string.whitespace):
                continue

            gitignore.write(line)

        if template != templates[-1]:
            gitignore.write("\n")

    gitignore.seek(0)

    return gitignore.read()


def save_gitignore(templates: List[str], remove_duplicates: bool, remove_comments: bool, use_cwd: bool = False) -> None:
    while True:
        if use_cwd:
            save_path = Path.cwd() / ".gitignore"
        else:
            def path_postprocessor(path: str) -> str:
                path = Path(path)
                if path.name != ".gitignore":
                    path = path / ".gitignore"

                path.parent.mkdir(parents=True, exist_ok=True)
                return path.expanduser().resolve()

            save_path = prompts.filepath(
                message="Where should your .gitignore be saved?",
                instruction="Your answer will be interpreted as a directory.",
                long_instruction="Both absolute and relative paths are cool. "
                                 "Nonexistent directories will be created as necessary.",
                mandatory_message="You can't skip this.",
                multicolumn_complete=True,
                only_directories=True,
                validate=lambda path: bool(path),
                invalid_message="You must enter a path.",
                filter=path_postprocessor,
                transformer=path_postprocessor,
                qmark="•",
                amark="✓").execute()

        if save_path.exists():
            overwrite_choices = [
                Choice(name="Overwrite it", value=True),
                Choice(name="Choose another place", value=False),
            ]

            overwrite = prompts.select(
                message="A .gitignore file already exists there. What do you wanna do?",
                choices=overwrite_choices,
                mandatory_message="You can't skip this.",
                qmark="•",
                amark="✓").execute()

            if overwrite:
                gitignore = generate_gitignore(templates, remove_duplicates, remove_comments)
                save_path.write_text(gitignore)
                break
            else:
                use_cwd = False
                continue

        else:
            if save_path.name != ".gitignore":
                save_path.mkdir(parents=True, exist_ok=True)

            gitignore = generate_gitignore(templates, remove_duplicates, remove_comments)

            save_path.write_text(gitignore)
            break

    print(f"\n.gitignore saved to {save_path}.")


def main():
    multiselect_controls = ("↑/↓: Move up and down\n"
                            "Control + Z: Toggle selection\n"
                            "Control + A: Toggle all on/off\n"
                            "Enter: Confirm\n")

    template_names = [Path(f).with_suffix("").name for f in os.listdir("templates") if f.endswith(".gitignore")]
    template_names.sort(key=str.casefold)
    templates = prompts.fuzzy(
        message="Choose some templates.",
        instruction="You can type to search for specific ones.",
        long_instruction=multiselect_controls,
        choices=template_names,
        multiselect=True,
        qmark="•",
        amark="✓",
        mandatory_message="You can't skip this.",
        transformer=lambda result: f"Generating from {inflect.no('template', len(result))}."
    ).execute()

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

    modifiers = prompts.select(message="Cool. Now choose some options.",
                               instruction="(You can also skip this question with Control + D.)",
                               long_instruction=multiselect_controls,
                               choices=modifier_choices,
                               multiselect=True,
                               mandatory=False,
                               qmark="•",
                               amark="✓",
                               transformer=lambda result: modifier_transformer(result)).execute() or []

    remove_duplicates, remove_comments = "no_duplicates" in modifiers, "no_comments" in modifiers

    output_choices = [
        Choice(name="Save to current directory", value="cwd"),
        Choice(name="Save to another directory", value="elsewhere"),
        Choice(name="Print to stdout", value="stdout"),
        Choice(name="Copy to clipboard", value="clipboard"),
    ]

    output = prompts.select(message="Gotcha. Now choose a place to save your .gitignore.",
                            choices=output_choices,
                            qmark="•",
                            amark="✓",
                            mandatory_message="You can't skip this.").execute()

    if output == "cwd":
        save_gitignore(templates, remove_duplicates, remove_comments, use_cwd=True)
    elif output == "elsewhere":
        save_gitignore(templates, remove_duplicates, remove_comments)
    elif output == "stdout":
        gitignore = generate_gitignore(templates, remove_duplicates, remove_comments)
        print(f"\n{Underline.underline}Generated .gitignore{Underline.end}\n{gitignore}")
    elif output == "clipboard":
        gitignore = generate_gitignore(templates, remove_duplicates, remove_comments)
        pyperclip.copy(gitignore)
        print("\n.gitignore copied to clipboard.")


if __name__ == '__main__':
    main()
