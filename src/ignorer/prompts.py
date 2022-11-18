from InquirerPy import inquirer


def prompt_decorator(func):
    def wrapper(*args, **kwargs):
        if kwargs.get("multiselect"):
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
        else:
            keybindings = {
                "answer": [
                    {"key": "enter"},
                    {"key": "c-z"}
                ],
            }

        keybindings["skip"] = [{"key": "c-d"}]

        kwargs["keybindings"] = keybindings
        kwargs["qmark"] = "•"
        kwargs["amark"] = "✓"
        kwargs["mandatory_message"] = "You can't skip this."

        return func(*args, **kwargs)

    return wrapper


@prompt_decorator
def checkbox(*args, **kwargs):
    return inquirer.checkbox(*args, **kwargs)


@prompt_decorator
def confirm(*args, **kwargs):
    return inquirer.confirm(*args, **kwargs)


@prompt_decorator
def expand(*args, **kwargs):
    return inquirer.expand(*args, **kwargs)


@prompt_decorator
def filepath(*args, **kwargs):
    return inquirer.filepath(*args, **kwargs)


@prompt_decorator
def fuzzy(*args, **kwargs):
    return inquirer.fuzzy(*args, **kwargs)


@prompt_decorator
def text(*args, **kwargs):
    return inquirer.text(*args, **kwargs)


@prompt_decorator
def select(*args, **kwargs):
    return inquirer.select(*args, **kwargs)


@prompt_decorator
def number(*args, **kwargs):
    return inquirer.number(*args, **kwargs)


@prompt_decorator
def rawlist(*args, **kwargs):
    return inquirer.rawlist(*args, **kwargs)


@prompt_decorator
def secret(*args, **kwargs):
    return inquirer.secret(*args, **kwargs)
