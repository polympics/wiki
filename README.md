# Polympics Site Wiki

This repository contains both the Polympics Wiki, as markdown, and the tool for rendering it to HTML.

## Contributing

TODO: Document making content contributions (markdown, Git/GitHub).

## Setup

This project requires Python3.9+ (Python 4 is not acceptable). Depending on your operating system, you may be able to install it from your package manager, an external PPA (like deadsnakes), or [the official website](https://python.org/download).

This project uses `pipenv` to manage dependencies. To get started, you'll need to install `pipenv` from PyPI, eg:
```bash
$ python3 -m pip install pipenv
```

Once you have `pipenv` installed, you can create a virtual enviroment and install the project's dependencies with
```bash
$ pipenv shell
$ pipenv install
```
You can then build the HTML output with
```bash
$ pipenv run build
```

If you are contributing to the build code, you will also need to install development dependencies:
```bash
$ pipenv install -d
```
You can then lint the code with
```bash
$ pipenv run lint
```

## Configuration

TODO: Document builder configuration (config.json).

## API

TODO: Document API (index.json, HTML files).
