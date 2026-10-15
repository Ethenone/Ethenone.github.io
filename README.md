# Tianci Wang's CV

The site opens `resume.html` from `index.html`. The web CV and the maintained general résumé use the same Markdown source files:

- `contents/resume-general.en.md` — English
- `contents/resume-general.zh.md` — 中文

Edit the matching sections in both files to keep the translations aligned. Section IDs (`profile`, `research`, `publications`, `projects`, `education`) are used by the navigation and should remain unchanged. `static/js/i18n.js` switches between the two sources; the Print / PDF button uses the browser's print dialog.


