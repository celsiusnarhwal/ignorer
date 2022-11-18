from InquirerPy import inquirer


def keybindings_decorator(func):
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

        return func(*args, **kwargs)

    return wrapper


@keybindings_decorator
def checkbox(*args, **kwargs):
    return inquirer.checkbox(*args, **kwargs)


@keybindings_decorator
def confirm(*args, **kwargs):
    return inquirer.confirm(*args, **kwargs)


@keybindings_decorator
def expand(*args, **kwargs):
    return inquirer.expand(*args, **kwargs)


@keybindings_decorator
def filepath(*args, **kwargs):
    return inquirer.filepath(*args, **kwargs)


@keybindings_decorator
def fuzzy(*args, **kwargs):
    return inquirer.fuzzy(*args, **kwargs)


@keybindings_decorator
def text(*args, **kwargs):
    return inquirer.text(*args, **kwargs)


@keybindings_decorator
def select(*args, **kwargs):
    return inquirer.select(*args, **kwargs)


@keybindings_decorator
def number(*args, **kwargs):
    return inquirer.number(*args, **kwargs)


@keybindings_decorator
def rawlist(*args, **kwargs):
    return inquirer.rawlist(*args, **kwargs)


@keybindings_decorator
def secret(*args, **kwargs):
    return inquirer.secret(*args, **kwargs)
