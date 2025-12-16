Software Design & Architecture Project Workspace

Structure:
- docs/: written materials and diagrams
- src/: source code (original baseline and redesigned)
- screenshots/: images of the app running


## Automated screenshots (macOS)

We added a small automation to capture the Tkinter app window during a scripted flow.

Prerequisites:
- Python 3.9+
- Install Pillow for ImageGrab on macOS:

```bash
pip install Pillow
```

Usage:
- Run the capture script, which launches the redesigned app, performs key actions, and saves images into `screenshots/` (captures only the app content area):

```bash
python scripts/capture_screenshots.py
```

Options:

```bash
python scripts/capture_screenshots.py --out-dir ./screenshots --delay-ms 300 --steps initial,create,park
```

- `--out-dir`: where to save images
- `--delay-ms`: delay after each action to allow UI to render
- `--steps`: comma-separated subset of steps [initial, create, park, park_ev, leave]

Automation notes:
- Dialogs are suppressed during automation via `APP_SUPPRESS_DIALOGS=1`.

Outputs:
- `screenshots/01_initial.png`
- `screenshots/02_after_create_lot.png`
- `screenshots/03_after_park.png`
- `screenshots/04_after_park_ev.png`
- `screenshots/05_after_leave.png`

How to use this workspace:
1) Place the baseline Parking Lot Manager code in src/original/
2) Run and explore the baseline; capture screenshots in screenshots/
3) Produce original UML in docs/uml/
4) Redesign code into src/redesign/ with improvements
5) Produce redesigned UML in docs/uml/
6) Write justification and DDD/microservices docs in docs/
7) Package for submission per guidelines

Notes:
- On macOS, you may need to grant “Screen Recording” permission to your terminal (System Settings → Privacy & Security → Screen Recording) for ImageGrab to work.
- If ImageGrab is unavailable or permission is denied, the script will print a helpful message.
# software_design_architecture_project
