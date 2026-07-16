// Loads the INLINED module out of the built gate-calculator.html and evaluates a known case, so a
// test can prove the self-contained artifact actually runs (this catches inlining bugs like a
// duplicate const that the per-module parity test cannot see). Prints "<decision> <shares>".
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "..");
const html = readFileSync(join(here, "gate-calculator.html"), "utf8");
const module = html.split('<script type="module">')[1].split("</script>")[0];
const code = module.split("const $ =")[0] + "\nexport { evaluate, DISCLAIMER };";
const mod = await import("data:text/javascript," + encodeURIComponent(code));
const RATES = JSON.parse(readFileSync(join(root, "config", "statutory_rates.json"), "utf8"));
const r = mod.evaluate({
  symbol: "RELIANCE", segment: "delivery", entry: "100", stop: "95", targets: ["110"], atr: "1",
  equity: "200000", risk: "0.01", cap: "0.15", heat: "6000", gross: "80000", exposure: "1",
  brokerage: "0", dp: "15.34", tier: "swing",
  freshness: { feed_type: "ltp", mode: "eod", market_phase: "closed", age_seconds: 40000, present: true },
}, RATES);
if (!mod.DISCLAIMER.includes("market risks")) { console.error("disclaimer missing"); process.exit(1); }
console.log(r.decision, r.shares);
