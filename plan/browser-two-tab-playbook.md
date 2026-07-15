# Browser Two-Tab Playbook (playwright-extension MCP)

> Confirmed working 2026-07-14. Two persistent, already-logged-in Chrome tabs driven by the
> `playwright-extension` MCP. **Tab 0 = ChatGPT (GPT-5.6 review lane) · Tab 1 = Google Scholar (search lane).**
> Keep both alive, never navigate-in-place, switch by **title-verified index**.

---

## 1. The fixed layout

| Page | Site | Logged-in as | Confirmed | Role |
|------|------|--------------|-----------|------|
| **Tab 0** | `https://chatgpt.com/` | xufeng ling's Workspace (Business) | **GPT-5.6 Thinking, effort High** | External-brain review / consult lane |
| **Tab 1** | `https://scholar.google.com/` | profile `Uq6ldZQAAAAJ` (no CAPTCHA) | search→scrape→PDF verified | Paper search / PDF fetch lane |

**Golden rule:** two persistent tabs beat one re-navigated page. Re-navigating **aborts** an in-flight
GPT-5.6 answer and loses the conversation thread + Scholar query/scroll state. Switching tabs is instant
and preserves everything. **Never close either tab.**

**Discipline:** tab indices shift when tabs open/close. **Always `list` and match the URL/title before
`select`** — never trust a hardcoded index.

---

## 2. Effortless recipes (copy-paste tool calls)

### 2.0 Always start here — find the right tab
```
browser_tabs { action: "list" }          # returns index + title + url for every tab
browser_tabs { action: "select", index: N }   # N = the one whose url matches chatgpt.com / scholar.google.com
```
If a tab is missing, open it (this becomes the new highest index):
```
browser_tabs { action: "new", url: "https://chatgpt.com/" }
browser_tabs { action: "new", url: "https://scholar.google.com/" }
```

---

### 2.1 ChatGPT lane — ask GPT-5.6 and read the reply

**Send** (composer is `role=textbox "Chat with ChatGPT"`; `submit:true` presses Enter):
```
browser_snapshot                          # get the current composer ref (e.g. f24e556)
browser_type {
  target: "<composer ref or selector #prompt-textarea>",
  text:   "<your prompt>",
  submit: true
}
```

**Read the reply** (High reasoning ≈ 15–40 s; poll until the stop-button disappears):
```
browser_wait_for { time: 15 }             # give it a head start
browser_evaluate { function: "() => {
  const t = document.querySelectorAll('[data-message-author-role=\"assistant\"]');
  const last = t[t.length - 1];
  const streaming = !!document.querySelector('button[data-testid=\"stop-button\"], button[aria-label=\"Stop streaming\"]');
  return { streaming, text: last ? last.innerText.trim() : null };
} }
```
Repeat the `browser_evaluate` (or another `browser_wait_for {time:10}`) until `streaming === false`.
Then `text` is the full answer.

> Tip: to continue the SAME thread, just `browser_type` again — do not navigate. To start a fresh
> thread, navigate the tab to `https://chatgpt.com/` (only when you deliberately want a clean context).

---

### 2.2 Google Scholar lane — search, scrape, grab PDF

**Search** (direct URL is the most reliable; `hl=en` forces English):
```
browser_navigate { url: "https://scholar.google.com/scholar?hl=en&q=YOUR+QUERY+HERE" }
```
(or type into the box: `browser_type { target: "<search box ref>", text: "...", submit: true }`)

**Scrape the whole results page in one pass** (title, authors/venue, snippet, citations, **direct PDF URL**):
```
browser_evaluate { function: "() => {
  const out = [];
  document.querySelectorAll('#gs_res_ccl_mid .gs_r.gs_or.gs_scl').forEach((root, i) => {
    const t = root.querySelector('.gs_rt a') || root.querySelector('.gs_rt');
    out.push({
      i,
      title: t ? t.textContent.replace(/^\\[[A-Z]+\\]\\s*/,'').trim() : null,
      link:  root.querySelector('.gs_rt a')?.href || null,
      meta:  root.querySelector('.gs_a')?.textContent.trim() || null,
      pdf:   root.querySelector('.gs_ggsd a')?.href || null,
      cited: Array.from(root.querySelectorAll('.gs_fl a')).find(a=>/Cited by/i.test(a.textContent))?.textContent.trim() || null,
      snippet: root.querySelector('.gs_rs')?.textContent.trim().slice(0,160) || null
    });
  });
  return { count: out.length, results: out };
} }
```

**Fetch + read the PDF** — do this in the SHELL (Bash), not the browser (arXiv is sandbox-allowlisted):
```
cd <scratchpad>
wget -q -O paper.pdf "https://arxiv.org/pdf/2411.03687"
file paper.pdf                # expect: PDF document
pdftotext paper.pdf paper.txt
grep -i "test-time" paper.txt # grep whatever you need
```
Non-allowlisted / paywalled hosts (some publisher PDFs) → either fetch through the browser tab, or run
the `wget` with `dangerouslyDisableSandbox: true`.

---

## 3. End-to-end example (research consult in ~5 calls)

1. `browser_tabs {list}` → find Scholar tab → `select`.
2. `browser_navigate {scholar?...q=world+model+test-time+adaptation}` → `browser_evaluate` scrape → pick a paper.
3. Bash: `wget` its `pdf` URL → `pdftotext` → read the abstract/method.
4. `browser_tabs {list}` → find ChatGPT tab → `select`.
5. `browser_type {..., submit:true}` "Here's the finding from <paper> … critique it / is it novel vs X?"
   → poll `browser_evaluate` for the GPT-5.6 reply.

No re-login, no reloads, no lost context — the two tabs stay warm the whole time.

---

## 4. Guardrails

- **User's real account.** Both tabs use the user's logged-in identity. Keep Scholar query volume modest —
  heavy automated scraping can trip Google's bot detection against the user's account.
- **Never close the tabs**; they are the standing external-brain + search lanes (matches CLAUDE.md
  "keep the external brain alive, never close").
- **Title-verify before every `select`** — indices are not stable.
- Each ChatGPT ping creates a chat in history (e.g. "Connectivity check request"); delete stray ones when tidying.

---

*Related: memory `browser-two-tab-pattern.md`; CLAUDE.md §2 external-brain binding; `research-tooling-channels`.*
