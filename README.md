# Ulauncher Sway+

An evolution of https://github.com/rdnetto/ulauncher-sway

This repo contains a [Ulauncher](https://ulauncher.io) extension for managing [Sway](https://swaywm.org).

## Sway + Windows

<p align="center">
  <img src="https://github.com/user-attachments/assets/bc16fcff-c8be-405a-ac76-e221b328a39a" alt="Sway Demo" width="720" />
</p>

## Sway + Marks

<p align="center">
  <img src="https://github.com/user-attachments/assets/a2d83e83-6273-4dfa-be84-d9cce6083649" alt="Sway Marks Demo" />
</p>

## Features of this fork

 - [x] Search and focus to window
 - [x] Sort by Most used/ Recently used / No sort
 - [x] Search takes into account title name + application name
 - [x] Fixes for windows without identification

### Marks management

 - [x] Add a mark to the current windows
 - [x] Unmark the current windows
 - [x] List and focus by marked windows

### Future implementations

 - [ ] Move selected window to a workspace
 - [ ] List windows by workspace

## Development

### Prerequisites

 - [Ulauncher](https://ulauncher.io)
 - [Sway](https://swaywm.org)
 - [gtk3](https://www.gtk.org/)

### CI tools

 - [black](https://github.com/psf/black) - Python code formatter
 - [isort](https://github.com/PyCQA/isort) - Python import sorter

### CI install

```bash
make ci-install
```

### Install

Clone the repository and inside the directory run:

```bash
make setup
```

To start run
```bash
make start
```
It will kill any ulauncher instance and restart


### Test

To run the automated tests

```bash
make test
```
