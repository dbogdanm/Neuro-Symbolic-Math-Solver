/* ============================================================================
   Math-OS · client
   BYOK settings (browser-only), SSE streaming, pipeline visualization.
   ========================================================================== */
(() => {
  "use strict";

  // ----------------------------------------------------------------- state
  const LS_KEY = "mathos.settings";
  const DEFAULTS = {
    provider: "ollama",
    mode: "ns",
    openrouter: { apiKey: "", model: "deepseek/deepseek-r1" },
    ollama: { baseUrl: "", model: "deepseek-r1:8b" },
    gemini: { apiKey: "", model: "gemini-2.5-flash" },
    openai: { apiKey: "", model: "gpt-4o-mini" },
    anthropic: { apiKey: "", model: "claude-3-5-sonnet-20241022" },
  };

  let settings = loadSettings();
  let busy = false;
  let modelsLoaded = false;

  function loadSettings() {
    try {
      const raw = JSON.parse(localStorage.getItem(LS_KEY) || "{}");
      return {
        ...DEFAULTS, ...raw,
        openrouter: { ...DEFAULTS.openrouter, ...(raw.openrouter || {}) },
        ollama: { ...DEFAULTS.ollama, ...(raw.ollama || {}) },
        gemini: { ...DEFAULTS.gemini, ...(raw.gemini || {}) },
        openai: { ...DEFAULTS.openai, ...(raw.openai || {}) },
        anthropic: { ...DEFAULTS.anthropic, ...(raw.anthropic || {}) },
      };
    } catch { return structuredClone(DEFAULTS); }
  }
  function persist() { localStorage.setItem(LS_KEY, JSON.stringify(settings)); }

  // ----------------------------------------------------------------- helpers
  const $ = (id) => document.getElementById(id);
  const chat = () => $("chat-stream");
  const escapeHtml = (s) => s.replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  function typeset(el) {
    if (window.MathJax && MathJax.typesetPromise) {
      MathJax.typesetPromise([el]).catch(() => {});
    }
  }
  function scrollDown() { const c = chat(); c.scrollTop = c.scrollHeight; }

  function toast(msg, kind = "ok") {
    const wrap = $("toast-wrap");
    const t = document.createElement("div");
    t.className = `toast ${kind}`;
    const icon = kind === "err" ? "fa-triangle-exclamation" : "fa-circle-check";
    t.innerHTML = `<i class="fa-solid ${icon}"></i> ${escapeHtml(msg)}`;
    wrap.appendChild(t);
    setTimeout(() => { t.style.opacity = "0"; t.style.transform = "translateY(10px)";
      t.style.transition = "all .3s"; setTimeout(() => t.remove(), 320); }, 3200);
  }

  // ----------------------------------------------------------------- request body
  function llmBody() {
    if (settings.provider === "openrouter") {
      return { provider: "openrouter", model: settings.openrouter.model.trim(),
               api_key: settings.openrouter.apiKey.trim() };
    }
    if (settings.provider === "gemini") {
      return { provider: "gemini", model: settings.gemini.model.trim(),
               api_key: settings.gemini.apiKey.trim() };
    }
    if (settings.provider === "openai") {
      return { provider: "openai", model: settings.openai.model.trim(),
               api_key: settings.openai.apiKey.trim() };
    }
    if (settings.provider === "anthropic") {
      return { provider: "anthropic", model: settings.anthropic.model.trim(),
               api_key: settings.anthropic.apiKey.trim() };
    }
    return { provider: "ollama", model: settings.ollama.model.trim(),
             base_url: settings.ollama.baseUrl.trim() };
  }
  function currentModelLabel() {
    if (settings.provider === "openrouter") return settings.openrouter.model;
    if (settings.provider === "gemini") return settings.gemini.model;
    if (settings.provider === "openai") return settings.openai.model;
    if (settings.provider === "anthropic") return settings.anthropic.model;
    return settings.ollama.model;
  }

  // ----------------------------------------------------------------- chrome UI
  function refreshProviderPill() {
    const pill = $("provider-pill");
    const isOR = settings.provider === "openrouter";
    const isGemini = settings.provider === "gemini";
    const noKey = (isOR && !settings.openrouter.apiKey.trim()) || (isGemini && !settings.gemini.apiKey.trim());
    pill.classList.toggle("is-openrouter", isOR || isGemini);
    pill.classList.toggle("is-nokey", noKey);
    let name = "Ollama";
    if (isOR) name = "OpenRouter";
    if (isGemini) name = "Gemini";
    $("provider-name").textContent = name;
    $("provider-model").textContent = noKey ? "add your key →" : currentModelLabel();
  }

  function refreshModeUI() {
    document.querySelectorAll("[data-mode]").forEach((el) =>
      el.classList.toggle("active", el.dataset.mode === settings.mode));
    positionSegGlow();
  }
  function positionSegGlow() {
    const active = document.querySelector(`.seg-btn[data-mode="${settings.mode}"]`);
    const glow = $("seg-glow");
    if (active && glow) { glow.style.left = active.offsetLeft + "px";
      glow.style.width = active.offsetWidth + "px"; }
  }

  // ----------------------------------------------------------------- LiveAnswer
  // Renders one assistant turn: pipeline logs, foldable reasoning/prompt
  // blocks, streamed markdown body, and a final meta line.
  class LiveAnswer {
    constructor(container) {
      container.innerHTML = "";
      this.container = container;
      this.pipeline = null;
      this.bodyEl = document.createElement("div");
      this.bodyEl.className = "answer-card";
      container.appendChild(this.bodyEl);
      this.buffer = "";
      this.thinkFold = null;
      this.start = performance.now();
    }
    ensurePipeline() {
      if (!this.pipeline) {
        this.pipeline = document.createElement("div");
        this.pipeline.className = "pipeline";
        this.container.insertBefore(this.pipeline, this.bodyEl);
      }
      return this.pipeline;
    }
    addLog(text) {
      const row = document.createElement("div");
      row.className = "pipeline-row";
      row.innerHTML = `<i class="fa-solid fa-angle-right ico"></i><span>${escapeHtml(text)}</span>`;
      this.ensurePipeline().appendChild(row);
      scrollDown();
    }
    addFold(title, content, kind = "think", icon = "fa-brain") {
      const fold = document.createElement("div");
      fold.className = `fold ${kind === "prompt" ? "is-prompt" : ""}`;
      fold.innerHTML =
        `<div class="fold-head"><i class="fa-solid ${icon}"></i><span>${escapeHtml(title)}</span>` +
        `<i class="fa-solid fa-chevron-down chev"></i></div>` +
        `<div class="fold-body"></div>`;
      fold.querySelector(".fold-body").textContent = content;
      fold.querySelector(".fold-head").addEventListener("click", () => fold.classList.toggle("open"));
      this.container.insertBefore(fold, this.bodyEl);
      scrollDown();
      return fold;
    }
    // streaming tokens (with inline <think> parsing)
    pushToken(token) {
      this.buffer += token;
      let main = "", think = "", mode = "main", s = this.buffer;
      while (s.length) {
        if (mode === "main") {
          const i = s.indexOf("<think>");
          if (i === -1) { main += s; break; }
          main += s.slice(0, i); s = s.slice(i + 7); mode = "think";
        } else {
          const i = s.indexOf("</think>");
          if (i === -1) { think += s; break; }
          think += s.slice(0, i); s = s.slice(i + 8); mode = "main";
        }
      }
      if (think.trim()) {
        if (!this.thinkFold) this.thinkFold = this.addFold("Reasoning", "", "think", "fa-brain");
        this.thinkFold.classList.add("open");
        this.thinkFold.querySelector(".fold-body").textContent = think;
      }
      if (main.trim()) this.bodyEl.innerHTML = marked.parse(main);
      scrollDown();
    }
    setMarkdown(md) { this.bodyEl.innerHTML = marked.parse(md); }
    finalize(label) {
      if (this.thinkFold && this.bodyEl.textContent.trim()) this.thinkFold.classList.remove("open");
      const secs = ((performance.now() - this.start) / 1000).toFixed(2);
      const meta = document.createElement("div");
      meta.className = "meta-time";
      meta.innerHTML = `<i class="fa-regular fa-clock"></i> ${escapeHtml(label)} · ${secs}s`;
      const copy = document.createElement("button");
      copy.className = "copy-btn";
      copy.innerHTML = `<i class="fa-regular fa-copy"></i> copy`;
      copy.addEventListener("click", () => {
        navigator.clipboard.writeText(this.bodyEl.textContent.trim());
        copy.innerHTML = `<i class="fa-solid fa-check"></i> copied`;
        setTimeout(() => copy.innerHTML = `<i class="fa-regular fa-copy"></i> copy`, 1500);
      });
      meta.appendChild(copy);
      this.container.appendChild(meta);
      typeset(this.container);
      scrollDown();
    }
    error(msg) {
      this.bodyEl.innerHTML =
        `<p style="color:var(--danger)"><i class="fa-solid fa-triangle-exclamation"></i> ${escapeHtml(msg)}</p>`;
      scrollDown();
    }
  }

  // ----------------------------------------------------------------- SSE reader
  async function readSSE(response, onData) {
    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let buf = "";
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      const lines = buf.split("\n");
      buf = lines.pop(); // keep last partial line
      for (const line of lines) {
        if (!line.startsWith("data:")) continue;
        const payload = line.slice(5).trim();
        if (!payload) continue;
        try { onData(JSON.parse(payload)); } catch { /* partial */ }
      }
    }
  }

  // ----------------------------------------------------------------- messages
  function appendMessage(role, innerHtml) {
    const msg = document.createElement("div");
    msg.className = `msg ${role}`;
    const icon = role === "user" ? "fa-user" : "fa-wand-magic-sparkles";
    msg.innerHTML =
      `<div class="msg-avatar"><i class="fa-solid ${icon}"></i></div>` +
      `<div class="msg-body">${innerHtml}</div>`;
    chat().appendChild(msg);
    scrollDown();
    return msg.querySelector(".msg-body");
  }
  function hideHero() { const h = $("hero"); if (h) h.remove(); }

  // ----------------------------------------------------------------- send
  async function send() {
    if (busy) return;
    const ta = $("prompt-input");
    const prompt = ta.value.trim();
    if (!prompt) return;

    if (settings.provider === "openrouter" && !settings.openrouter.apiKey.trim()) {
      toast("Add your OpenRouter key first — it stays in your browser.", "err");
      openSettings();
      return;
    }
    if (settings.provider === "gemini" && !settings.gemini.apiKey.trim()) {
      toast("Add your Gemini API key first — it stays in your browser.", "err");
      openSettings();
      return;
    }

    busy = true; $("send-btn").disabled = true;
    ta.value = ""; ta.style.height = "auto";
    hideHero();

    appendMessage("user", `<p>${marked.parseInline(prompt)}</p>`);
    typeset(chat().lastElementChild);

    const modeLabel = { ns: "Neuro-Symbolic", web_rag: "Web Search", generate: "Direct" }[settings.mode];
    const container = appendMessage("bot",
      `<div class="typing"><span class="spin"></span> Routing through ${escapeHtml(modeLabel)} · ${escapeHtml(currentModelLabel())}…</div>`);

    try {
      if (settings.mode === "ns") await runNeuroSymbolic(prompt, container);
      else if (settings.mode === "web_rag") await runStreaming("/api/web_rag", prompt, container, "Web-RAG");
      else await runStreaming("/api/generate", prompt, container, "Generation");
    } catch (e) {
      new LiveAnswer(container).error(e.message || String(e));
    } finally {
      busy = false; $("send-btn").disabled = false;
    }
  }

  async function runStreaming(url, prompt, container, label) {
    const resp = await fetch(url, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, ...llmBody() }),
    });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const ans = new LiveAnswer(container);
    let errored = false;
    await readSSE(resp, (d) => {
      if (d.step) {
        const s = d.step;
        if (s.startsWith("PROMPT: ")) ans.addFold("Search context", s.slice(8), "prompt", "fa-terminal");
        else ans.addLog(s.replace(/^LOG: /, ""));
      } else if (d.text) {
        ans.pushToken(d.text);
      } else if (d.error) {
        errored = true; ans.error(d.error);
      } else if (d.done && !errored) {
        ans.finalize(label);
      }
    });
  }

  async function runNeuroSymbolic(prompt, container) {
    const resp = await fetch("/api/neuro_symbolic", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, ...llmBody() }),
    });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const ans = new LiveAnswer(container);
    let errored = false;
    await readSSE(resp, (d) => {
      if (d.step) {
        const s = d.step;
        if (s.startsWith("THINK: ")) ans.addFold("Model reasoning", s.slice(7), "think", "fa-brain");
        else if (s.startsWith("PROMPT: ")) ans.addFold("Injected context", s.slice(8), "prompt", "fa-terminal");
        else ans.addLog(s.replace(/^LOG: /, "").trim());
      } else if (d.final_answer !== undefined) {
        ans.setMarkdown(d.final_answer);
        ans.finalize("Pipeline");
      } else if (d.error) {
        errored = true; ans.error(d.error);
      }
    });
  }

  // ----------------------------------------------------------------- settings modal
  function openSettings() {
    syncSettingsForm();
    if (!modelsLoaded) loadOpenRouterModels();
    $("settings-modal").classList.add("open");
  }
  function closeSettings() { $("settings-modal").classList.remove("open"); }

  function selectProvider(p) {
    document.querySelectorAll(".pt-btn").forEach((b) =>
      b.classList.toggle("active", b.dataset.provider === p));
    $("fields-openrouter").classList.toggle("show", p === "openrouter");
    $("fields-gemini").classList.toggle("show", p === "gemini");
    $("fields-openai").classList.toggle("show", p === "openai");
    $("fields-anthropic").classList.toggle("show", p === "anthropic");
    $("fields-ollama").classList.toggle("show", p === "ollama");
    settings._draftProvider = p;
  }

  function syncSettingsForm() {
    selectProvider(settings.provider);
    $("or-key").value = settings.openrouter.apiKey;
    $("or-model").value = settings.openrouter.model;
    $("ge-key").value = settings.gemini.apiKey;
    $("ge-model").value = settings.gemini.model;
    $("oa-key").value = settings.openai.apiKey;
    $("oa-model").value = settings.openai.model;
    $("an-key").value = settings.anthropic.apiKey;
    $("an-model").value = settings.anthropic.model;
    $("ol-base").value = settings.ollama.baseUrl;
    $("ol-model").value = settings.ollama.model;
  }

  function saveSettings() {
    const p = settings._draftProvider || settings.provider;
    settings.provider = p;
    settings.openrouter.apiKey = $("or-key").value.trim();
    settings.openrouter.model = $("or-model").value.trim() || DEFAULTS.openrouter.model;
    settings.gemini.apiKey = $("ge-key").value.trim();
    settings.gemini.model = $("ge-model").value.trim() || DEFAULTS.gemini.model;
    settings.openai.apiKey = $("oa-key").value.trim();
    settings.openai.model = $("oa-model").value.trim() || DEFAULTS.openai.model;
    settings.anthropic.apiKey = $("an-key").value.trim();
    settings.anthropic.model = $("an-model").value.trim() || DEFAULTS.anthropic.model;
    settings.ollama.baseUrl = $("ol-base").value.trim();
    settings.ollama.model = $("ol-model").value.trim() || DEFAULTS.ollama.model;
    delete settings._draftProvider;
    persist();
    refreshProviderPill();
    closeSettings();
    toast("Settings saved.", "ok");
  }

  function clearKey() {
    if (settings._draftProvider === "openrouter" || settings.provider === "openrouter") {
      $("or-key").value = "";
      settings.openrouter.apiKey = "";
    } else if (settings._draftProvider === "gemini" || settings.provider === "gemini") {
      $("ge-key").value = "";
      settings.gemini.apiKey = "";
    } else if (settings._draftProvider === "openai" || settings.provider === "openai") {
      $("oa-key").value = "";
      settings.openai.apiKey = "";
    } else if (settings._draftProvider === "anthropic" || settings.provider === "anthropic") {
      $("an-key").value = "";
      settings.anthropic.apiKey = "";
    }
    persist();
    refreshProviderPill();
    toast("API key cleared from this browser.", "ok");
  }

  function toggleKeyVisibility(inputId = "or-key", eyeId = "key-eye") {
    const inp = $(inputId); const eye = $(eyeId);
    if (!inp || !eye) return;
    const show = inp.type === "password";
    inp.type = show ? "text" : "password";
    eye.className = show ? "fa-solid fa-eye-slash" : "fa-solid fa-eye";
  }

  async function loadOpenRouterModels() {
    try {
      const resp = await fetch("/api/openrouter/models");
      const data = await resp.json();
      const dl = $("or-models");
      if (!data.models || !data.models.length) return;
      modelsLoaded = true;
      dl.innerHTML = "";
      data.models.slice(0, 120).forEach((m) => {
        const opt = document.createElement("option");
        opt.value = m.id;
        opt.label = (m.free ? "★ free · " : "") + (m.name || m.id);
        dl.appendChild(opt);
      });
      const free = data.models.filter((m) => m.free).length;
      $("models-hint").innerHTML =
        `${data.models.length} models available (${free} free). Start typing to filter.`;
    } catch { /* keep built-in suggestions */ }
  }

  // ----------------------------------------------------------------- misc UI
  function setMode(m) { settings.mode = m; persist(); refreshModeUI(); }
  function clearChat() {
    chat().innerHTML = `
      <div class="hero" id="hero">
        <div class="hero-glyph"><i class="fa-solid fa-infinity"></i></div>
        <h1 class="hero-title">Solve anything,<br><em>symbolically.</em></h1>
        <p class="hero-sub">A hybrid engine that hands rigid arithmetic to a deterministic SymPy core
        and lets the model reason — zero calculation hallucinations.</p>
        <div class="chips" id="example-chips">
          <button class="chip" onclick="MathOS.useExample(this)">Find the smallest positive perfect cube that is a sum of three consecutive integers.</button>
          <button class="chip" onclick="MathOS.useExample(this)">How many ordered pairs of integers $(x,y)$ in $[-100,100]$ satisfy $12x^2 - xy - 6y^2 = 0$?</button>
          <button class="chip" onclick="MathOS.useExample(this)">Solve $\\sqrt{11 - 2x} = x - 4$.</button>
          <button class="chip" onclick="MathOS.useExample(this)">Sum of all positive integers $n$ such that $n+2$ divides $3(n+3)(n^2+9)$.</button>
        </div>
      </div>`;
    typeset(chat());
  }
  function useExample(el) {
    const ta = $("prompt-input");
    ta.value = el.textContent.trim();
    ta.focus(); autoresize(ta);
  }
  function toggleSidebar() { $("sidebar").classList.toggle("open"); }

  function autoresize(ta) {
    ta.style.height = "auto";
    ta.style.height = Math.min(ta.scrollHeight, 200) + "px";
  }

  // ----------------------------------------------------------------- init
  function init() {
    const ta = $("prompt-input");
    ta.addEventListener("input", () => autoresize(ta));
    ta.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); }
    });
    window.addEventListener("resize", positionSegGlow);
    $("settings-modal").addEventListener("click", (e) => {
      if (e.target === $("settings-modal")) closeSettings();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeSettings();
    });
    refreshProviderPill();
    refreshModeUI();
    // re-place glow after fonts settle
    setTimeout(positionSegGlow, 250);
  }

  // expose
  window.MathOS = {
    send, setMode, clearChat, useExample, toggleSidebar,
    openSettings, closeSettings, selectProvider, saveSettings,
    clearKey, toggleKeyVisibility,
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();