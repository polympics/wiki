# Polympics Site Wiki

This repository contains both the Polympics Wiki, as markdown, and the tool for rendering it to HTML.

## Contributing

### Intro to Markdown

*You can skip this section if you already know markdown. Alternatively, try this [markdown cheatsheet](https://commonmark.org/help/).*

Wiki pages are markdown (`.md`) files. Go ahead and open one to see how they look. Actually, this is README is a markdown file too! You can see the source code that made this file [here](https://raw.githubusercontent.com/polympics/wiki/main/README.md).

If you've used Discord, you're probably already familiar with parts of markdown like `*italic*` and `**bold**`. Some more features of markdown are showcased below:

```md
# Title
## Subtitle
### Sub subtitle
###### ... 6 is the smallest

* list
* of
* items

Divided
- - -
Sections
[Link](https://example.com).

> Someone famous probably said this.
```
This looks like:

> # Title
> ## Subtitle
> ### Sub subtitle
> ###### ... 6 is the smallest
>
> * list
> * of
> * items
>
> Divided
> - - -
> Sections
>
> [Link](https://example.com).
>
> > Someone famous probably said this.

There are also [online markdown editors](https://stackedit.io/app), so you can write markdown like you might in Google Docs or Microsoft Word. However, many of these provide extensions not currently supported by the Polympics Wiki. The flavour of markdown this Wiki uses [*Commonmark*](https://commonmark.org). The only difference you will probably notice is that tables are not supported.

### Adding to the Wiki

You will need a GitHub account to contribute to this Wiki. They are free, you can create one [here](https://github.com/join).

The files that make up the wiki are markdown files (see above), in the `content` folder. Unless you are writing code, you can ignore everything except that folder (and this file!).

All file names should be lowercase, using underscores (`_`) instead of spaces.

If you want to add or edit a file, find the relevant "Add file" or "Edit file" buttons on Github (the edit file button is usually just a pencil icon). GitHub will help automate the process and guide you through it. Once you've made your changes or written your file, press the "Create pull request" button. We will review it as soon as we can!

If you're a frequent contributor to the Wiki, you can also get write access. Just [contact Artemis](https://artemisdev.xyz) with your GitHub username.

### Wiki Directives

As well as markdown, you'll often see something like this at the top of files:
```
@navbar
@title Cool Page!
```
These are a feature of this wiki, called *wiki directives* (or you can call them whatever, I don't mind). A wiki directive is any line beginning with an `@`. The currently support directives are listed below:

#### @navbar

Indicates that the file should be linked to directly from the Polympics navbar. Please use this sparingly as there is limited space in the navbar. Four of five pages at most should include this.

#### @title <Page Title>

Specifies a title for the page. Currently, this is only used in the navbar. Especially for navbar pages, this should be kept to two words, or three short ones. If you don't use this directive, a reasonable default will be chosen based on the file name.

***Unless you're writing code, you don't need to read any further.***

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

Configuration goes in the same dir as this README, in a file named `config.json`. The available options are as follows:

| Field             | Default       |
|:------------------|:--------------|
| `in_dir`          | `content`     |
| `out_dir`         | `out`         |
| `index_file`      | `index.json`  |

Because all fields are optional, you need not make the file at all.

## API

The API consists of a single root endpoint which links to available files.

For this repository, the endpoint is:
```
https://raw.githubusercontent.com/polympics/wiki/build/index.json
```
This returns a JSON object, though the `Content-Type` header may be incorrect. It contains one key: `files`. This is a list of file objects, defined below:

| Field    | Type      | Description                                      |
|:---------|:----------|:-------------------------------------------------|
| `path`   | `string`  | The relative path to the page (see below).       |
| `title`  | `string`  | The title of the page.                           |
| `navbar` | `boolean` | Whether the page should be linked in the navbar. |

The `path` is relative to the root endpoint. For example, a path of `events/art.html` for this repository would mean:
```
https://raw.githubusercontent.com/polympics/wiki/build/events/art.html
```
