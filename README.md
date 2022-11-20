# ignorer

ignorer generates .gitignore files from your command line using
GitHub's [vast repository](https://github.com/github/gitignore) of .gitignore templates.

## Installation

### pipx (recommended)

The recommended, cross-platform, way of installing ignorer is via [pipx](https://pypa.github.io/pipx/).

```bash
pipx install ignorer
```

### Homebrew

macOS users who would rather install via [Homebrew](https://brew.sh) can do that instead:

```bash
brew tap celsiusnarhwal/formulae
brew install ignorer
```

### pip (not recommended)

ignorer can be installed via pip like any other Python package, but unless you're going to make a virtual environment
for it yourself, you're strongly encouraged to use pipx or Homebrew.

```bash
pip install ignorer
```

## Usage

Simply invoke ignorer from the command line:

```bash
ignorer
```

That's it. ignorer will interactively guide you through the rest.

See it in action below.

![A GIF demonstrating the usage of ignorer.](media/demonstration.gif)]

# Acknowledgements

ignorer's functionality is largely based on JetBrains' [.ignore plugin](https://github.com/JetBrains/idea-gitignore)
for their IDEs.

## License

ignorer is licensed under the [MIT License](LICENSE.md).
