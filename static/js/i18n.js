(function () {
  "use strict";
  const files = { en: "contents/resume-general.en.md", zh: "contents/resume-general.zh.md" };
  const labels = {
    en: { title: "Tianci Wang | CV", toggle: "中文", print: "Print / PDF", loading: "Loading CV…", error: "The CV could not be loaded. Please refresh the page.", nav: ["Profile", "Research", "Publications", "Projects", "Education"] },
    zh: { title: "王天赐 | 简历", toggle: "EN", print: "打印 / PDF", loading: "正在加载简历…", error: "简历加载失败，请刷新页面。", nav: ["简介", "科研", "论文成果", "项目", "教育"] },
  };
  const navItems = ["profile", "research", "publications", "projects", "education"];
  const content = document.getElementById("resume-content");
  const status = document.getElementById("resume-loading");
  const toggle = document.getElementById("lang-toggle");
  const print = document.getElementById("print-btn");
  let lang;
  let requestId = 0;
  try { lang = localStorage.getItem("resume-lang"); } catch (_) {}
  if (lang !== "en" && lang !== "zh") lang = (navigator.language || "").toLowerCase().startsWith("zh") ? "zh" : "en";

  async function render(nextLang) {
    const currentRequest = ++requestId;
    lang = nextLang;
    const ui = labels[lang];
    document.documentElement.lang = lang === "zh" ? "zh-CN" : "en";
    document.title = ui.title;
    toggle.textContent = ui.toggle;
    print.textContent = ui.print;
    navItems.forEach((item, index) => { document.querySelector(`[data-nav="${item}"]`).textContent = ui.nav[index]; });
    status.textContent = ui.loading;
    status.hidden = false;
    try {
      const response = await fetch(files[lang], { cache: "no-cache" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const markdown = await response.text();
      if (currentRequest !== requestId) return;
      content.innerHTML = marked.parse(markdown, { mangle: false, headerIds: false });
      status.hidden = true;
    } catch (error) {
      if (currentRequest !== requestId) return;
      console.error("CV load failed:", error);
      status.textContent = ui.error;
    }
  }
  toggle.addEventListener("click", () => {
    const nextLang = lang === "en" ? "zh" : "en";
    try { localStorage.setItem("resume-lang", nextLang); } catch (_) {}
    render(nextLang);
  });
  print.addEventListener("click", () => window.print());
  render(lang);
})();
