# Git, GitHub, VS Code, And AI Workflow

This course uses Git, GitHub, VS Code, Markdown, Arduino sketches, Python code,
and AI coding agents as part of the laboratory workflow. The goal is not to
become a software engineer. The goal is to avoid losing work, keep your
instrument code organized, and make a clear record of what you built and tested.

## What Each Tool Is For

| Tool | What You Use It For In This Course |
| --- | --- |
| Git | Make checkpoints of your code and notes on your computer. |
| GitHub | Store a copy of your project online and submit a link to your work. |
| VS Code | Edit Arduino sketches, Python programs, and Markdown notes in one workspace. |
| Markdown | Write readable documentation in `README.md` files. |
| AI agent | Help draft or revise code, then explain, test, and improve it yourself. |

## Recommended Project Structure

By the end of Lab 3, organize your work into one clear project folder:

```text
phys39-tec-control/
  README.md
  arduino/
    thermistor_serial/
    tec_manual_control/
    tec_python_serial_control/
  python/
    display_strip_chart/
    manual_control_gui/
  docs/
    wiring_notes/
    screenshots/
  data/
    example_runs/
```

You may use a different structure if it is clear. The important point is that a
reader should be able to find your Arduino code, Python code, notes, images, and
data without guessing.

## VS Code Basics

Open your project folder, not just a single file:

1. Open VS Code.
2. Choose **File > Open Folder...**.
3. Select your project folder, such as `phys39-tec-control`.
4. Use the Explorer panel on the left to inspect folders and files.
5. Use **Terminal > New Terminal** to open a terminal inside VS Code.

Use VS Code to:

- edit `.ino` Arduino sketches,
- edit `.py` Python programs,
- edit and preview `README.md`,
- inspect your folder structure,
- run Python commands in the integrated terminal,
- work with an AI coding assistant while keeping your files visible.

To preview Markdown, open the `.md` file and choose **Open Preview to the Side**,
or press **Command-K**, then **V** on a Mac.

## The Four-Command Git Checkpoint

Use this workflow whenever you reach a meaningful checkpoint.

```bash
git status
git add README.md arduino python docs
git commit -m "Describe what changed"
git push
```

What the commands mean:

| Command | Meaning |
| --- | --- |
| `git status` | Show what changed. Run this before every commit. |
| `git add` | Choose which files go into the next checkpoint. |
| `git commit -m "..."` | Make the checkpoint on your computer. |
| `git push` | Upload the checkpoint to GitHub. |

Use commit messages that say what changed, for example:

```bash
git commit -m "Add thermistor serial sketch"
git commit -m "Add Python display strip chart"
git commit -m "Document H-bridge wiring"
git commit -m "Organize Lab 3 TEC control project"
```

## What Not To Commit

Do not blindly commit everything. Look at `git status` first.

Usually commit:

- Arduino sketches you wrote or modified,
- Python scripts and GUIs,
- `README.md`,
- wiring notes,
- small example data files,
- screenshots or diagrams needed to explain your project.

Usually do not commit:

- temporary files,
- duplicate AI drafts you are not using,
- very large raw data files unless instructed,
- accidental downloads,
- files whose purpose you cannot explain.

## What Your README Should Explain

Your `README.md` is the front door to your project. It should explain:

- what the project does,
- what hardware is connected to which Arduino pins,
- which Arduino sketch goes with which Python program,
- how to upload the Arduino sketch,
- how to run the Python program,
- one example serial line and what each field means,
- what Git commits you made to organize and preserve your work,
- what you tested on real hardware,
- what you still do not fully understand.

## AI Use Note

AI can help you write code, but you are responsible for the instrument. Include
a short AI use note in your `README.md`:

- Which parts of the code did AI help generate?
- Which parts did you modify yourself?
- Which parts did you test on real hardware?
- Which parts can you explain without looking at the AI transcript?

Good AI use sounds like:

```text
AI helped me draft the serial parser and the first pyqtgraph strip chart. I
modified the axis limits, added the PWM display, and tested the program with the
Arduino on /dev/cu.usbmodem.... I can explain how one serial line is parsed and
how the plot buffers are updated.
```

## Practice Exercise

Before using Git on your real lab code, practice with a tiny project:

```text
phys39-git-practice/
  README.md
  arduino/
  python/
  docs/
```

Then:

1. Write two sentences in `README.md`.
2. Run `git status`.
3. Commit the README.
4. Add one small Arduino sketch.
5. Run `git status` again.
6. Commit the sketch.
7. Push to GitHub.
8. Open GitHub in a browser and confirm that the files are there.

## Troubleshooting

If `git status` shows many unexpected files, stop and ask before committing.

If `git push` asks for GitHub login, follow the GitHub authentication prompt or
ask for help.

If VS Code asks whether to save a file you did not mean to edit, choose
**Cancel** first and inspect the tab. A dot on the tab means there are unsaved
changes.

If a Python program says the Arduino port does not exist, check the port name:

```bash
ls /dev/cu.usb*
```

If the port is busy, close Arduino Serial Monitor, Arduino Serial Plotter,
MATLAB, or another Python GUI that may already be using the port.
