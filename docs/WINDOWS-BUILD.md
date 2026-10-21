# Windows launcher and single-file build

Run `Start-Windows.bat` with Python 3.10+ installed to start from source. It opens the browser and stores progress in `%LOCALAPPDATA%\THORNS\thorns-saves.sqlite3`. Keep the console open while playing. On first launch, an existing database beside the source/EXE is copied only if no destination exists. Existing destination saves are never replaced.

To build a single executable on Windows, install Python **3.12** with the Python launcher, then run `Build-Windows.bat`. It creates a dedicated build environment, installs pinned PyInstaller 6.11.1, runs the tests, and bundles the launcher and static assets into `dist\THORNS.exe`. An internet connection is required to install the build dependency. A failed test stops the build. The console stays visible so the host can stop the server with Ctrl+C.

Packaging reference: https://pyinstaller.org/en/v6.11.1/usage.html

The batch file and native executable have **not been run on Windows** in this environment. No EXE is included. Validate the built EXE by creating an open-world room, moving, closing/reopening, resuming saved progress, checking both maps, and joining from a second computer. LAN users connect to the host's LAN address on port 8765. Internet play still requires your chosen hosting/private VPN setup; an EXE does not provide a relay or bypass NAT.

To use another port: `THORNS.exe --port 8766`. To avoid automatic browser opening: `THORNS.exe --no-browser`. Saves belong to the host; browser resume credentials belong to each player's browser. Server console errors identify occupied ports without launching a browser toward another running service.
