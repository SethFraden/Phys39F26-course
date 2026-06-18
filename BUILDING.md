# Website Workflow

## Edit

Edit the Markdown source in `course/`. For example:

```text
course/labs/lab-01.md
```

## Preview

```bash
source .venv/bin/activate
mkdocs serve
```

Open `http://127.0.0.1:8000/`.

## Publish

```bash
mkdocs build --strict
git status
git add course docs mkdocs.yml
git commit -m "Update student course materials"
git push origin main
```

GitHub Pages publishes the generated `docs/` folder.

Do not edit files inside `docs/` by hand. They are regenerated from `course/`.
