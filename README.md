# Portfolio

This is a small static portfolio site (HTML + CSS). Preview locally and deploy to GitHub Pages.

Preview locally

```bash
python -m http.server 8000
# open http://localhost:8000
```

Push to GitHub (example)

```bash
git init                # if not already a git repo
git add .
git commit -m "Initial portfolio site"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo>.git
git push -u origin main
```

Enable GitHub Pages

1. Go to GitHub → Repository → Settings → Pages
2. Select branch `main` and folder `/ (root)` then Save
3. Wait a few minutes for the site to publish at `https://<username>.github.io/<repo>/`

Replace `<your-username>` and `<repo>` with your values.

Assets

- `assets/profile.jpg` — profile photo
- `assets/resume.pdf` — resume (embedded at `/resume.html`)

If you want, I can run the exact `git` commands for you (I will need the repo remote URL), or prepare a branch/commit message ready for push.
# Portfolio scaffold

This folder contains a minimal static portfolio you can customize.

- `index.html` — homepage (edit your name, about, and contact)
- `projects.html` — project list and links
- `styles.css` — simple responsive styles

## Local preview
From the `portfolio` folder run a simple HTTP server and open `index.html` in your browser:

```bash
# Python 3
python -m http.server 8000
# then visit http://localhost:8000
```

## Notes about ML scripts referenced in `projects.html`
- Several project cards reference scripts that live on the developer's local OneDrive via `file:///` URLs. Those external files are not included in this repository.
- To avoid broken external links the repo includes placeholder pages under `projects/ml/` (one per referenced project). To add the original scripts into the repo:
	1. Copy the script(s) and any model/data artifacts into a new folder, e.g. `projects/ml/exam_score/`.
	2. Add a short `index.html` or `README.md` explaining how to run the demo.
	3. Update `projects.html` if you want the public link text changed.

If you want me to import files from your OneDrive into this repository, confirm and grant access (or upload the files here) and I'll add them and update the links.
 
Imported ML scripts
- The previously external ML scripts have been copied into `projects/ml/`:
	- `projects/ml/exam_score/exam_score.py`
	- `projects/ml/credit_card/credit.py`
	- `projects/ml/diabetes/diabetes_classification.py`
- Each folder contains a `README.md` with run notes and the shared `projects/ml/requirements.txt` lists the main Python dependencies.

## Deploy
- Easiest: push this folder to a GitHub repo and enable GitHub Pages (use `main` branch or a `gh-pages` branch).
- Alternative: Netlify or Vercel (drag & drop or connect repo).

## Edit tips
- Replace "Your Name" and contact links in `index.html` and `projects.html`.
- Add screenshots in a new `images/` folder and reference them from the HTML.
