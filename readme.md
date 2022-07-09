NextTest
---

A simple solution to actually testing discord bots.

---

#### Motivation

Testing discord bots is rather manual and tedious. I'd like to describe my bots with code
and have them meet that criteria (I.e. Unit tests), however, no framework exists to
easily build out tests. 

Further to this, testing pull requests can be tedious and result in missed cases. Unit-testing
provides both a way to test new code, and backwards compatibility in a simple, repeatable manner.

---

#### Goals

- [ ] Run PR tests via the command line
  - `python -m nexttest -repo nextcord -pr 1` -> Would execute any known tests relating to nextcord PR 1
- [ ] Run all tests for a given repo
  - `python -m nexttest -repo nextcord` -> Would execute all nextcord associated tests
- [ ] Support for both `disnake` and `nextcord` bots
- [x] Support HTML reporting
  - Add `--html=report.html --self-contained-html` when running nexttest
- [ ] Ship tests with Pypi build. I'm lazy, and it saves git cloning for most of my use-cases.

Note, tests will be written with `pytest`. `NextTest` simply provides the means
to test discord bots within `pytest`.

---

#### Features

This will support the things I need to be able to test for personal usage,
which albeit is not exhaustive. Please open an issue or pr for support for things you want.

---

#### Note

Make sure to have `disnake` or `nextcord` installed from Git to test prs. 
You will also need the github command line tools if you wish to test prs.