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

Complete these steps in order when setting up your computer and accounts:

1. [Create a GitHub account](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github), if you do not already have one.
2. [Install GitHub Desktop](https://desktop.github.com/).
3. [Sign in to and get started with GitHub Desktop](https://docs.github.com/en/desktop/overview/getting-started-with-github-desktop).
4. [Install VS Code](https://code.visualstudio.com/).
5. [Set up GitHub Copilot in VS Code](https://code.visualstudio.com/docs/setup/copilot).
6. [Get GitHub Copilot access as a student](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/enable-copilot/set-up-for-students).

When you apply for GitHub student access, do not use your Brandeis ID card as
the proof document. Students report that GitHub rejects it because it does not
show a date. A transcript or acceptance letter works better. GitHub asks you to
upload the document as a `.jpg` image.

For this course, the default AI coding assistant is GitHub Copilot in VS Code.
If you use another approved coding AI tool, the same rule applies: AI may help
you draft code, but you are responsible for testing it, organizing it,
making a checkpoint in GitHub Desktop, syncing it to GitHub, and explaining
what it does.

## Receive And Clone Your Team Repository

Each team will use one private project repository for the entire course. The
instructor will provide the repository or an invitation link. Do not create a
second experimental repository unless the instructor asks you to do so.

The standard starter project is available publicly:

- [Download the Phys 39 starter project](downloads/phys39-instrumentation-starter.zip)
- [Browse the starter-project files on GitHub](https://github.com/SethFraden/Phys39F26-course/tree/main/student_project_template)

Your assigned private repository may already contain these files. If it does
not, the instructor will tell you to download and unzip the starter project,
then copy `README.md`, `.gitignore`, `requirements.txt`, and the `arduino`,
`python`, `docs`, and `data` folders into the top level of your cloned private
repository. Do not leave them inside an extra nested starter-project folder.

After both team members can open the repository on GitHub:

1. Open GitHub Desktop.
2. Choose **File > Clone Repository...**.
3. On the **GitHub.com** tab, select your assigned Phys 39 repository. If it is
   not listed, use the **URL** tab and paste the repository URL.
4. Choose a local path you can find again, such as your `Documents/GitHub`
   folder, and click **Clone**.
5. In GitHub Desktop, choose **Repository > Open in Visual Studio Code**.
6. Confirm that VS Code Explorer shows `README.md`, `.gitignore`,
   `requirements.txt`, `arduino`, `python`, `docs`, and `data` at the top
   level. If the starter files are absent, follow the instructor's directions
   for copying the downloaded files before proceeding.

Cloning makes a working copy on your laptop and connects it to the private
GitHub repository. Both partners should clone the same team repository onto
their own computers.

### Working With A Partner

At the beginning of a work session, open GitHub Desktop and click **Fetch
origin**. If **Pull origin** appears, click it before editing. This brings your
partner's committed work onto your computer.

Until the class introduces more advanced Git tools, do not have both partners
edit the same file at the same time. Agree who is editing it, make and push a
checkpoint, and then have the other partner fetch and pull before continuing.
You may work simultaneously on different files, but communicate before moving
or renaming shared folders.

## Team Project Structure

Use one repository throughout the course. By the end of Module 3, the working
part of the repository should resemble this structure:

```text
phys39-instrumentation/
  README.md
  .gitignore
  requirements.txt
  arduino/
    thermistor_serial/
      thermistor_serial.ino
    tec_manual_control/
      tec_manual_control.ino
    tec_python_control/
      tec_python_control.ino
  python/
    tec_display_strip_chart.py
    tec_control_gui.py
    models/
    analysis/
  docs/
    module_notes/
    wiring/
    figures/
  data/
```

Do not create every future experiment folder immediately. Add folders as the
project develops. For example, create `data/module_04_open_loop/` when you
collect the Module 4 data.

The important rules are:

- A reader can find code, notes, figures, and data without guessing.
- Every Arduino `.ino` file is inside a folder with exactly the same name. For
  example, `thermistor_serial.ino` belongs in `thermistor_serial/`.
- Small standalone Python programs can sit directly in `python/`. Later
  simulations and data-processing programs go in `python/models/` and
  `python/analysis/`.
- `README.md` identifies which Arduino and Python programs currently work
  together.
- `.gitignore` excludes local environments and temporary files. Do not use it
  to hide files merely because their purpose is unclear.
- `requirements.txt` records the Python packages needed to run the project.

Git records files, not empty folders. A folder will appear on GitHub only after
it contains a committed file. The starter repository therefore includes short
`README.md` files in folders that would otherwise be empty.

## Create And Move Files In VS Code

Use the Explorer panel on the left side of VS Code:

1. Select the project name at the top of Explorer.
2. Click the **New Folder** icon and enter a folder name such as `arduino`.
3. Select the destination folder, click the **New File** icon, and enter the
   complete filename, including `.ino`, `.py`, or `.md`.
4. Drag an existing file onto a folder in Explorer to move it.
5. Save the file and check that it appears in the intended folder.

When moving an Arduino sketch, move its same-named sketch folder as a unit. Open
the moved `.ino` file in Arduino IDE, compile it, and upload it again before
discarding the earlier copy. Avoid accumulating ambiguous names such as
`final.py`, `final2.py`, or `newest.py`; use names that describe the program.

## VS Code Basics

Open your project folder, not just a single file:

1. Open VS Code.
2. Choose **File > Open Folder...**.
3. Select your project folder, such as `phys39-instrumentation`.
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

- **Save** writes the current file to your laptop.
- **Commit** records a named checkpoint in the Git repository on your laptop.
- **Push** uploads your committed checkpoints to GitHub.

1. Open GitHub Desktop.
2. Select your course project repository.
3. Click **Fetch origin** and then **Pull origin** if it appears. If pulling
   introduces unexpected changes, stop and inspect them before committing.
4. Look at the changed files list.
5. Uncheck files that do not belong in this checkpoint.
6. Write a short summary that says what changed.
7. Click **Commit to main**.
8. Click **Push origin** or **Sync changes** to upload the checkpoint to GitHub.
9. Choose **Repository > View on GitHub** and confirm that the latest commit and
   intended files appear online.

Use commit messages that say what changed, for example:

- Add thermistor serial sketch
- Add Python display strip chart
- Document H-bridge wiring
- Organize Module 3 TEC control project

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
