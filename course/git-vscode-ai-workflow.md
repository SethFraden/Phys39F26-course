# GitHub Desktop, GitHub, VS Code, And AI Workflow

This course uses GitHub Desktop, GitHub, VS Code, Markdown, Arduino sketches,
Python code, and AI coding agents as part of the laboratory workflow. The goal
is not to become a software engineer. The goal is to avoid losing work, keep
your instrument code organized, and make a clear record of what you built and
tested.

## What Each Tool Is For

| Tool | What You Use It For In This Course |
| --- | --- |
| GitHub Desktop | Make checkpoints of your code and notes, then sync them to GitHub. |
| GitHub | Store a copy of your project online and submit a link to your work. |
| VS Code | Edit Arduino sketches, Python programs, and Markdown notes in one workspace. |
| Markdown | Write readable documentation in `README.md` files. |
| AI agent | Help draft or revise code, then explain, test, and improve it yourself. |

## Set Up Accounts And Software

Use these official guides when setting up your computer and accounts:

- [Create a GitHub account](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github)
- [Install GitHub Desktop](https://desktop.github.com/)
- [Get started with GitHub Desktop](https://docs.github.com/en/desktop/overview/getting-started-with-github-desktop)
- [Set up GitHub Copilot in VS Code](https://code.visualstudio.com/docs/setup/copilot)
- [Get GitHub Copilot access as a student](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/enable-copilot/set-up-for-students)

When you apply for GitHub student access, do not use your Brandeis ID card as
the proof document. Students report that GitHub rejects it because it does not
show a date. A transcript or acceptance letter works better. GitHub asks you to
upload the document as a `.jpg` image.

For this course, the default AI coding assistant is GitHub Copilot in VS Code.
If you use another approved coding AI tool, the same rule applies: AI may help
you draft code, but you are responsible for testing it, organizing it,
making a checkpoint in GitHub Desktop, syncing it to GitHub, and explaining
what it does.

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

To use Copilot, open the Copilot Chat panel in VS Code, paste a course prompt,
and ask it to write into the file you currently have open. Some AI tools edit
files directly; others give code in the chat window for you to copy into the
right file. Make sure Arduino code goes in `.ino` files, Python code goes in
`.py` files, and documentation goes in `.md` files.

## GitHub Desktop Checkpoint Workflow

Use this workflow whenever you reach a meaningful checkpoint.

1. Open GitHub Desktop.
2. Select your course project repository.
3. Look at the changed files list.
4. Uncheck files that do not belong in this checkpoint.
5. Write a short summary that says what changed.
6. Click **Commit to main**.
7. Click **Push origin** or **Sync changes** to upload the checkpoint to GitHub.

Use commit messages that say what changed, for example:

- Add thermistor serial sketch
- Add Python display strip chart
- Document H-bridge wiring
- Organize Lab 3 TEC control project

## What Not To Commit

Do not blindly commit everything. Look at the changed files list in GitHub
Desktop first.

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
- what checkpoints you made to organize and preserve your work,
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

Before using GitHub Desktop on your real lab code, practice with a tiny project:

```text
phys39-desktop-practice/
  README.md
  arduino/
  python/
  docs/
```

Then:

1. Write two sentences in `README.md`.
2. Open the project in GitHub Desktop.
3. Look at the changed files list.
4. Commit the README.
5. Add one small Arduino sketch.
6. Check the changed files list again.
7. Commit the sketch.
8. Push or sync to GitHub.
9. Open GitHub in a browser and confirm that the files are there.

## Troubleshooting

If GitHub Desktop shows many unexpected changed files, stop and ask before
committing.

If GitHub Desktop asks you to sign in, follow the GitHub authentication prompt
or ask for help.

If VS Code asks whether to save a file you did not mean to edit, choose
**Cancel** first and inspect the tab. A dot on the tab means there are unsaved
changes.

If a Python program says the Arduino port does not exist, check the port name:

```bash
ls /dev/cu.usb*
```

If the port is busy, close Arduino Serial Monitor, Arduino Serial Plotter,
MATLAB, or another Python GUI that may already be using the port.
