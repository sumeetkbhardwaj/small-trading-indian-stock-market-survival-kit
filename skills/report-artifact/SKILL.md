---
name: report-artifact
description: The shared visual design system for the kit's beautiful, self-contained HTML report Artifacts — screen shortlist, portfolio evaluation, watchlist status, research brief, premarket/EOD digest. Use whenever another skill renders a report as a claude.ai Artifact so every report shares one calm, disciplined, scannable identity with provenance labels and the SEBI disclaimer. Read-only presentation only.
---

# Report Artifact — shared design system (survival-first)

Render reports as a **self-contained** claude.ai Artifact (single HTML file) only on surfaces that support Artifacts; otherwise emit a clean text digest. The report **presents** numbers the deterministic gate/helpers already computed — it never computes or asserts a figure itself, and never adds a number the data didn't carry.

## Hard rules (non-negotiable)
- **Self-contained, CSP-safe.** No external fonts, scripts, images, or fetch/XHR — the artifact CSP blocks them. Inline all CSS; use a system font stack (below); draw any chart with inline `<canvas>` + JS, not remote libraries.
- **Theme-aware.** Define tokens on `:root`, redefine under `@media (prefers-color-scheme: dark)` **and** under `:root[data-theme="dark"]` / `:root[data-theme="light"]` (the viewer's toggle stamps `data-theme` and must win both directions). Style through tokens, never hard-coded colors.
- **Figures line up.** `font-variant-numeric: tabular-nums` on every column of money/percent/shares. Wide tables live in an `overflow-x: auto` container so the body never scrolls sideways.
- **Provenance on every number.** Show `delay_class` (live / **delayed** / manual) and `as_of` near each figure or as a per-section stamp — delayed data is always labeled delayed.
- **Verdict = semantic state, not accent.** Encode state in form: a pill/chip with its own color, separate from the accent hue — HOLD/TRADE = good, TRIM/caution = warn, EXIT/NO-TRADE/STAND-DOWN = critical/neutral. Scannable at a glance.
- **Mandatory disclaimer footer** — the verbatim SEBI-safe disclaimer (from `scripts/disclaimer.py`) at the foot of every report.
- **Compliance copy.** No price targets, no "assured/guaranteed/risk-free/target-return", no performance claims, no SEBI reg number / exchange logos. Default framing is NO-TRADE.

## Design plan (tokens)
Calm, disciplined, ledger-like — the opposite of a casino/finfluencer look. Neutrals carry a slight cool ink bias; one restrained accent (deep teal); semantic greens/ambers/reds reserved for verdict state.

```css
:root{
  --paper:#f7f8f7; --ink:#12201f; --muted:#5c6b69; --line:#e2e6e4; --card:#ffffff;
  --accent:#0f6f6b;                     /* deep teal — the one bold hue, used sparingly */
  --good:#2f7a4f; --warn:#a86b12; --bad:#b23b3b; --neutral:#6b7472;  /* semantic verdicts */
  --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --serif:ui-serif,Georgia,"Times New Roman",serif;   /* display headings, used with restraint */
}
@media (prefers-color-scheme:dark){:root{
  --paper:#0e1413; --ink:#e7edea; --muted:#93a19e; --line:#233029; --card:#141c1a;
  --accent:#3fb3ad; --good:#57b07e; --warn:#d29b4a; --bad:#e0736f; --neutral:#8a938f;
}}
:root[data-theme="dark"]{--paper:#0e1413;--ink:#e7edea;--muted:#93a19e;--line:#233029;--card:#141c1a;--accent:#3fb3ad;--good:#57b07e;--warn:#d29b4a;--bad:#e0736f;--neutral:#8a938f;}
:root[data-theme="light"]{--paper:#f7f8f7;--ink:#12201f;--muted:#5c6b69;--line:#e2e6e4;--card:#ffffff;--accent:#0f6f6b;--good:#2f7a4f;--warn:#a86b12;--bad:#b23b3b;--neutral:#6b7472;}
```
Body text in `--sans` near 65ch; section headings in `--serif` with `text-wrap:balance`; all data in `--mono` tabular. Uppercase eyebrow labels get slight letter-spacing. Respect `prefers-reduced-motion`; give focus a visible ring.

## Layout — summary first, then detail
Open with a **status banner** (the one thing that needs attention: regime posture, or the dominant verdict), then the detail. Per report:
- **Opportunity screen** — a shortlist table: `symbol · entry · stop · shares · target(R) · net break-even · dominant reason`, each row a verdict pill. If empty: a single calm "No trade — dominant gate: …" card.
- **Portfolio eval** — total value + concentration/health callouts up top; a composition table with horizontal weight bars (canvas or CSS), unrealized P&L% colored by sign, and a HOLD/TRIM/EXIT pill per name.
- **Watchlist** — setups grouped by status (triggered → armed → extended → invalidated/aged-out), each with pivot · price · age; extended/invalidated visually de-emphasized.
- **Research brief** — sections (snapshot · **risks/red-flags first** · quality · valuation · technical) with a red-flags table and a sources list.
- **Premarket / EOD digest** — regime posture banner + holdings-needing-action + up to 3 opportunities, compact.

## Never
- Never compute or invent a number in the artifact; render only what the gate/helpers produced, with its provenance.
- Never omit the disclaimer footer or the delayed-data labels. Never use forbidden performance/target language.
