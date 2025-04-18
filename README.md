# Ulauncher Sway+

A improved take of https://github.com/rdnetto/ulauncher-sway

This repo contains a [Ulauncher](https://ulauncher.io) extension for managing [Sway](https://swaywm.org).

![screenshot](https://github.com/rdnetto/ulauncher-sway/raw/master/images/screenshot.png)

## Features

 - [x] Search and focus to window
 - [x] Most used windows first
 - [ ] Move window to a given workspace

## Development

### Prerequisites

 - [Ulauncher](https://ulauncher.io)
 - [Sway](https://swaywm.org)
 - [gtk3](https://www.gtk.org/)

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
