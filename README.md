# Tianci Wang's CV

The site opens `resume.html` from `index.html`. The web CV and the maintained general résumé use the same Markdown source files:

- `contents/resume-general.en.md` — English
- `contents/resume-general.zh.md` — 中文

Edit the matching sections in both files to keep the translations aligned. Section IDs (`profile`, `research`, `publications`, `projects`, `education`) are used by the navigation and should remain unchanged. `static/js/i18n.js` switches between the two sources; the Print / PDF button uses the browser's print dialog.

For local preview, run `python -m http.server 8000` in this directory and open `http://localhost:8000/`. Opening the HTML files directly may block Markdown loading.

Local analysis and archived drafts are kept in `.local-review/`, which is ignored by Git.

