# Phys 39: Instrumentation and Thermal Physics

This is the student-facing repository for Phys 39, Fall 2026.

The rendered course website is built from the Markdown files in `course/`.
Students can read the material on the website or browse the same source files
directly in GitHub.

## Local Website Preview

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs serve
```

Then open:

```text
http://127.0.0.1:8000/
```

## Publishing

Build the public website from the approved Markdown:

```bash
mkdocs build --strict
```

The generated website is written to `docs/`. Commit both the source changes in
`course/` and the generated changes in `docs/`, then push `main`. GitHub Pages
publishes the `docs/` folder automatically.

The source files in `course/` are authoritative. Do not hand-edit generated
files in `docs/`.

