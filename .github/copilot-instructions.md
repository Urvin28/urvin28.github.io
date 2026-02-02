<!-- Repository-specific Copilot / AI agent guidance -->
# Copilot instructions — Portfolio (static site)

Purpose
- Small, static portfolio: a landing page plus a projects index. No build system, package manager, or CI present.

Run & preview
- From repo root run: `python -m http.server 8000` and open http://localhost:8000

High-level structure (what to read first)
- `index.html`: landing copy and featured project.
- `projects.html`: project cards; many entries reference local ML demo folders under `projects/`.
- `styles.css`: global styling; uses `:root` CSS variables, `.container` layout, and a `.cards` grid.

Conventions & patterns to follow
- Layout: pages use a `.container` wrapper and semantic sections like `.hero`, `.intro`, and `.cards`.
- Project entries: use `<article class="card">` with a `.card-left` icon column and content column. Copy this example when adding projects:

```html
<article class="card">
  <div class="card-left">🧩</div>
  <div>
    <h4>Project Title</h4>
    <p>Short description and tech stack.</p>
    <p><a href="projects/project-folder/index.html">Demo / details</a></p>
  </div>
</article>
```

- Styling: prefer class-based changes in `styles.css` over inline styles. Preserve header/footer, `.container` wrappers, and `article.card` structure unless redesign is requested.

Project-specific notes
- `projects/ml/` contains ML demos (CSV data, `*.py` scripts, and `*.joblib` models). Some `projects.html` entries use absolute `file:///` links pointing outside this repo — do not assume those files exist.
- If asked to bundle external ML demos: convert `file:///` links to relative paths, add the demo folder under `projects/` (or `projects/ml/`), include a minimal `index.html` and `README.md`, and list the change in the commit message. Confirm with the user before copying files from their OneDrive.

Developer workflow & edits
- No tests or build tooling. Keep edits minimal and focused; use present-tense commit messages.
- Preview with the simple HTTP server and verify layout in browser DevTools.

When to change repository structure
- Avoid adding a build system or npm unless explicitly requested — if you add tooling, update `README.md` with exact install/run commands.

Files to read before editing
- [index.html](index.html)
- [projects.html](projects.html)
- [styles.css](styles.css)
- [README.md](README.md)

If you want a checklist for adding projects or a proposal to introduce tooling, tell me which part to expand and I will update this file.
<!-- Repository-specific Copilot / AI agent guidance -->
# Copilot instructions — Portfolio (static site)

This repository is a small, static portfolio site (HTML + CSS) with optional references to local ML scripts. Keep guidance concise and focused on what's discoverable here.

- Purpose: single-page landing (`index.html`) plus `projects.html` and a central stylesheet `styles.css`. No build system or package manager is present.
- How this repo runs: open `index.html` in a browser, or serve the folder with a simple static server, e.g. `python -m http.server 8000` from the repository root.

Key patterns and conventions
- Layout classes: pages use a `.container` wrapper and semantic sections such as `.hero`, `.intro`, and `.cards`.
- Project entries: `projects.html` uses `<article class="card">` blocks (left icon + content). When adding projects, follow that structure to preserve styling.
- Styling: all site styles live in `styles.css`. Prefer class-based styling (add classes rather than inline styles) to keep consistency.

<!-- Repository-specific Copilot / AI agent guidance -->
# Copilot instructions — Portfolio (static site)

This repository is a minimal static portfolio: `index.html`, `projects.html`, and `styles.css`. There is no build system, package manager, or test suite.

What this is
- Single-page landing (`index.html`) plus a projects index (`projects.html`).
- Styling and responsive rules live in `styles.css` (CSS variables in `:root`, `.container` layout, `.cards` grid).

How to run locally
- From the repository root run:

  python -m http.server 8000

  Then open http://localhost:8000 in a browser.

Big-picture conventions (read these before editing)
- Structure: pages use a `.container` wrapper and semantic sections: `.hero`, `.intro`, `.cards`.
- Project entries: `projects.html` uses `<article class="card">` with a `.card-left` for an icon and a content column. Keep that structure to preserve layout and accessibility.
- Styling: prefer adding classes and updating `styles.css` rather than inline styles. CSS variables and media queries are used for theming and responsiveness.

Integration & external links
- Google Fonts (`Poppins`) is loaded in the page headers — no local fonts.
- Several project links point to local absolute `file:///C:/Users/.../ML Practice/...` paths (see `projects.html` — e.g., the Exam Score script). These files are outside this repo. Do not assume they exist.

Rules for handling external/local ML scripts
- If you are asked to bundle external ML scripts into this repo: convert `file:///` links to relative paths, add the files under a new `ml/` or `projects/` folder, and add an index or README inside that folder. In your commit message note the conversion (e.g., "Convert ML script links to relative paths and add ML index"). Ask the user before copying files from their OneDrive.

Developer workflow notes
- There is no npm/CI by default. If you add tooling (build, lint, test), update `README.md` with exact commands and ask before adding to the repo.
- Preview changes with the local HTTP server and verify layout in browser DevTools.

Precise editing rules for AI agents
- Preserve header/footer markup, `.container` wrappers, and `article.card` blocks unless the user asks for redesign.
- Keep changes minimal and focused; use present-tense commit messages.
- When converting `file:///` links to relative paths, add a short note in `README.md` explaining the change.

Quick examples (copy into `projects.html` to add a project):

```html
<article class="card">
  <div class="card-left">🧩</div>
  <div>
    <h4>Project Title</h4>
    <p>Short description and tech stack.</p>
    <p><a href="projects/project-folder/index.html">Demo / details</a></p>
  </div>
</article>
```

Files you should always read before making changes
- [index.html](index.html) — landing copy, featured card
- [projects.html](projects.html) — project cards and the local `file:///` links
- [styles.css](styles.css) — site styles, colors, responsive rules
- [README.md](README.md) — preview and deploy notes

If you need more detail (e.g., a checklist for adding projects, or a proposal to introduce a build step), tell me which part to expand.
