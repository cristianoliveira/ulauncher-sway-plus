# Ulauncher Sway+

A improved take of https://github.com/rdnetto/ulauncher-sway

This repo contains a [Ulauncher](https://ulauncher.io) extension for managing [Sway](https://swaywm.org).

![screenshot](https://github.com/rdnetto/ulauncher-sway/raw/master/images/screenshot.png)

## Sway Marks Feature

<div style="text-align: center;">
  <img src="https://github.com/user-attachments/assets/aa9f598f-580a-4217-b996-968e97c0c23f" alt="Sway Marks Demo" />
</div>

## Features of this fork

 - [x] Search and focus to window
 - [x] Sort by Most used/ Recently used / No sort
 - [ ] Move window to a given workspace

### Marks management

 - [x] Add a mark to the current windows
 - [x] Unmark the current windows
 - [x] List and focus by marked windows

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
