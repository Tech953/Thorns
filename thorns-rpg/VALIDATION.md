# v0.4 validation — 2026-09-30

24 distinct automated tests pass under Python 3.12, including chapter routes, six-player capacity/voting, permissions, character budgets, reputation, encounter variety, persisted state, grid movement and distance, survival/evacuation, contracts, mod limits, independent duel completion, and non-overwriting save migration.

The HTTP test starts a real local server and covers six-player chapter actions plus six independent open-world players moving with survival updates. It checks all scripts, styles, and maps are served. JavaScript syntax checks pass for app.js and openworld.js.

Visual browser validation was attempted but blocked by a missing Playwright Chromium executable. No visual playtest, real LAN/internet session, Windows batch execution, native EXE build, or human balance assessment is claimed. Windows build scripts are supplied for the next stage.

Run: `python -m unittest discover -v` from this folder.
